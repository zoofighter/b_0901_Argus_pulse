"""
add_news.py — 수기 뉴스 등록 유틸리티

자동 수집기가 놓쳤거나 긴급하게 분석해야 하는 뉴스를 news.sqlite에 직접 등록합니다.
등록 즉시 Argus Pulse의 모든 모듈(hourly_monitor, topic_generator, thesis_checker, daily_digest)이
동일하게 인식하고 모멘텀 점수와 테제 매칭에 반영합니다.

사용법:
  python add_news.py                                    # 대화형 입력 모드
  python add_news.py --title "..." --company "..."      # CLI 인자 직접 입력
"""

import argparse
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import config
from thesis_loader import get_active_keywords
from topic_generator import match_thesis_to_context


def insert_news(title: str, company: str, snippet: str = "", url: str = "", score: int = 80, source: str = "수기입력", ticker: str = "") -> int:
    """news.sqlite 데이터베이스에 뉴스 1건 수기 등록"""
    if not config.NEWS_DB_PATH.exists():
        print(f"❌ 뉴스 DB 경로 없음: {config.NEWS_DB_PATH}")
        sys.exit(1)

    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    now_iso = now.isoformat()

    if not url:
        url = f"manual://{today_str}/{int(now.timestamp())}"

    conn = sqlite3.connect(config.NEWS_DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO news (url, title, snippet, source, company, ticker, query, score, published, collected_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (url, title, snippet, source, company, ticker, "manual", score, today_str, now_iso))

    news_id = cur.lastrowid
    conn.commit()
    conn.close()

    return news_id


def interactive_mode():
    print("\n" + "=" * 60)
    print("📝 Argus Pulse — 수기 뉴스 등록기 (Manual News Ingestion)")
    print("=" * 60)
    print("자동 크롤러가 놓친 중요한 뉴스를 DB에 직접 주입합니다.\n")

    title = input("1. 기사 제목 (필수): ").strip()
    if not title:
        print("❌ 제목은 필수입니다. 취소되었습니다.")
        return

    company = input("2. 대상 기업/섹터 (예: 삼성전자, SK하이닉스, TSMC) [기본: 시장]: ").strip() or "시장"
    score_str = input("3. 임팩트 점수 (0~100) [기본: 80]: ").strip() or "80"
    try:
        score = int(score_str)
    except ValueError:
        score = 80

    url = input("4. 기사 원문 URL (선택, 엔터 시 자동생성): ").strip()
    source = input("5. 언론사/출처 (예: 한국경제, Bloomberg) [기본: 수기입력]: ").strip() or "수기입력"
    print("6. 기사 핵심 본문/요약 (엔터 후 완료 시 EOF or 빈 줄 입력):")
    snippet = input("   요약: ").strip()

    news_id = insert_news(title=title, company=company, snippet=snippet, url=url, score=score, source=source)
    print(f"\n✅ 뉴스 DB 등록 완료! [ID: {news_id}, 점수: {score}점, 기업: {company}]")

    # 테제 매칭 테스트
    kmap = get_active_keywords()
    text = f"{title} {snippet} {company}"
    matched = match_thesis_to_context(text, kmap, top_n=5)
    if matched:
        print(f"📊 실시간 매칭된 투자 테제: {', '.join(matched)}")
    else:
        print("ℹ️ 기존 41개 테제 키워드와 매칭되지 않음 (미매칭 풀 분류)")

    # 즉시 기획 연동 여부
    print("-" * 60)
    gen_choice = input("🚀 지금 바로 이 뉴스로 주제 추천 및 블로그 기획을 진행할까요? (y/n, 기본 y): ").strip().lower()
    if gen_choice in ("y", ""):
        import subprocess
        cmd = [sys.executable, "topic_generator.py", "--text", f"[{company}] {title}\n{snippet}"]
        subprocess.run(cmd)


def main():
    parser = argparse.ArgumentParser(description="Argus Pulse — 수기 뉴스 등록")
    parser.add_argument("--title",   type=str, help="기사 제목")
    parser.add_argument("--company", type=str, default="시장", help="관련 기업")
    parser.add_argument("--snippet", type=str, default="", help="기사 요약/본문")
    parser.add_argument("--url",     type=str, default="", help="기사 원문 URL")
    parser.add_argument("--score",   type=int, default=80, help="임팩트 점수 (기본 80)")
    parser.add_argument("--source",  type=str, default="수기입력", help="언론사/출처")
    args = parser.parse_args()

    if not args.title:
        interactive_mode()
    else:
        news_id = insert_news(
            title=args.title,
            company=args.company,
            snippet=args.snippet,
            url=args.url,
            score=args.score,
            source=args.source
        )
        print(f"✅ 뉴스 DB 등록 완료 [ID: {news_id}, {args.score}점] {args.company} - {args.title}")


if __name__ == "__main__":
    main()
