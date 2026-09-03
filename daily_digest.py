"""
daily_digest.py — 일일 뉴스 종합 및 Thesis별 다이제스트 생성기

실행:
  python daily_digest.py              # 오늘 일자 다이제스트 생성
  python daily_digest.py --days 1     # 최근 N일치 데이터 기준 생성

기능:
  - 최근 24시간 뉴스를 Thesis별로 매칭 및 점수 집계
  - 가장 뜨거웠던 테제 Top 5 및 핵심 뉴스 선별
  - Gemini를 통한 테제별 일일 인사이트 요약 생성
  - output/digest/YYYY-MM-DD-digest.md 저장
"""

import argparse
import json
import re
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

import config
from notifier import send_discord
from thesis_loader import get_active_keywords, load_thesis_by_id


def fetch_daily_news(days: int = 1) -> list[dict]:
    """최근 N일간의 뉴스 전체 조회"""
    if not config.NEWS_DB_PATH.exists():
        return []

    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    conn = sqlite3.connect(config.NEWS_DB_PATH)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT company, ticker, title, snippet, score, source, published, collected_at
        FROM news
        WHERE published >= ? OR collected_at >= ?
        ORDER BY score DESC
    """, (since, since)).fetchall()
    conn.close()

    return [dict(r) for r in rows]


def group_news_by_thesis(news_list: list[dict], kmap: dict) -> dict:
    """뉴스를 연관된 Thesis별로 그룹핑"""
    grouped = {}
    for news in news_list:
        title = news.get("title", "")
        snippet = news.get("snippet", "")
        text = f"{title} {snippet}"

        matched_theses = []
        for tid, keywords in kmap.items():
            if any(kw in text for kw in keywords):
                matched_theses.append(tid)

        for tid in matched_theses:
            if tid not in grouped:
                grouped[tid] = []
            grouped[tid].append(news)

    return grouped


def build_digest_prompt(date_str: str, top_theses_summary: str, rag_context: str = "") -> str:
    rag_section = f"\n\n[증권사 리포트 및 지식 DB 심층 참조]\n{rag_context}\n" if rag_context else ""

    return f"""당신은 테크/투자 리서치 랩의 시니어 애널리스트입니다.
아래 [오늘의 Thesis별 뉴스 데이터]를 바탕으로, 투자자를 위한 깔끔하고 명료한 [일일 다이제스트]를 마크다운 형식으로 작성하세요.

[기준일] {date_str}

[Thesis별 핵심 뉴스 데이터]
{top_theses_summary[:3500]}{rag_section}

[작성 가이드라인]
1. 최상단에 오늘 테크/반도체/AI 시장을 관통한 핵심 테마 3가지를 한 줄씩 요약
2. 주요 테제별로:
   - 오늘의 상황 판단 (호재/악재/중립)
   - 가장 중요한 팩트 및 수치 (증권사 리포트 데이터 포함 시 적극 인용)
   - 애널리스트 한 줄 뷰
3. 마지막에 '내일 시장에서 확인해야 할 포인트' 제시
4. 담백하고 통찰력 있는 어조 유지 (~함, ~음 또는 정중한 경어체)

마크다운 형식으로 바로 작성하세요."""


from llm_client import call_llm

def call_gemini(prompt: str) -> str:
    """통합 LLM 호출 (Gemini 우선, 실패 시 OpenCode 대체)"""
    return call_llm(prompt)


def generate_daily_digest(days: int = 1, use_rag: bool = False) -> Path:
    today_str = date.today().isoformat()
    print(f"\n📊 [Daily Digest] {today_str} 보고서 생성 시작")

    news_list = fetch_daily_news(days=days)
    print(f"  조회된 뉴스: {len(news_list)}건")

    if not news_list:
        print("  ⚠️  최근 뉴스가 없어 다이제스트 생성을 건너뜁니다.")
        return None

    kmap = get_active_keywords()
    grouped = group_news_by_thesis(news_list, kmap)

    # 뉴스 건수 및 최고점 기준 상위 Thesis 정렬
    ranked_theses = sorted(
        grouped.keys(),
        key=lambda tid: (len(grouped[tid]), max(n.get("score", 0) for n in grouped[tid])),
        reverse=True
    )[:6]

    print(f"  상위 주목 Thesis ({len(ranked_theses)}개): {', '.join(ranked_theses)}")

    summary_lines = []
    for tid in ranked_theses:
        t_info = load_thesis_by_id(tid)
        t_title = t_info["title"] if t_info else tid
        items = grouped[tid][:4]  # 상위 4개 뉴스만 발췌
        summary_lines.append(f"\n### [{tid}] {t_title} (관련 뉴스 {len(grouped[tid])}건)")
        for item in items:
            summary_lines.append(f"- [{item.get('company','')}] {item.get('title','')} (점수: {item.get('score',0)})")

    top_summary_text = "\n".join(summary_lines)

    # RAG 심층 검색 (옵션 활성화 시)
    rag_context = ""
    if use_rag:
        try:
            from rag_engine import search, format_rag_context
            query = f"{' '.join(ranked_theses)} 반도체 데이터센터 실적 가이던스"
            chunks = search(query, n_results=config.RAG_TOP_K)
            if chunks:
                print(f"  🔍 [RAG 활성화] 지식 DB에서 관련 리포트 {len(chunks)}개 청크 검색 및 주입")
                rag_context = format_rag_context(chunks)
            else:
                print("  ℹ️ [RAG 활성화] 관련 리포트 청크 없음 (기본 모드로 진행)")
        except Exception as e:
            print(f"  ⚠️ RAG 검색 오류 (기본 모드로 대체): {e}")

    prompt = build_digest_prompt(today_str, top_summary_text, rag_context=rag_context)
    print("  🤖 Gemini로 일일 다이제스트 작성 중...")
    content = call_gemini(prompt)

    # 정리 및 프론트매터 결합
    content = re.sub(r"^```(?:markdown)?\n?", "", content.strip())
    content = re.sub(r"\n?```$", "", content.strip())

    header = f"""---
title: "Argus Pulse 일일 다이제스트 ({today_str})"
date: {today_str}
type: digest
top_theses: {json.dumps(ranked_theses, ensure_ascii=False)}
news_count: {len(news_list)}
rag_enhanced: {str(use_rag).lower()}
---

# 🌐 Argus Pulse 데일리 인텔리전스 ({today_str})

"""
    full_doc = header + content

    digest_dir = config.OUTPUT_DIR / "digest"
    digest_dir.mkdir(parents=True, exist_ok=True)
    out_file = digest_dir / f"{today_str}-digest.md"
    out_file.write_text(full_doc, encoding="utf-8")
    print(f"  ✅ 다이제스트 저장 완료: {out_file}")

    try:
        from obsidian_sync import sync_file
        sync_file(out_file, "digest")
    except Exception:
        pass

    # 디스코드 알림
    send_discord(
        message=f"📰 **Argus Pulse 데일리 다이제스트 ({today_str})** 생성이 완료되었습니다!\n주목 테제: `{', '.join(ranked_theses)}`"
    )

    return out_file


def main():
    parser = argparse.ArgumentParser(description="Argus Pulse 데일리 다이제스트")
    parser.add_argument("--days", type=int, default=1, help="분석 기간 (일 단위)")
    parser.add_argument("--rag",  action="store_true", help="증권사 리포트 및 지식 DB RAG 심층 검색 활용")
    args = parser.parse_args()
    generate_daily_digest(days=args.days, use_rag=args.rag)


if __name__ == "__main__":
    main()
