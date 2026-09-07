"""
thesis_brief_writer.py — 1-Page 투자 메모 'Thesis Inflection Brief' 생성기

기능:
  - 2-Page 대중 블로그를 대체하는 실전 투자자 전용 1-Page 압축 액션 메모 자동 집필
  - 핵심 3섹션 구성:
      1. 팩트 체커: 지지(Bull) vs 훼손/리스크(Bear) 데이터 대조
      2. 밸류에이션 및 기업 실적 영향도
      3. 포트폴리오 액션 시그널 & 다음 주목 D-Day 이벤트
  - 옵시디언 볼트(obs_argus/argus/Review/) 자동 동기화 및 디스코드 알림

실행:
  python thesis_brief_writer.py --id T2-01          # 특정 Thesis 1-Page 메모 생성
  python thesis_brief_writer.py --inflection-only   # 최근 변곡점 발생 가설 자동 탐지 생성
"""

import argparse
import json
import re
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import config
from llm_client import call_llm
from notifier import notify_content_generated
from rag_engine import search as rag_search
from thesis_loader import (
    get_thesis_momentum_ranking,
    load_theses,
    load_thesis_by_id,
)

OUTPUT_BRIEF_DIR = config.OUTPUT_DIR / "brief"


def fetch_recent_facts_for_brief(keywords: list[str], days: int = 7) -> list[dict]:
    """최근 N일간 관련 고득점 뉴스 수집"""
    if not config.NEWS_DB_PATH.exists() or not keywords:
        return []

    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    conn = sqlite3.connect(config.NEWS_DB_PATH)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT company, title, snippet, score, published, url
        FROM news
        WHERE published >= ? OR collected_at >= ?
        ORDER BY score DESC
        LIMIT 60
    """, (since, since)).fetchall()
    conn.close()

    matched = []
    for r in rows:
        text = f"{r['title']} {r['snippet'] or ''}"
        if any(str(kw) in text for kw in keywords):
            matched.append(dict(r))
    return matched[:8]


def generate_brief_content(thesis: dict, news_items: list[dict], rag_chunks: list[dict]) -> str:
    """LLM을 통해 1-Page 액션 지향형 Thesis Inflection Brief 마크다운 생성"""
    tid = thesis["id"]
    title = thesis["title"]
    conf = thesis.get("confidence", 70)
    hypo = thesis.get("hypothesis", "")
    milestone = thesis.get("milestone", "(미지정)")
    m_status = thesis.get("milestone_status", "NONE")
    falsification = thesis.get("falsification_condition", "(미지정)")
    companies = ", ".join(thesis.get("related_companies", [])) or "관련 기업"

    news_text = "\n".join([
        f"- [{n.get('company','')}] {n['title']} (점수: {n['score']}점, 내용: {(n['snippet'] or '')[:100]})"
        for n in news_items
    ]) or "(최근 7일 관련 뉴스 없음)"

    rag_text = "\n".join([
        f"- [{c['metadata'].get('company','')} | {c['metadata'].get('broker','')}] {c['text'][:150]}..."
        for c in rag_chunks
    ]) or "(관련 증권사 리포트 청크 없음)"

    prompt = f"""당신은 글로벌 톱티어 헤지펀드의 시니어 테크 포트폴리오 매니저입니다.
아래 [투자 가설]과 최근 관측된 [뉴스 팩트], [증권사 분석 데이터]를 바탕으로,
투자심의위원회에 즉시 제출할 **'1-Page Thesis Inflection Brief (투자 의사결정 메모)'**를 작성하세요.

불필요한 서론, 수식어, 잡담을 완전히 배제하고, 철저히 **팩트 대조, 실적/밸류에이션 임팩트, 그리고 포트폴리오 액션(매수/매도/비중조절)**에 집중하세요.

[투자 가설 프로필]
- ID: {tid}
- 테제 명칭: {title}
- 핵심 가설: {hypo}
- 현재 신뢰도: {conf}%
- 마일스톤(Catalyst): {milestone} (현재 상태: {m_status})
- 기각 조건(Falsification): {falsification}
- 주요 밸류체인 기업: {companies}

[최근 관측 뉴스]
{news_text}

[증권사 리포트 핵심 청크]
{rag_text}

[작성 지침 및 구조]
1. 제목: `# 🎯 [Thesis Brief] {tid} {title}: 변곡점 및 가설 점검`
2. 한 줄 결론 (Executive Summary): `> **한 줄 결론**: ...` 형식으로 마일스톤 진척, 가설 유효성, 포트폴리오 액션 요약을 2문장 이내로 강력하게 압축.
3. `## 1. 팩트 체커: 가설 지지(Bull) vs 훼손/리스크(Bear) 데이터 대조`
   - ✅ **지지 팩트 (Bull)**: 가설을 강화하는 구체적 사실/수치 2~3개 불릿.
   - ⚠️ **훼손/리스크 (Bear)**: 가설을 위협하거나 감시해야 할 역풍/경쟁 팩트 1~2개 불릿.
4. `## 2. 밸류에이션 및 기업 실적 영향도 (Valuation & Financial Impact)`
   - 핵심 기업({companies})별 단기/중기 매출 및 마진(ASP, 영업이익률) 영향 분석.
5. `## 3. 포트폴리오 액션 시그널 & 다음 주목 D-Day 이벤트`
   - **투자 포지션 권고**: [비중 확대 (Overweight)] / [비중 유지 (Neutral)] / [비중 축소 (Underweight)] 중 택1 및 근거.
   - **차기 분수령 이벤트 (Catalyst D-Day)**: 실적 발표, 고객사 퀄 테스트, 신제품 런칭 등 투자자가 캘린더에 적어두어야 할 일정/이벤트.

마크다운 본문만 간결하고 명확하게 출력하세요."""

    return call_llm(prompt)


def write_thesis_brief(thesis: dict) -> Path:
    """단일 Thesis에 대한 1-Page 투자 메모 작성 및 저장/동기화"""
    tid = thesis["id"]
    title = thesis["title"]
    conf = thesis.get("confidence", 70)
    kws = thesis.get("keywords", [])

    print(f"\n📝 [{tid}] {title} 1-Page Thesis Inflection Brief 작성 중...")

    # 1. 팩트 및 RAG 데이터 조회
    news_items = fetch_recent_facts_for_brief(kws, days=7)
    rag_chunks = rag_search(f"{title} {thesis.get('hypothesis', '')}", n_results=3)

    # 2. 본문 생성
    body_md = generate_brief_content(thesis, news_items, rag_chunks)

    # 3. 파일 저장
    OUTPUT_BRIEF_DIR.mkdir(parents=True, exist_ok=True)
    today_str = datetime.now().strftime("%Y-%m-%d")
    slug = re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "-")
    filename = f"{today_str}-brief-{tid}-{slug}.md"
    filepath = OUTPUT_BRIEF_DIR / filename

    frontmatter = f"""---
title: "[Thesis Brief] {tid} {title} — 변곡점 및 가설 점검"
date: {today_str}
thesis_id: {tid}
confidence: {conf}%
status: action-ready
type: thesis-brief
tags:
  - thesis-brief
  - argus-pulse
  - investment-memo
  - {thesis.get('sector_id', 'T1')}
---

"""
    full_content = frontmatter + body_md.strip() + "\n"
    filepath.write_text(full_content, encoding="utf-8")
    print(f"  ✅ [작성 완료] {filepath.name}")

    # 4. 옵시디언 동기화 (Review 카테고리)
    try:
        from obsidian_sync import sync_file
        sync_file(filepath, "review")
    except Exception as e:
        print(f"  ⚠️ 옵시디언 동기화 오류: {e}")

    # 5. 디스코드 알림
    notify_content_generated(
        content_type="Thesis Brief",
        title=f"[{tid}] {title} 1-Page 투자 메모",
        filepath=filepath,
        summary=f"신뢰도 {conf}% | 핵심 마일스톤 및 가설 팩트 대조 완료"
    )

    return filepath


def main():
    parser = argparse.ArgumentParser(description="Argus Pulse — 차세대 1-Page 투자 메모 생성기")
    parser.add_argument("--id", type=str, help="특정 Thesis ID 지정 (예: T2-01)")
    parser.add_argument("--inflection-only", action="store_true", help="변곡점(마일스톤 달성, 기각, 신뢰도 급변) 테제 자동 선별")
    args = parser.parse_args()

    if args.id:
        t = load_thesis_by_id(args.id.upper())
        if not t:
            print(f"❌ Thesis를 찾을 수 없습니다: {args.id}")
            return
        write_thesis_brief(t)
    elif args.inflection_only:
        print("\n🔍 최근 변곡점 발생 테제 검색 중...")
        theses = load_theses(status_filter="active")
        # 마일스톤 달성, 기각, 또는 신뢰도 80% 이상 활성 가설 필터링
        inflection_candidates = [
            t for t in theses
            if t.get("milestone_status") in ("ACHIEVED", "PROGRESS")
            or t.get("falsification_triggered") is True
            or t.get("confidence", 0) >= 80
        ]
        if not inflection_candidates:
            print("  ℹ️ 현재 뚜렷한 변곡점 테제가 없어 모멘텀 1위 테제를 대상으로 작성합니다.")
            ranked = get_thesis_momentum_ranking(days=2, status_filter="active")
            inflection_candidates = ranked[:1] if ranked else theses[:1]

        for t in inflection_candidates[:2]:
            write_thesis_brief(t)
    else:
        # 기본 실행: 시장 모멘텀 상위 1개 테제 작성
        ranked = get_thesis_momentum_ranking(days=2, status_filter="active")
        target = ranked[0] if ranked else load_theses()[0]
        write_thesis_brief(target)


if __name__ == "__main__":
    main()
