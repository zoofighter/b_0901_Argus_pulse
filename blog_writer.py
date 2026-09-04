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


# ── 뉴스 원문 및 링크 로드 ───────────────────────────────────────────────────

def fetch_related_news(thesis_ids: list[str], title: str = "", limit: int = 5) -> list[dict]:
    """DB에서 관련 고득점 뉴스 및 실제 URL 조회"""
    if not config.NEWS_DB_PATH.exists():
        return []
    import sqlite3
    from datetime import timedelta
    conn = sqlite3.connect(config.NEWS_DB_PATH)
    conn.row_factory = sqlite3.Row

    keywords = []
    for tid in thesis_ids:
        t = load_thesis_by_id(tid)
        if t:
            keywords.extend(t.get("keywords", []))

    since = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")

    rows = conn.execute("""
        SELECT id, company, title, url, source, score, published
        FROM news
        WHERE published >= ? OR collected_at >= ?
        ORDER BY score DESC, id DESC
        LIMIT 100
    """, (since, since)).fetchall()
    conn.close()

    results = []
    for r in rows:
        d = dict(r)
        t_text = f"{d.get('company','')} {d.get('title','')}"
        if any(kw in t_text for kw in keywords) or any(w in t_text for w in title.split() if len(w) >= 2):
            results.append(d)
        if len(results) >= limit:
            break

    if len(results) < limit:
        for r in rows:
            d = dict(r)
            if d not in results:
                results.append(d)
            if len(results) >= limit:
                break

    return results


def format_news_references(news_list: list[dict]) -> str:
    """LLM 프롬프트에 주입할 뉴스 및 원문 URL 목록"""
    if not news_list:
        return ""
    lines = [
        "────────────────────────────────────────────────────────────",
        "📰 [관련 뉴스 기사 및 공식 웹 출처 원문 링크]",
        "참고 자료 및 출처 섹션에 아래 실제 기사 제목과 URL을 반드시 마크다운 링크 형태로 표기하세요.",
        "────────────────────────────────────────────────────────────"
    ]
    for n in news_list:
        comp = n.get("company") or n.get("source") or "뉴스"
        title = n.get("title", "")
        url = n.get("url", "")
        pub = n.get("published", "")
        score = n.get("score", 0)
        lines.append(f"- [{comp}] {title} ({pub}, 점수:{score})\n  원문 링크: {url}")
    return "\n".join(lines)


# ── 프롬프트 구성 ──────────────────────────────────────────────────────────────

def build_blog_prompt(topic: dict, thesis_guide: str, selected_title: str, rag_context: str = "", news_context: str = "", user_feedback: str = "") -> str:
    outline = topic.get("outline", {})
    outline_str = "\n".join([f"  - {k}: {v}" for k, v in outline.items()])
    today = date.today().isoformat()

    rag_section = f"\n\n[증권사 리포트 및 심층 데이터]\n{rag_context}\n" if rag_context else ""
    news_section = f"\n\n[뉴스 및 웹 원문 출처 데이터]\n{news_context}\n" if news_context else ""
    feedback_section = f"\n\n[사용자 특별 지침 및 윤곽 수정 사항]\n{user_feedback}\n위 지침을 반드시 본론 및 논점 전개에 최우선 반영하세요.\n" if user_feedback else ""

    return f"""당신은 테크/투자 전문 블로그 작가입니다.
아래 [기획안]을 바탕으로 [양식]에 맞는 블로그 초안을 작성하세요.

[기획안]
- 제목: {selected_title}
- 관점(Angle): {topic.get('angle', '')}
- 관련 Thesis: {', '.join(topic.get('thesis_ids', []))}
- 핵심 훅: {topic.get('hook', '')}
- 목차:
{outline_str}
{feedback_section}
[Thesis 작성 가이드]
{thesis_guide if thesis_guide else '(가이드 없음 — 기획안 기반으로 작성)'}{rag_section}{news_section}

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

### 📰 핵심 뉴스 및 웹 출처
- [기사 제목](실제 URL) — 언론사/출처 (날짜)
(반드시 위 [뉴스 및 웹 원문 출처 데이터]에 기재된 실제 기사 제목과 원문 URL을 마크다운 링크 형식으로 빠짐없이 기재)

### 📊 증권사 리포트 & 데이터
- 발행기관, 리포트명 (날짜)

### 🔗 연관 투자 테제
- [[관련 Thesis ID 및 제목]]
```

[작성 시 자기 검토 후 제출]
✅ 본론에 마크다운 비교 표(Table)가 1개 이상 포함되었는가?
✅ 문단 첫 머리에 핵심 문장이 볼드로 강조되었는가?
✅ 기본 금융 용어(CAPEX, ROIC 등)의 불필요한 괄호 설명이 생략되고 템포가 빠른가?
✅ 결론에 3대 인사이트와 다음 주목 이벤트가 있는가?
✅ 문서 하단 [참고 자료 및 출처(References)] 섹션에 실제 뉴스 원문 URL 링크([제목](URL))가 명확히 기재되었는가?
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


def save_outline_file(topic: dict, title: str) -> Path:
    """1-Page 기획 윤곽서 파일(output/outline/YYYY-MM-DD-outline-{slug}.md) 저장"""
    today = date.today().isoformat()
    slug = make_slug(title)
    outline_dir = config.OUTPUT_DIR / "outline"
    outline_dir.mkdir(parents=True, exist_ok=True)
    base = outline_dir / f"{today}-outline-{slug}"

    filepath = Path(f"{base}.md")
    i = 1
    while filepath.exists():
        filepath = Path(f"{base}-{i}.md")
        i += 1

    outline = topic.get("outline", {})
    variants = topic.get("title_variants", {})
    thesis_ids = topic.get("thesis_ids", [])

    # 관련 뉴스 원문 링크 조회
    related_news = fetch_related_news(thesis_ids, title, limit=4)
    news_links_lines = []
    if related_news:
        for n in related_news:
            comp = n.get("company") or n.get("source") or "뉴스"
            news_links_lines.append(f"- [{comp}] [{n.get('title')}]({n.get('url')}) ({n.get('published')}, {n.get('score')}점)")
    news_section = "\n".join(news_links_lines) if news_links_lines else "- (관련 뉴스 링크 없음)"

    content = f"""---
title: "{title}"
date: {today}
type: outline
thesis: {json.dumps(topic.get('thesis_ids', []), ensure_ascii=False)}
angle: "{topic.get('angle', '')}"
status: draft
---

# 🗺️ 블로그 기획 윤곽서 (Outline Blueprint)

> **주제**: {title}  
> **핵심 훅**: {topic.get('hook', '')}  
> **관점(Angle)**: {topic.get('angle', '')}  
> **연계 테제**: {', '.join(topic.get('thesis_ids', []))}

---

## 1. 제목 후보 3종
- **A (직관형)**: {variants.get('A', '')}
- **B (의문형)**: {variants.get('B', '')}
- **C (스토리)**: {variants.get('C', '')}

---

## 2. 4단계 목차 및 핵심 논점 구상
- **서론**: {outline.get('서론', '')}
- **본론 1**: {outline.get('본론1', '')}
- **본론 2 (반론/검증)**: {outline.get('본론2', '')}
- **결론 (투자 뷰 & 이벤트)**: {outline.get('결론', '')}

---

## 3. 집필 체크포인트
- [ ] 본론 내 비교 표(Table) 구상 (기업/기술 대조)
- [ ] 핵심 수치 데이터 박스 배치
- [ ] 증권사 리포트 / 공식 출처 각주 확보

---

## 4. 📰 핵심 뉴스 및 원문 링크
{news_section}
"""
    filepath.write_text(content, encoding="utf-8")

    try:
        from obsidian_sync import sync_file
        sync_file(filepath, "outline")
    except Exception:
        pass

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

def generate_blog(topic: dict, title_choice: str = None, interactive: bool = True, use_rag: bool = False, use_critic: bool = False, outline_only: bool = False) -> Path:
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

    # ── 윤곽(Outline) 사전 확인 및 편집 루프 (Human-in-the-Loop) ──
    user_feedback = ""
    outline = topic.get("outline", {})

    if outline_only:
        filepath = save_outline_file(topic, selected_title)
        print(f"\n  💾 기획 윤곽서 저장 완료: {filepath}")
        return filepath

    if interactive and outline:
        print("\n" + "━" * 60)
        print("🗺️  [블로그 작성 전 윤곽(Outline) 사전 확인]")
        print("━" * 60)
        print(f"📌 주제: {selected_title}")
        print(f"🎯 관점: {topic.get('angle', '')} | 훅: {topic.get('hook', '')}")
        print("\n[예정된 4단계 목차 구성]")
        for k, v in outline.items():
            print(f"  • {k}: {v}")
        print("━" * 60)
        print("옵션 선택:")
        print("  [Enter] / y : 위 윤곽 그대로 본문 작성 진행")
        print("  e           : 윤곽 수정 및 추가 요청사항 입력 후 작성")
        print("  o           : 윤곽(기획서)만 마크다운 파일로 저장 후 종료")
        print("  n           : 취소")
        action = input("선택 → ").strip().lower()

        if action == "n":
            print("  취소되었습니다.")
            sys.exit(0)
        elif action == "o":
            filepath = save_outline_file(topic, selected_title)
            print(f"\n  💾 기획 윤곽서 저장 완료: {filepath}")
            return filepath
        elif action == "e":
            print("\n✏️  추가하거나 강조하고 싶은 논점, 수정 사항을 입력하세요:")
            user_feedback = input("피드백 → ").strip()
            print(f"  💡 지침 반영: '{user_feedback}'")

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

    # 관련 뉴스 원문 및 링크 조회
    # 관련 뉴스 및 원문 링크 조회
    related_news = fetch_related_news(thesis_ids, selected_title, limit=5)
    news_context = format_news_references(related_news)
    if related_news:
        print(f"  📰 관련 뉴스 원문 링크 {len(related_news)}건 확보 및 프롬프트 주입")

    # 프롬프트 구성 + LLM 호출
    prompt = build_blog_prompt(
        topic, guide, selected_title,
        rag_context=rag_context,
        news_context=news_context,
        user_feedback=user_feedback
    )
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
    parser.add_argument("--index",   type=int, default=None, help="주제 번호 (1부터 시작)")
    parser.add_argument("--outline", action="store_true", help="본문 작성 없이 1-Page 기획 윤곽서(Blueprint)만 생성")
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

        if args.index:
            idx = args.index - 1
        elif args.auto or not sys.stdin.isatty():
            idx = 0
            print(f"  자동 선택 (1순위): {topics[idx]['title']}")
        else:
            idx = int(input("번호 선택: ").strip()) - 1
        topic = topics[idx]
    else:
        topic = json.loads(args.topic)

    generate_blog(topic, interactive=not args.auto, use_rag=args.rag, use_critic=args.critic, outline_only=args.outline)


if __name__ == "__main__":
    main()
