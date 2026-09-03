"""
blog_writer.py — 선택된 주제로 2-Page 블로그 초안 생성

실행:
  python blog_writer.py --topic '{"title":"...","angle":"...","thesis_ids":["T-02"],"outline":{...}}'
  python blog_writer.py --from-log   # 오늘 저장된 logs/YYYY-MM-DD-topics.json 사용

Human in the Loop:
  - 제목 3종(A/B/C) 중 선택
  - 생성 후 미리보기 확인
"""

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

import config
from thesis_loader import load_thesis_by_id


# ── Thesis 가이드 로드 ─────────────────────────────────────────────────────────

def load_thesis_guide(thesis_ids: list[str]) -> str:
    """blog_thesis_guides.md에서 해당 Thesis 섹션 추출, 없으면 Thesis 파일 본문 사용"""
    guide_path = config.ROOT_DIR / "docs" / "blog_thesis_guides.md"
    sections = []

    if guide_path.exists():
        full = guide_path.read_text(encoding="utf-8")
        for tid in thesis_ids:
            # ## T-XX: 제목 섹션 추출
            pattern = rf"(## {tid}:.+?)(?=\n## T-|\Z)"
            match = re.search(pattern, full, re.DOTALL)
            if match:
                sections.append(match.group(1).strip())
                continue

            # 가이드에 없으면 Thesis 파일 hypothesis 사용
            t = load_thesis_by_id(tid)
            if t:
                sections.append(
                    f"## {tid}: {t['title']}\n"
                    f"- 핵심 가설: {t['hypothesis']}\n"
                    f"- 관련 키워드: {', '.join(t.get('keywords', []))}"
                )

    return "\n\n".join(sections)


# ── 프롬프트 구성 ──────────────────────────────────────────────────────────────

def build_blog_prompt(topic: dict, thesis_guide: str, selected_title: str, rag_context: str = "") -> str:
    outline = topic.get("outline", {})
    outline_str = "\n".join([f"  - {k}: {v}" for k, v in outline.items()])
    today = date.today().isoformat()

    rag_section = f"\n\n[증권사 리포트 및 심층 데이터]\n{rag_context}\n" if rag_context else ""

    return f"""당신은 테크/투자 전문 블로그 작가입니다.
아래 [기획안]을 바탕으로 [양식]에 맞는 블로그 초안을 작성하세요.

[기획안]
- 제목: {selected_title}
- 관점(Angle): {topic.get('angle', '')}
- 관련 Thesis: {', '.join(topic.get('thesis_ids', []))}
- 핵심 훅: {topic.get('hook', '')}
- 목차:
{outline_str}

[Thesis 작성 가이드]
{thesis_guide if thesis_guide else '(가이드 없음 — 기획안 기반으로 작성)'}{rag_section}

[양식 및 작성 규칙]
1. 어조: 날카롭고 명료한 시니어 애널리스트 톤 (불필요한 미사여구 배제, 단호하고 통찰력 있는 분석)
2. 전문 용어 규칙:
   - 기초 금융/투자 용어(CAPEX, ROIC, PER, WACC, EPS, LTV 등)는 괄호 설명 없이 즉시 사용
   - 생소한 핵심 테크/공정 용어(베이스 다이, CoWoS, TSV, zHBM 등)만 최초 1회 간결하게 설명
3. 시각적 구조:
   - 각 문단의 첫 문장은 핵심 결론을 담아 **볼드 처리**
   - 본론 1 또는 본론 2 내에 반드시 3~4열로 구성된 **마크다운 비교 표(Table)** 1개 이상 삽입 (예: 기업 간 경쟁 구도, 세대별 사양 비교, 수혜 vs 리스크)
   - 핵심 수치는 `> 💡 데이터 박스` 인용구 블록으로 집약
4. 증권사 리포트/지식 DB가 제공된 경우, 구체적 출처(증권사명/일자)와 추정 수치를 본문에 자연스럽게 인용

```markdown
---
title: "{selected_title}"
date: {today}
thesis: {json.dumps(topic.get('thesis_ids', []), ensure_ascii=False)}
angle: "{topic.get('angle', '')}"
status: draft
tags: []
trigger: "{topic.get('hook', '')[:60]}"
reading_time: "4분"
---

# {selected_title}

> **한 줄 요약**: (이 글의 핵심을 한 문장으로)

---

## 서론: (왜 지금 이 글을 읽어야 하는가)

(독자의 주의를 끄는 수치/사실로 시작, 맥락 2~3줄, 이 글의 핵심 질문 제시)

---

## 본론 1: (첫 번째 핵심 논점)

### (소제목)
(핵심 팩트/데이터 + 분석)

### (소제목)
(추가 근거 + 업계 동향 및 비교 표)

| 구분 | A 기업/기술 | B 기업/기술 | 핵심 차별점 |
|---|---|---|---|
| ... | ... | ... | ... |

> 💡 **데이터 박스**
> - 수치 1: ...
> - 수치 2: ...

---

## 본론 2: (두 번째 핵심 논점)

### (소제목)
(핵심 팩트 + 분석)

### (반론 또는 리스크)
(균형 잡힌 시각)

---

## 결론: 투자 관점 & 핵심 테이크어웨이

### 💡 핵심 인사이트
1. 
2. 
3. 

### ⚠️ 리스크 요인
- 

### 👀 다음에 주목할 것
- (날짜, 이벤트, 지표)

---

> **면책**: 이 글은 투자 권유가 아닌 산업 분석 목적의 콘텐츠입니다.

---

## 📚 참고 자료 및 출처 (References)
- **[증권사 리포트]**: 발행사, 리포트명, 일자 (원문 PDF 링크 또는 출처 기재)
- **[뉴스 및 공시]**: 언론사/기관명, 기사 제목 및 일자
- **[관련 테제 & 지식]**: [[관련 Thesis ID 및 제목]]
```

[작성 시 자기 검토 후 제출]
✅ 본론에 마크다운 비교 표(Table)가 1개 이상 포함되었는가?
✅ 문단 첫 머리에 핵심 문장이 볼드로 강조되었는가?
✅ 기본 금융 용어(CAPEX, ROIC 등)의 불필요한 괄호 설명이 생략되고 템포가 빠른가?
✅ 결론에 3대 인사이트와 다음 주목 이벤트가 있는가?
✅ 문서 하단에 [참고 자료 및 출처(References)] 섹션에 증권사 리포트/뉴스/URL이 명확히 기재되었는가?
위 조건을 모두 충족하는 마크다운 초안만 출력하세요."""


# ── LLM 호출 ──────────────────────────────────────────────────────────────────
from llm_client import call_llm

def call_gemini(prompt: str) -> str:
    """통합 LLM 호출 (Gemini 우선, 실패 시 OpenCode 대체)"""
    return call_llm(prompt)


# ── 파일 저장 ──────────────────────────────────────────────────────────────────

def make_slug(title: str) -> str:
    """한글+영문 제목 → 파일명용 slug"""
    slug = re.sub(r"[^\w\s가-힣]", "", title)
    slug = re.sub(r"\s+", "-", slug.strip())
    return slug[:40]


def save_blog(content: str, title: str) -> Path:
    """output/blog/YYYY-MM-DD-blog-{slug}.md 로 저장 (중복 시 suffix)"""
    today = date.today().isoformat()
    slug = make_slug(title)
    base = config.OUTPUT_DIR / "blog" / f"{today}-blog-{slug}"

    filepath = Path(f"{base}.md")
    i = 1
    while filepath.exists():
        filepath = Path(f"{base}-{i}.md")
        i += 1

    filepath.write_text(content, encoding="utf-8")
    return filepath


# ── 미리보기 ──────────────────────────────────────────────────────────────────

def preview_blog(content: str, lines: int = 20):
    print()
    print("─" * 60)
    print("📄 생성된 블로그 미리보기 (처음 20줄)")
    print("─" * 60)
    for line in content.split("\n")[:lines]:
        print(line)
    print("─" * 60)


# ── 메인 ──────────────────────────────────────────────────────────────────────

def generate_blog(topic: dict, title_choice: str = None, interactive: bool = True, use_rag: bool = False, use_critic: bool = False) -> Path:
    """주제 dict → 블로그 파일 생성 후 경로 반환"""

    variants = topic.get("title_variants", {})
    default_title = topic.get("title", "")

    if interactive and variants:
        print()
        print("📝 제목을 선택하세요:")
        print(f"   기본: {default_title}")
        for k, v in variants.items():
            print(f"   {k}: {v}")
        choice = input("선택 (기본/A/B/C): ").strip().upper()
        selected_title = variants.get(choice, default_title)
    elif title_choice and variants:
        selected_title = variants.get(title_choice.upper(), default_title)
    else:
        selected_title = default_title

    print(f"\n  제목: {selected_title}")

    # Thesis 가이드 로드
    thesis_ids = topic.get("thesis_ids", [])
    guide = load_thesis_guide(thesis_ids)

    # RAG 심층 검색 (옵션 활성화 시)
    rag_context = ""
    if use_rag:
        try:
            from rag_engine import search, format_rag_context
            query = f"{selected_title} {' '.join(thesis_ids)}"
            chunks = search(query, n_results=config.RAG_TOP_K)
            if chunks:
                print(f"  🔍 [RAG 활성화] 지식 DB에서 관련 리포트/자료 {len(chunks)}개 청크 검색 및 주입")
                rag_context = format_rag_context(chunks)
            else:
                print("  ℹ️ [RAG 활성화] 관련 리포트 청크 없음 (기본 모드로 진행)")
        except Exception as e:
            print(f"  ⚠️ RAG 검색 오류 (기본 모드로 대체): {e}")

    # 프롬프트 구성 + LLM 호출
    prompt = build_blog_prompt(topic, guide, selected_title, rag_context=rag_context)
    print(f"  🤖 블로그 생성 중... ({config.GEMINI_MODEL})")
    content = call_gemini(prompt)

    # 코드 블록 래퍼 제거
    content = re.sub(r"^```(?:markdown)?\n?", "", content.strip())
    content = re.sub(r"\n?```$", "", content.strip())

    # Critic 자가 검수 루프 (옵션 활성화 시)
    if use_critic:
        try:
            from critic import run_critic_loop
            content, _ = run_critic_loop(content)
        except Exception as e:
            print(f"  ⚠️ Critic 검수 오류 (초안 유지): {e}")

    # 미리보기
    preview_blog(content)

    if interactive:
        save_choice = input("저장하시겠습니까? (y/n/e=편집 후 저장): ").strip().lower()
        if save_choice == "n":
            print("  취소됨.")
            sys.exit(0)

    filepath = save_blog(content, selected_title)
    print(f"\n  ✅ 저장 완료: {filepath}")

    try:
        from obsidian_sync import sync_file
        sync_file(filepath, "blog")
    except Exception:
        pass

    try:
        from notifier import notify_content_generated
        notify_content_generated("Blog", selected_title, filepath, content[:150])
    except Exception as e:
        print(f"  (알림 발송 생략: {e})")

    return filepath


def main():
    parser = argparse.ArgumentParser(description="Argus Pulse — 블로그 생성기")
    grp = parser.add_mutually_exclusive_group(required=True)
    grp.add_argument("--topic",    type=str, help="주제 JSON 문자열 (topic_generator 출력)")
    grp.add_argument("--from-log", action="store_true", help="오늘의 topic 로그에서 선택")
    parser.add_argument("--rag",    action="store_true", help="증권사 리포트 및 지식 DB RAG 심층 검색 활용")
    parser.add_argument("--critic", action="store_true", help="Critic 에이전트 자가 품질 검수 및 자동 보완 실행")
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
        print(f"\n📋 오늘의 주제 ({log_path.name}):")
        for i, t in enumerate(topics, 1):
            print(f"  [{i}] {t['title']}")
        idx = int(input("번호 선택: ").strip()) - 1
        topic = topics[idx]
    else:
        topic = json.loads(args.topic)

    generate_blog(topic, interactive=not args.auto, use_rag=args.rag, use_critic=args.critic)


if __name__ == "__main__":
    main()
