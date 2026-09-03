"""
thread_writer.py — 선택된 주제로 구어체 팩트 스레드 생성

각도(Angle):
  A: 수혜 계산 각도 — 숫자·팩트 중심, 투자자 타깃
  B: 구조 변화 각도 — 산업 스토리, 일반 독자 타깃
  C: 공장/실행 각도 — 리스크·회의적 시각

Human in the Loop:
  1. 각도 선택 (A/B/C)
  2. 도입부 5줄 미리보기 → 재생성 or 확인
  3. 결말 5줄 미리보기 → 수정 or 확인
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import config
from thesis_loader import load_thesis_by_id


ANGLE_DESCRIPTIONS = {
    "A": "수혜 계산 각도 — 숫자·팩트 중심, 투자자 타깃\n     예) GWh, %, 조원 등 구체 수치로 수혜 구조 설명",
    "B": "구조 변화 각도 — 산업 판도 변화 스토리, 일반 독자 타깃\n     예) '왜 지금인가', '무엇이 달라지나' 흐름",
    "C": "공장/실행 각도 — 리스크·회의적 시각\n     예) '착시인가', '진짜 문제는 뭔가' 반론 구조",
}


# ── 프롬프트 구성 ──────────────────────────────────────────────────────────────

def build_thread_prompt(topic: dict, angle: str, rag_context: str = "", length: str = "deep") -> str:
    thesis_ids = topic.get("thesis_ids", [])
    thesis_context = []
    for tid in thesis_ids:
        t = load_thesis_by_id(tid)
        if t:
            thesis_context.append(f"- [{tid}] {t['title']}: {t['hypothesis']}")
    thesis_str = "\n".join(thesis_context) or "(Thesis 없음)"

    outline = topic.get("outline", {})
    outline_str = " → ".join(outline.values()) if outline else topic.get("hook", "")

    angle_guide = {
        "A": "숫자와 팩트 중심. 각 줄에 반드시 수치(%, $, GWh, 조원 등)를 포함. 투자 수혜 구조를 단계적으로 설명.",
        "B": "산업 변화 스토리. '왜 지금인가', '무엇이 달라지나'를 흐름으로 서술. 숫자보다 맥락 중심.",
        "C": "회의적·리스크 각도. 대중의 기대에 반론. '진짜 문제는', '착시인가'를 중심으로 균형 잡힌 시각.",
    }[angle]

    rag_section = f"\n\n[증권사 리포트 및 심층 데이터 참조]\n{rag_context}\n" if rag_context else ""

    if length == "compact":
        structure_guide = """- 구조 및 분량: 총 10~15번 (모바일 스크롤 완독형 압축 스레드)
- 도입부 (1~2번): 시선을 잡는 강렬한 팩트/한 줄 요약
- 중간 (3~10번): 핵심 수치와 구조적 변화 설명
- 결말 (11~13번): 앞으로의 투자 결론 및 관전 포인트"""
    else:
        structure_guide = """- 구조 및 분량: 총 25~35번 (심층 리포트형 롱폼 스레드)
- 도입부 (1~5번): 핵심 한 줄 요약으로 시작, 왜 읽어야 하는지 명확히
- 중간 (6~25번): 팩트와 분석을 번갈아 배치
- 결말 (마지막 5번): '앞으로 볼 것' 또는 핵심 정리로 마무리"""

    return f"""당신은 테크/투자 분야 트위터·텔레그램 인플루언서입니다.
아래 [주제]를 [{angle}각도]로 풀어, 구어체 번호 나열 스레드를 작성하세요.

[주제]
제목: {topic.get('title', '')}
훅: {topic.get('hook', '')}
흐름: {outline_str}

[관련 Thesis]
{thesis_str}{rag_section}

[{angle}각도 작성 지침]
{angle_guide}

[작성 규칙]
- 각 줄: 번호. 내용 (1~2문장)
- 말투: '~임', '~함', '~됨', '~음' (구어체, 문어체 금지)
- 숫자: 구체적 수치 반드시 포함 (GWh, %, 조원, YoY 등)
- 전문 용어: 기본 금융 용어(CAPEX, ROIC, PER 등)는 괄호 해설 없이 바로 쓰고, 생소한 테크 용어만 첫 등장 시 괄호 설명
- 증권사 리포트 및 심층 데이터가 제공된 경우, 구체적인 추정치와 수치를 각 줄에 적극 반영하세요.
{structure_guide}
- JSON이나 코드 블록 없이 순수 번호 나열로만 출력

번호 1번부터 바로 시작하세요."""


# ── LLM 호출 ──────────────────────────────────────────────────────────────────
from llm_client import call_llm

def call_gemini(prompt: str) -> str:
    """통합 LLM 호출 (Gemini 우선, 실패 시 OpenCode 대체)"""
    return call_llm(prompt)


# ── 파싱 ──────────────────────────────────────────────────────────────────────

def parse_thread_lines(text: str) -> list[str]:
    """LLM 출력에서 번호 줄(1. ~ N.)만 추출"""
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if re.match(r"^\d+[\.\)]\s+", line):
            lines.append(line)
    return lines


# ── 파일 저장 ──────────────────────────────────────────────────────────────────

def make_slug(title: str) -> str:
    slug = re.sub(r"[^\w\s가-힣]", "", title)
    slug = re.sub(r"\s+", "-", slug.strip())
    return slug[:40]


def save_thread(lines: list[str], title: str, angle: str, topic: dict = None) -> Path:
    today = date.today().isoformat()
    slug = make_slug(title)
    base = config.OUTPUT_DIR / "thread" / f"{today}-thread-{slug}-{angle}"

    filepath = Path(f"{base}.md")
    i = 1
    while filepath.exists():
        filepath = Path(f"{base}-{i}.md")
        i += 1

    content = f"---\ntitle: \"{title}\"\ndate: {today}\nangle: \"{angle}\"\nstatus: draft\n---\n\n"
    content += "\n".join(lines)

    # 참고 자료 및 출처 섹션 자동 부착
    if topic:
        thesis_ids = topic.get("thesis_ids", [])
        ref_lines = ["\n\n---\n\n## 📚 핵심 참고 자료 및 출처 (Data Sources & Links)"]
        if thesis_ids:
            ref_lines.append("### 1. 연계 투자 테제 (Thesis)")
            for tid in thesis_ids:
                t = load_thesis_by_id(tid)
                if t:
                    ref_lines.append(f"- `[[{tid} {t['title']}]]`: {t['hypothesis']}")
                else:
                    ref_lines.append(f"- `[[{tid}]]`")
        
        hook = topic.get("hook", "")
        if hook:
            ref_lines.append(f"\n### 2. 시장 트리거 & 데이터 소스\n- **분석 팩트**: {hook}")
            
        content += "\n".join(ref_lines)

    filepath.write_text(content, encoding="utf-8")
    return filepath


# ── HitL 미리보기 ─────────────────────────────────────────────────────────────

def preview_section(lines: list[str], label: str, n: int = 5) -> bool:
    print(f"\n── {label} ({'앞' if '도입' in label else '뒤'} {n}줄) ──")
    preview = lines[:n] if "도입" in label else lines[-n:]
    for line in preview:
        print(f"  {line}")
    choice = input(f"\n✅ 확인 (y=계속 / r=전체 재생성): ").strip().lower()
    return choice != "r"


# ── 메인 ──────────────────────────────────────────────────────────────────────

def generate_thread(topic: dict, angle: str, interactive: bool = True, use_rag: bool = False, length: str = "deep") -> Path:
    """주제 dict + 각도 → 스레드 파일 생성 후 경로 반환"""
    print(f"\n  🤖 스레드 생성 중... (각도:{angle}, 길이:{length} / {config.GEMINI_MODEL})")

    # RAG 심층 검색 (옵션 활성화 시)
    rag_context = ""
    if use_rag:
        try:
            from rag_engine import search, format_rag_context
            title = topic.get("title", "")
            thesis_ids = topic.get("thesis_ids", [])
            query = f"{title} {' '.join(thesis_ids)}"
            chunks = search(query, n_results=config.RAG_TOP_K)
            if chunks:
                print(f"  🔍 [RAG 활성화] 지식 DB에서 관련 리포트/자료 {len(chunks)}개 청크 검색 및 주입")
                rag_context = format_rag_context(chunks)
            else:
                print("  ℹ️ [RAG 활성화] 관련 리포트 청크 없음 (기본 모드로 진행)")
        except Exception as e:
            print(f"  ⚠️ RAG 검색 오류 (기본 모드로 대체): {e}")

    min_lines = 8 if length == "compact" else 15
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        prompt = build_thread_prompt(topic, angle, rag_context=rag_context, length=length)
        raw = call_gemini(prompt)
        lines = parse_thread_lines(raw)

        if len(lines) < min_lines:
            print(f"  ⚠️  줄 수 부족 ({len(lines)}줄) — 재시도 {attempt}/{max_retries}")
            continue

        print(f"  생성 완료: {len(lines)}줄")

        if interactive:
            # HitL — 도입부 확인
            if not preview_section(lines, "도입부 확인", n=5):
                print("  재생성 중...")
                continue

            # HitL — 결말 확인
            if not preview_section(lines, "결말 확인", n=5):
                print("  재생성 중...")
                continue

        break
    else:
        print("  ❌ 재시도 초과. 현재 결과로 저장합니다.")

    # 전체 출력
    print()
    print("─" * 60)
    print(f"📋 전체 스레드 ({len(lines)}줄)")
    print("─" * 60)
    for line in lines[:10]:
        print(line)
    if len(lines) > 10:
        print(f"... ({len(lines)-10}줄 생략)")
    print("─" * 60)

    if interactive:
        save_choice = input("저장하시겠습니까? (y/n): ").strip().lower()
        if save_choice == "n":
            print("  취소됨.")
            sys.exit(0)

    filepath = save_thread(lines, topic.get("title", "thread"), angle, topic=topic)
    print(f"\n  ✅ 저장 완료: {filepath}")

    try:
        from obsidian_sync import sync_file
        sync_file(filepath, "thread")
    except Exception:
        pass

    try:
        from notifier import notify_content_generated
        summary = lines[0] if lines else ""
        notify_content_generated("Thread", topic.get("title", "Thread"), filepath, summary)
    except Exception as e:
        print(f"  (알림 발송 생략: {e})")

    return filepath


def main():
    parser = argparse.ArgumentParser(description="Argus Pulse — 스레드 생성기")
    grp = parser.add_mutually_exclusive_group(required=True)
    grp.add_argument("--topic",    type=str, help="주제 JSON 문자열")
    grp.add_argument("--from-log", action="store_true", help="오늘의 topic 로그에서 선택")
    parser.add_argument("--angle", type=str, choices=["A", "B", "C"],
                        help="각도 선택 (없으면 대화형 선택)")
    parser.add_argument("--rag",   action="store_true", help="증권사 리포트 및 지식 DB RAG 심층 검색 활용")
    parser.add_argument("--length", choices=["compact", "deep"], default="deep", help="스레드 길이 (compact: 10~15줄, deep: 25~35줄)")
    parser.add_argument("--auto", "-y", action="store_true", help="대화형 확인 없이 자동 저장")
    args = parser.parse_args()

    if args.from_log:
        log_path = config.LOG_DIR / f"{date.today().isoformat()}-topics.json"
        if not log_path.exists():
            print(f"❌ 오늘의 주제 로그 없음: {log_path}")
            print("   먼저 python topic_generator.py 를 실행하세요.")
            sys.exit(1)
        data = json.loads(log_path.read_text(encoding="utf-8"))
        topics = data["topics"]
        print(f"\n📋 오늘의 주제:")
        for i, t in enumerate(topics, 1):
            print(f"  [{i}] {t['title']}")
        idx = int(input("번호 선택: ").strip()) - 1
        topic = topics[idx]
    else:
        topic = json.loads(args.topic)

    # 각도 선택
    angle = args.angle
    if not angle:
        print("\n각도 선택:")
        for k, v in ANGLE_DESCRIPTIONS.items():
            print(f"  {k}: {v}")
        angle = input("각도 (A/B/C): ").strip().upper() or "A"

    generate_thread(topic, angle, interactive=not args.auto, use_rag=args.rag, length=args.length)


if __name__ == "__main__":
    main()
