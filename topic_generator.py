"""
topic_generator.py — 블로그/스레드 주제 추천

뉴스 소스:
  --auto     : b_0826 SQLite DB 자동 수집 (기본값)
  --input    : MD/TXT/HTML 파일 직접 지정
  --raw      : 폴더 내 전체 파일 (기본: 99.raw/)
  --text     : 텍스트 직접 입력

실행:
  python topic_generator.py                           # 자동 모드
  python topic_generator.py --raw 99.raw             # 수동 폴더
  python topic_generator.py --input docs/askask.md   # 파일 지정
  python topic_generator.py --text "SK하이닉스 HBM4..."
"""

import argparse
import json
import re
import sqlite3
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import config
from html_parser import parse_file, parse_raw_folder, merge_contents, archive_processed_files
from thesis_loader import load_theses, get_active_keywords, load_thesis_by_id

# ── 뉴스 수집 ─────────────────────────────────────────────────────────────────

def load_recent_news(days: int = None, threshold: int = None, limit: int = None) -> list[dict]:
    """b_0826 SQLite에서 최근 고득점 뉴스 로드"""
    days      = days      or config.NEWS_LOOKBACK_DAYS
    threshold = threshold or config.NEWS_SCORE_THRESHOLD
    limit     = limit     or config.MAX_NEWS_FOR_PROMPT

    if not config.NEWS_DB_PATH.exists():
        print(f"  ⚠️  뉴스 DB 없음: {config.NEWS_DB_PATH}")
        return []

    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    conn = sqlite3.connect(config.NEWS_DB_PATH)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT company, ticker, title, snippet, score, source, published
        FROM news
        WHERE score >= ?
          AND (published >= ? OR collected_at >= ?)
        ORDER BY score DESC
        LIMIT ?
    """, (threshold, since, since, limit)).fetchall()
    conn.close()

    return [dict(r) for r in rows]


def should_generate_new(hot_news: list[dict]) -> bool:
    """고득점(HOT_THRESHOLD 이상) 뉴스가 MIN_COUNT 이상일 때만 새 콘텐츠 생성"""
    hot = [n for n in hot_news if n.get("score", 0) >= config.NEWS_HOT_THRESHOLD]
    return len(hot) >= config.HOT_NEWS_MIN_COUNT


# ── Thesis 매칭 ───────────────────────────────────────────────────────────────

def match_thesis_to_context(context: str, kmap: dict, top_n: int = 5) -> list[str]:
    """컨텍스트 텍스트에서 관련 Thesis ID를 점수 순으로 반환"""
    scores = {}
    for tid, keywords in kmap.items():
        score = sum(1 for kw in keywords if kw in context)
        if score > 0:
            scores[tid] = score
    sorted_ids = sorted(scores, key=scores.get, reverse=True)
    return sorted_ids[:top_n]


# ── 프롬프트 구성 ──────────────────────────────────────────────────────────────

def _build_news_text(news_list: list[dict]) -> str:
    lines = []
    for n in news_list:
        company = n.get("company") or n.get("source") or "?"
        title   = n.get("title", "")
        score   = n.get("score", 0)
        snippet = n.get("snippet", "")[:80]
        lines.append(f"- [{company}] {title} (점수:{score})\n  → {snippet}")
    return "\n".join(lines)


def _build_thesis_text(thesis_ids: list[str]) -> str:
    lines = []
    for tid in thesis_ids:
        t = load_thesis_by_id(tid)
        if t:
            lines.append(f"- [{tid}] {t['title']}: {t['hypothesis']}")
    return "\n".join(lines)


def build_topic_prompt(context: str, thesis_ids: list[str], num_topics: int) -> str:
    thesis_text = _build_thesis_text(thesis_ids)

    return f"""당신은 테크/투자 전문 수석 콘텐츠 디렉터입니다.
아래 [컨텍스트]와 [투자 테제]를 교차 분석하여,
독자의 시선을 사로잡는 블로그/스레드 기획안 {num_topics}개를 생성하세요.

[컨텍스트 — 최신 뉴스 및 분석]
{context[:3000]}

[관련 투자 테제]
{thesis_text}

[출력 형식 — 반드시 아래 JSON 배열로만 응답]
[
  {{
    "rank": 1,
    "title": "매력적이고 도발적인 제목",
    "angle": "기술진화 | 기업격돌 | 공급망병목 | 팩트체크 중 택1",
    "thesis_ids": ["T-XX"],
    "hook": "이 글을 읽어야 하는 이유 한 문장",
    "outline": {{
      "서론": "핵심 훅 — 무엇을 보여줄 것인가",
      "본론1": "첫 번째 핵심 논점",
      "본론2": "두 번째 핵심 논점 또는 반론",
      "결론": "투자 관점 & 다음 주목 이벤트"
    }},
    "title_variants": {{
      "A": "직관적 분석형 제목",
      "B": "도발적 의문형 제목",
      "C": "스토리텔링형 제목"
    }}
  }}
]

JSON 외 다른 텍스트는 절대 포함하지 마세요."""


# ── LLM 호출 ──────────────────────────────────────────────────────────────────
from llm_client import call_llm

def call_gemini(prompt: str) -> str:
    """통합 LLM 호출 (Gemini 우선, 실패 시 OpenCode 대체)"""
    return call_llm(prompt)


def parse_topics_json(raw: str) -> list[dict]:
    """LLM 응답에서 JSON 추출"""
    # 코드 블록 제거
    clean = re.sub(r"```(?:json)?", "", raw).strip().rstrip("```").strip()
    # JSON 배열 추출
    match = re.search(r"\[.*\]", clean, re.DOTALL)
    if match:
        return json.loads(match.group())
    return json.loads(clean)


# ── 출력 ──────────────────────────────────────────────────────────────────────

def display_topics(topics: list[dict]):
    print()
    print("━" * 60)
    print("📋  오늘의 콘텐츠 추천")
    print("━" * 60)
    for t in topics:
        rank = t.get("rank", "?")
        print(f"\n[{rank}] {t['title']}")
        print(f"     관점: {t.get('angle', '')}  |  Thesis: {', '.join(t.get('thesis_ids', []))}")
        print(f"     훅  : {t.get('hook', '')}")
        outline = t.get("outline", {})
        if outline:
            print(f"     목차: {' → '.join(outline.values())}")
        variants = t.get("title_variants", {})
        if variants:
            print(f"     제목A: {variants.get('A', '')}")
            print(f"     제목B: {variants.get('B', '')}")


def save_topics_log(topics: list[dict], source_label: str):
    """생성된 주제 목록을 로그 파일로 저장"""
    today = date.today().isoformat()
    log_path = config.LOG_DIR / f"{today}-topics.json"
    payload = {
        "date": today,
        "source": source_label,
        "topics": topics,
    }
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"\n  💾 주제 목록 저장: {log_path}")
    return log_path


# ── 메인 ──────────────────────────────────────────────────────────────────────

def generate_topics(context: str, source_label: str, num_topics: int = None) -> list[dict]:
    """컨텍스트로 주제 생성 (공통 로직)"""
    num_topics = num_topics or config.NUM_TOPICS
    kmap = get_active_keywords()
    thesis_ids = match_thesis_to_context(context, kmap, top_n=6)

    print(f"  📊 Thesis 매칭: {', '.join(thesis_ids)}")
    print(f"  🤖 LLM 호출 중... ({config.GEMINI_MODEL})")

    prompt = build_topic_prompt(context, thesis_ids, num_topics)
    raw = call_gemini(prompt)
    topics = parse_topics_json(raw)
    return topics


def main():
    parser = argparse.ArgumentParser(description="Argus Pulse — 주제 추천기")
    grp = parser.add_mutually_exclusive_group()
    grp.add_argument("--auto",  action="store_true", help="뉴스 DB 자동 수집 (기본)")
    grp.add_argument("--raw",   type=str, nargs="?", const="99.raw",
                     help="폴더 내 파일 파싱 (기본: 99.raw)")
    grp.add_argument("--input", type=str, help="파일 직접 지정 (MD/TXT/HTML)")
    grp.add_argument("--text",  type=str, help="텍스트 직접 입력")
    parser.add_argument("--n",  type=int, default=config.NUM_TOPICS, help="추천 개수")
    parser.add_argument("--archive", action="store_true", help="수동 입력 파일 처리 후 자동으로 archive/ 로 이동")
    args = parser.parse_args()

    print("\n🔍 Argus Pulse — 주제 추천 시작")
    print(f"   시각: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    parsed_raw_files = []

    # ── 소스 결정 ──────────────────────────────────────────────────────────────
    if args.raw is not None:
        print(f"\n📂 수동 입력 [폴더]: {args.raw}")
        parsed = parse_raw_folder(args.raw)
        if not parsed:
            print("  ❌ 파싱된 파일 없음")
            sys.exit(1)
        parsed_raw_files = [p["filepath"] for p in parsed]
        context = merge_contents(parsed)
        source_label = f"folder:{args.raw}"

    elif args.input:
        print(f"\n📄 수동 입력 [파일]: {args.input}")
        result = parse_file(args.input)
        if not result["content"]:
            print("  ❌ 본문 추출 실패")
            sys.exit(1)
        print(f"  추출: {result['char_count']:,}자 ({result['type']})")
        parsed_raw_files = [args.input]
        context = result["content"]
        source_label = f"file:{Path(args.input).name}"

    elif args.text:
        print("\n📝 수동 입력 [텍스트]")
        context = args.text
        source_label = "text:direct"

    else:  # --auto (기본)
        print(f"\n📡 자동 수집: 최근 {config.NEWS_LOOKBACK_DAYS}일 / 점수≥{config.NEWS_SCORE_THRESHOLD}")
        news = load_recent_news()
        if not news:
            print("  ❌ 뉴스 없음 — --raw 또는 --input 모드를 사용하세요")
            sys.exit(1)
        print(f"  수집: {len(news)}건")

        if not should_generate_new(news):
            hot_count = sum(1 for n in news if n.get("score", 0) >= config.NEWS_HOT_THRESHOLD)
            print(f"\n  ⚠️  고득점 뉴스 {hot_count}건 — {config.HOT_NEWS_MIN_COUNT}건 미달")
            print("     → 리뷰 모드를 사용하려면: python review_generator.py")
            sys.exit(0)

        context = _build_news_text(news)
        source_label = "auto:sqlite"

    # ── 주제 생성 ──────────────────────────────────────────────────────────────
    try:
        topics = generate_topics(context, source_label, num_topics=args.n)
    except Exception as e:
        print(f"\n  ❌ LLM 오류: {e}")
        sys.exit(1)

    # ── 출력 ──────────────────────────────────────────────────────────────────
    display_topics(topics)
    save_topics_log(topics, source_label)

    try:
        from notifier import notify_topics_ready
        notify_topics_ready(topics)
    except Exception as e:
        pass

    # ── Human in the Loop ──────────────────────────────────────────────────────
    print()
    print("━" * 60)
    print("번호 선택 + 포맷 (예: 1b=블로그, 1br=RAG심층블로그, 2t=스레드, 2tr=RAG심층스레드, s=건너뜀)")
    choice = input("→ ").strip().lower()

    if choice == "s" or not choice:
        print("건너뜀. 필요 시: python review_generator.py")
        return

    # 번호 + 포맷 + RAG 파싱 (예: 1, 1b, 1br, 1r, 2t, 2tr)
    match = re.match(r"^(\d+)([btr]{0,2})$", choice)
    if not match:
        print("입력 오류. 예: 1b, 1br, 2t, 2tr")
        return

    idx = int(match.group(1)) - 1
    mod_str = match.group(2)
    fmt = "t" if "t" in mod_str else "b"
    use_rag = "r" in mod_str

    if idx < 0 or idx >= len(topics):
        print(f"번호 범위 오류: 1~{len(topics)}")
        return

    selected = topics[idx]
    if fmt == "b":
        mode_label = " [RAG 심층 모드]" if use_rag else ""
        print(f"\n→ blog_writer.py 실행{mode_label}: [{selected['title']}]")
        import subprocess
        cmd = [
            sys.executable, "blog_writer.py",
            "--topic", json.dumps(selected, ensure_ascii=False)
        ]
        if use_rag:
            cmd.append("--rag")
        subprocess.run(cmd)
    else:
        mode_label = " [RAG 심층 모드]" if use_rag else ""
        print(f"\n→ thread_writer.py 실행{mode_label}: [{selected['title']}]")
        # 각도 선택
        print("\n각도 선택:")
        print("  A: 수혜 계산 각도 — 숫자·팩트 중심")
        print("  B: 구조 변화 각도 — 산업 스토리")
        print("  C: 공장/실행 각도 — 리스크 중심")
        angle = input("각도 (A/B/C): ").strip().upper() or "A"
        import subprocess
        cmd = [
            sys.executable, "thread_writer.py",
            "--topic", json.dumps(selected, ensure_ascii=False),
            "--angle", angle
        ]
        if use_rag:
            cmd.append("--rag")
        subprocess.run(cmd)

    # ── 원본 파일 아카이빙 (수동 파일 입력 시) ──────────────────────────────────
    if parsed_raw_files:
        if args.archive:
            archive_processed_files(parsed_raw_files)
        else:
            arch_choice = input("\n📦 분석에 사용된 원본 파일을 archive/ 로 이동할까요? (y/n, 기본 y): ").strip().lower()
            if arch_choice in ("y", ""):
                archive_processed_files(parsed_raw_files)


if __name__ == "__main__":
    main()
