"""
manual_news_injector.py
자동 크롤러가 놓친 고품질 뉴스/공시/전문가 인사이트를 수기로 입력하여
1) news.sqlite DB 적재, 2) 테제 모멘텀 및 지지/반박 근거 반영, 3) 옵시디언 자동 동기화를 일괄 수행하는 도구
"""

import sys
import os
import sqlite3
import argparse
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

import config
import thesis_loader
import obsidian_sync

NEWS_DB = config.NEWS_DB_PATH


def inject_manual_news(
    title: str,
    thesis_id: str,
    score: float = 75.0,
    source: str = "수기입력",
    nature: str = "supporting",  # supporting | counter | neutral
    snippet: str = "",
    url: str = "",
    company: str = "",
    confidence_delta: int = 0
):
    """수기 뉴스를 시스템 전반(DB, 테제 MD, 옵시디언)에 일괄 주입"""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%Y-%m-%d")

    # 1. 테제 유효성 검증
    target_thesis = thesis_loader.load_thesis_by_id(thesis_id)
    if not target_thesis:
        print(f"❌ [오류] 유효하지 않은 테제 ID입니다: {thesis_id}")
        return False

    real_tid = target_thesis["id"]
    thesis_title = target_thesis["title"]

    # 2. SQLite news DB에 수기 데이터 적재
    if NEWS_DB.exists():
        try:
            conn = sqlite3.connect(str(NEWS_DB))
            conn.execute("""
                INSERT INTO news (company, ticker, title, snippet, score, source, url, published, collected_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                company or target_thesis.get("related_companies", ["-"])[0],
                real_tid,
                f"[수기] {title}",
                snippet or f"수기 등록된 핵심 뉴스 (테제: {real_tid} {thesis_title})",
                score,
                f"MANUAL:{source}",
                url or "manual://entry",
                now_str,
                now_str
            ))
            conn.commit()
            conn.close()
            print(f"  💾 [news.sqlite] 수기 뉴스 DB 적재 완료 (Score: {score}점)")
        except Exception as e:
            print(f"  ⚠️ DB 적재 중 경고: {e}")

    # 3. 테제 MD 본문에 근거 텍스트 추가
    evidence_text = f"[{source}] {title}"
    if snippet:
        evidence_text += f" — {snippet}"
    if url:
        evidence_text += f" ([원문]({url}))"

    supporting_arg = evidence_text if nature == "supporting" else None
    counter_arg = evidence_text if nature == "counter" else None

    res = thesis_loader.append_thesis_evidence(
        real_tid,
        date_str=date_str,
        supporting=supporting_arg,
        counter=counter_arg
    )
    if res:
        print(f"  📝 [테제 MD 갱신] {real_tid} ({thesis_title}) 본문에 {nature.upper()} 근거 추가")

    # 4. 신뢰도(Confidence) 가감 반영 (선택)
    if confidence_delta != 0:
        current_conf = target_thesis.get("confidence", 50)
        new_conf = max(0, min(100, current_conf + confidence_delta))
        thesis_loader.update_thesis_confidence(real_tid, new_conf)
        print(f"  🎯 [신뢰도 조정] {real_tid}: {current_conf}% ➔ {new_conf}% (Delta: {confidence_delta:+d}p)")

    # 5. 모멘텀 랭킹 재계산 및 옵시디언 동기화
    thesis_loader.sync_thesis_ranks_to_files(days=2)
    obsidian_sync.sync_all_outputs()

    print(f"\n✨ [성공] 수기 뉴스가 테제 [{real_tid} {thesis_title}] 및 옵시디언 볼트에 완벽하게 반영되었습니다!")
    return True


def interactive_wizard():
    """터미널 대화형 입력 마법사"""
    print("═" * 70)
    print(" ✍️  Argus Pulse — 수기 뉴스 & 인사이트 주입 마법사 (Manual News Injector)")
    print("═" * 70)

    title = input("\n1. 뉴스 제목 또는 핵심 사건 (필수): ").strip()
    if not title:
        print("❌ 제목은 필수입니다.")
        return

    tid_input = input("2. 연관 테제 ID (예: T1-01, T2-07, T3-01): ").strip().upper()
    target_thesis = thesis_loader.load_thesis_by_id(tid_input)
    if not target_thesis:
        print(f"❌ 테제를 찾을 수 없습니다: {tid_input}")
        return
    print(f"   ➔ 대상 테제: [{target_thesis['id']} {target_thesis['title']}]")

    print("\n3. 가설 영향 성격:")
    print("   [1] 지지 근거 (Supporting - 가설 강화)")
    print("   [2] 반박/위험 근거 (Counter/Bear - 가설 훼손)")
    print("   [3] 중립 (Neutral)")
    n_choice = input("   선택 (기본: 1): ").strip() or "1"
    nature = "supporting" if n_choice == "1" else ("counter" if n_choice == "2" else "neutral")

    score_in = input("4. 중요도 점수 (1~100, 기본 80): ").strip() or "80"
    score = float(score_in)

    source = input("5. 정보 출처 (예: 디일렉, 텔레그램, 유료리포트, 오프라인세미나, 기본: 수기입력): ").strip() or "수기입력"
    snippet = input("6. 핵심 상세 요약 (선택): ").strip()
    url = input("7. 관련 URL (선택): ").strip()
    
    conf_in = input("8. 신뢰도(Confidence) 수동 조정 (예: +5, -10, 엔터 시 0): ").strip() or "0"
    conf_delta = int(conf_in)

    print("\n" + "─" * 70)
    print("🚀 수기 뉴스 주입 실행 중...")
    inject_manual_news(
        title=title,
        thesis_id=target_thesis["id"],
        score=score,
        source=source,
        nature=nature,
        snippet=snippet,
        url=url,
        confidence_delta=conf_delta
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Argus Pulse — 수기 뉴스 주입기")
    parser.add_argument("--title", type=str, help="뉴스 제목")
    parser.add_argument("--thesis", type=str, help="연관 테제 ID (예: T1-01, T2-07)")
    parser.add_argument("--score", type=float, default=80.0, help="중요도 점수 (1~100)")
    parser.add_argument("--source", type=str, default="수기입력", help="정보 출처")
    parser.add_argument("--nature", choices=["supporting", "counter", "neutral"], default="supporting", help="가설 영향 성격")
    parser.add_argument("--snippet", type=str, default="", help="상세 요약")
    parser.add_argument("--url", type=str, default="", help="기사 원문 URL")
    parser.add_argument("--delta", type=int, default=0, help="신뢰도 가감 점수 (예: +5, -10)")

    args = parser.parse_args()

    if args.title and args.thesis:
        inject_manual_news(
            title=args.title,
            thesis_id=args.thesis,
            score=args.score,
            source=args.source,
            nature=args.nature,
            snippet=args.snippet,
            url=args.url,
            confidence_delta=args.delta
        )
    else:
        interactive_wizard()
