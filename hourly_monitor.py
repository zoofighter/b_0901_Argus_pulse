"""
hourly_monitor.py — 매시간 뉴스 모니터링 및 고득점 감지기

기능:
  - b_0826 SQLite DB에서 최근 수집된 신규 뉴스 폴링
  - Thesis 키워드 기반 연관 테제 자동 매칭
  - 80점 이상 고득점 뉴스 감지 시 Discord/콘솔 즉시 알림 발송
  - 처리된 뉴스 ID 기록으로 중복 알림 방지

실행:
  python hourly_monitor.py --once       # 1회 즉시 실행 (크론용)
  python hourly_monitor.py --interval 60 # N분마다 주기적 반복 실행
"""

import argparse
import json
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path

import config
from notifier import notify_hot_news
from thesis_loader import get_active_keywords

STATE_FILE = config.LOG_DIR / "monitor_state.json"


def load_processed_ids() -> set[int]:
    """이미 알림을 발송하거나 처리한 뉴스 ID 로드"""
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            return set(data.get("processed_ids", []))
        except Exception:
            return set()
    return set()


def save_processed_ids(processed_ids: set[int]):
    """처리된 뉴스 ID 저장 (최근 5000개 유지)"""
    recent_ids = list(processed_ids)[-5000:]
    payload = {
        "last_run": datetime.now().isoformat(),
        "processed_ids": recent_ids
    }
    STATE_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_unprocessed_news(processed_ids: set[int], lookback_hours: int = 4) -> list[dict]:
    """DB에서 최근 N시간 내 수집된 미처리 뉴스 조회"""
    if not config.NEWS_DB_PATH.exists():
        print(f"  ⚠️  뉴스 DB를 찾을 수 없음: {config.NEWS_DB_PATH}")
        return []

    since = (datetime.now() - timedelta(hours=lookback_hours)).isoformat()
    conn = sqlite3.connect(config.NEWS_DB_PATH)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT id, company, ticker, title, snippet, score, source, published, collected_at
        FROM news
        WHERE (collected_at >= ? OR published >= date('now', '-1 day'))
        ORDER BY id DESC
        LIMIT 100
    """, (since,)).fetchall()
    conn.close()

    news_list = []
    for r in rows:
        d = dict(r)
        if d["id"] not in processed_ids:
            news_list.append(d)
    return news_list


def match_theses(title: str, snippet: str, keyword_map: dict) -> list[str]:
    """제목 및 요약문에서 연관 Thesis ID 추출"""
    text = f"{title} {snippet or ''}"
    matched = []
    for tid, keywords in keyword_map.items():
        if any(kw in text for kw in keywords):
            matched.append(tid)
    return matched


def run_monitor_cycle() -> int:
    """1회 모니터링 주기 실행. 새로 감지된 고득점 뉴스 수 반환"""
    print(f"\n🔍 [Hourly Monitor] 실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    processed_ids = load_processed_ids()
    unprocessed = fetch_unprocessed_news(processed_ids)
    print(f"  새로 확인된 뉴스: {len(unprocessed)}건")

    if not unprocessed:
        return 0

    kmap = get_active_keywords()
    hot_count = 0

    for news in unprocessed:
        nid = news["id"]
        score = news.get("score") or 0
        matched = match_theses(news.get("title", ""), news.get("snippet", ""), kmap)

        # 고득점(80점 이상) 뉴스 알림
        if score >= config.NEWS_HOT_THRESHOLD:
            notify_hot_news(news, matched)
            hot_count += 1
        elif matched and score >= 70:
            print(f"  📌 [관심] {news.get('company','')} ({score}점): {news.get('title','')[:40]}... → {matched}")

        processed_ids.add(nid)

    save_processed_ids(processed_ids)
    if hot_count > 0:
        print(f"  🔥 고득점 뉴스 {hot_count}건 알림 발송 완료")
    else:
        print("  ✓ 고득점(80점+) 뉴스 없음")

    return hot_count


def main():
    parser = argparse.ArgumentParser(description="Argus Pulse — 뉴스 모니터링 서비스")
    parser.add_argument("--once", action="store_true", help="1회만 실행하고 종료 (기본)")
    parser.add_argument("--interval", type=int, default=0, help="지정된 분 단위로 주기적 실행 (예: 60)")
    args = parser.parse_args()

    if args.interval > 0:
        print(f"🚀 Argus Pulse Hourly Monitor 시작 ({args.interval}분 주기)")
        try:
            while True:
                run_monitor_cycle()
                time.sleep(args.interval * 60)
        except KeyboardInterrupt:
            print("\n모니터링 종료")
    else:
        run_monitor_cycle()


if __name__ == "__main__":
    main()
