"""
review_generator.py — 과거 블로그 예측 검증 및 Thesis 팔로업 리뷰 생성기

실행:
  python review_generator.py               # 가장 최근 블로그 대상 자동 리뷰
  python review_generator.py --file 경로    # 특정 블로그 지정 리뷰

기능:
  - output/blog/ 내의 과거 블로그 파일 탐색 및 테제/가설 로드
  - 해당 Thesis 관련 최근 뉴스 데이터 대조 분석
  - '당시의 예측 vs 현재의 팩트' 사후 검증 콘텐츠 생성
  - output/review/YYYY-MM-DD-review-{slug}.md 저장
"""

import argparse
import json
import re
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

import config
from notifier import send_discord
from thesis_loader import load_thesis_by_id


def find_latest_blog() -> Path | None:
    """output/blog/ 폴더에서 가장 최근 생성된 마크다운 파일 탐색"""
    blog_dir = config.OUTPUT_DIR / "blog"
    if not blog_dir.exists():
        return None
    files = sorted(blog_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def parse_blog_content(filepath: Path) -> dict:
    """블로그 파일에서 프론트매터 및 본문 발췌"""
    text = filepath.read_text(encoding="utf-8")
    frontmatter_match = re.search(r"^---\n(.*?)\n---", text, re.DOTALL)
    meta = {}
    if frontmatter_match:
        for line in frontmatter_match.group(1).split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"').strip("'")

    # 본문 요약 (서론/결론 발췌)
    return {
        "title": meta.get("title", filepath.stem),
        "date": meta.get("date", ""),
        "thesis": meta.get("thesis", "[]"),
        "raw_text": text[:3000]
    }


def fetch_thesis_recent_news(thesis_ids: list[str], days: int = 7) -> list[dict]:
    """해당 Thesis 관련 최근 뉴스 조회"""
    if not config.NEWS_DB_PATH.exists():
        return []

    from thesis_loader import get_active_keywords
    kmap = get_active_keywords()

    target_keywords = set()
    for tid in thesis_ids:
        target_keywords.update(kmap.get(tid, []))

    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    conn = sqlite3.connect(config.NEWS_DB_PATH)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT company, title, snippet, score, published
        FROM news
        WHERE published >= ? OR collected_at >= ?
        ORDER BY score DESC
        LIMIT 50
    """, (since, since)).fetchall()
    conn.close()

    matched = []
    for r in rows:
        title = r["title"]
        if any(kw in title for kw in target_keywords):
            matched.append(dict(r))
    return matched[:10]


def build_review_prompt(blog_info: dict, recent_news: list[dict], rag_context: str = "") -> str:
    news_text = "\n".join([f"- [{n.get('company','')}] {n['title']} (점수: {n['score']})" for n in recent_news]) or "(최근 관련 뉴스 미발견)"
    rag_section = f"\n\n[증권사 리포트 및 지식 DB 참조 데이터]\n{rag_context}\n" if rag_context else ""

    return f"""당신은 테크/투자 콘텐츠 사후 검증(Fact-Check) 전문가입니다.
과거에 작성된 [블로그 글]의 핵심 주장 및 예측과, 그 이후 발생한 [최신 팩트/뉴스]를 대조하여
독자에게 깊은 신뢰를 주는 'Thesis 추적 & 리뷰 보고서'를 마크다운 형식으로 작성하세요.

[과거 작성된 원문 정보]
- 제목: {blog_info['title']}
- 작성일: {blog_info['date']}
- 관련 테제: {blog_info['thesis']}
- 원문 요약:
{blog_info['raw_text'][:1500]}

[이후 발생한 최신 팩트 & 뉴스]
{news_text}{rag_section}

[작성 가이드라인]
1. 제목: [리뷰 & 추적] {blog_info['title']} — 무엇이 맞았고 무엇이 빗나갔나?
2. 1부: '우리가 그때 던졌던 핵심 가설' (원문 요약)
3. 2부: '새로 확인된 데이터와 시장의 답' (최신 팩트와 수치로 검증, 증권사 리포트 데이터 적극 인용)
4. 3부: 'Thesis 업데이트 & 수정된 포지션 뷰' (가설 유효성 평가: 강화 / 유지 / 수정 / 폐기)
5. 어조: 냉철하고 객관적이며 투명한 분석 톤

마크다운 형식으로 바로 작성하세요."""


from llm_client import call_llm

def call_gemini(prompt: str) -> str:
    """통합 LLM 호출 (Gemini 우선, 실패 시 OpenCode 대체)"""
    return call_llm(prompt)


def generate_review(blog_path: Path = None, use_rag: bool = False) -> Path:
    target_blog = blog_path or find_latest_blog()
    if not target_blog or not target_blog.exists():
        print("  ⚠️  리뷰할 과거 블로그를 찾을 수 없습니다.")
        return None

    print(f"\n🔍 [Review Generator] 대상 블로그: {target_blog.name}")
    blog_info = parse_blog_content(target_blog)

    # 테제 ID 파싱
    thesis_ids = []
    try:
        thesis_ids = json.loads(blog_info["thesis"].replace("'", '"'))
    except Exception:
        thesis_ids = re.findall(r"T-\d+", blog_info["thesis"])

    print(f"  연관 테제: {thesis_ids}")
    recent_news = fetch_thesis_recent_news(thesis_ids)
    print(f"  검증에 대조할 최근 뉴스: {len(recent_news)}건")

    # RAG 심층 검색 (옵션 활성화 시)
    rag_context = ""
    if use_rag:
        try:
            from rag_engine import search, format_rag_context
            query = f"{blog_info['title']} {' '.join(thesis_ids)}"
            chunks = search(query, n_results=config.RAG_TOP_K)
            if chunks:
                print(f"  🔍 [RAG 활성화] 지식 DB에서 관련 리포트 {len(chunks)}개 청크 검색 및 주입")
                rag_context = format_rag_context(chunks)
            else:
                print("  ℹ️ [RAG 활성화] 관련 리포트 청크 없음 (기본 모드로 진행)")
        except Exception as e:
            print(f"  ⚠️ RAG 검색 오류 (기본 모드로 대체): {e}")

    prompt = build_review_prompt(blog_info, recent_news, rag_context=rag_context)
    print("  🤖 Gemini로 사후 검증 리뷰 작성 중...")
    content = call_gemini(prompt)

    content = re.sub(r"^```(?:markdown)?\n?", "", content.strip())
    content = re.sub(r"\n?```$", "", content.strip())

    today_str = date.today().isoformat()
    header = f"""---
title: "[리뷰] {blog_info['title']}"
date: {today_str}
type: review
target_blog: "{target_blog.name}"
thesis: {json.dumps(thesis_ids, ensure_ascii=False)}
rag_enhanced: {str(use_rag).lower()}
---

"""
    full_doc = header + content

    review_dir = config.OUTPUT_DIR / "review"
    review_dir.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^\w\s가-힣]", "", blog_info["title"])[:30].strip().replace(" ", "-")
    out_file = review_dir / f"{today_str}-review-{slug}.md"
    out_file.write_text(full_doc, encoding="utf-8")

    print(f"  ✅ 리뷰 저장 완료: {out_file}")

    try:
        from obsidian_sync import sync_file
        sync_file(out_file, "review")
    except Exception:
        pass

    send_discord(
        message=f"🔍 **Argus Pulse 과거 예측 사후 리뷰**가 발행되었습니다: `{out_file.name}`"
    )

    return out_file


def main():
    parser = argparse.ArgumentParser(description="Argus Pulse 과거 예측 사후 리뷰 생성기")
    parser.add_argument("--file", type=str, help="특정 블로그 파일 경로")
    parser.add_argument("--rag",  action="store_true", help="증권사 리포트 및 지식 DB RAG 심층 검색 활용")
    args = parser.parse_args()
    path = Path(args.file) if args.file else None
    generate_review(path, use_rag=args.rag)


if __name__ == "__main__":
    main()
