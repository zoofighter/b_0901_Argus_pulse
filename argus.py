"""
argus.py — Argus Pulse 통합 제어 센터 (CLI & 대화형 콘솔)

실행:
  python argus.py              # 대화형 대시보드 메뉴 실행
  python argus.py --topic      # 아침 주제 추천 (뉴스 DB 자동)
  python argus.py --raw        # 99.raw 수동 자료 분석
  python argus.py --monitor    # 매시간 뉴스 감시 1회 실행
  python argus.py --digest     # 데일리 다이제스트 생성
  python argus.py --review     # 과거 블로그 검증 리뷰 생성
  python argus.py --sync       # 옵시디언 전체 동기화
  python argus.py --schedule   # 백그라운드 스케줄러 실행
"""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import config

BANNER = """
======================================================================
                  🦅 Argus Pulse — 통합 제어 센터
======================================================================
  환경: LLM={llm} | 볼트={vault}
======================================================================
  [1] 🌅 아침 주제 추천 (DB 핫뉴스 → 블로그/스레드 기획)
  [2] 📂 수동 자료 분석 (99.raw 폴더 자료 → 기획 → 아카이빙)
  [3] 🔍 실시간 뉴스 모니터링 (1회 즉시 감시 & 80점+ 알림)
  [4] 📊 데일리 다이제스트 (하루 전체 테제별 동향 요약)
  [5] 🔄 과거 블로그 검증 리뷰 (Thesis 장기 추적 & 사후 검증)
  [6] 📓 옵시디언 볼트 전체 동기화 (Output -> Obsidian)
  [7] ⏰ 스케줄러 실행 (08시 추천 / 매시간 감시 / 21시 다이제스트+점검)
  [8] 📋 Crontab 자동화 설정 가이드 확인
  [9] 🧠 Thesis 가설 신뢰도 자동 점검 (thesis_checker.py)
  [10] 📚 RAG 지식 DB 상태 및 인제스트 (ingest.py)
  [11] 🔥 시장 모멘텀(News Momentum) Thesis 랭킹 조회
  [12] 📝 수기 뉴스 등록 (add_news.py — 자동 수집 누락 기사 주입)
  [13] 🌱 신규 테마 발굴기 (theme_discoverer.py — 미매칭 고득점 뉴스 마이닝)
  [14] 🎯 1-Page 투자 메모 생성 (thesis_brief_writer.py — 변곡점 브리프)
  ──────────────────────────────────────────────────────────────────
  [q] 종료
======================================================================
"""


CRONTAB_SAMPLE = f"""# ── Argus Pulse Crontab 스케줄 ─────────────────────────────
# 08:00 아침 주제 추천 & 신규 테마 발굴
0 8 * * * cd {config.ROOT_DIR} && {sys.executable} topic_generator.py --auto >> logs/cron_topic.log 2>&1
5 8 * * * cd {config.ROOT_DIR} && {sys.executable} theme_discoverer.py >> logs/cron_theme.log 2>&1

# 09:00~21:00 매시간 뉴스 모니터링 (80점 이상 즉시 알림)
0 9-21 * * * cd {config.ROOT_DIR} && {sys.executable} hourly_monitor.py --once >> logs/cron_monitor.log 2>&1

# 13:00 오후 블로그 사후 검증 리뷰 & 1-Page 투자 메모 (변곡점 발생 시)
0 13 * * * cd {config.ROOT_DIR} && {sys.executable} review_generator.py --rag >> logs/cron_review.log 2>&1
5 13 * * * cd {config.ROOT_DIR} && {sys.executable} thesis_brief_writer.py --inflection-only >> logs/cron_brief.log 2>&1

# 21:00 데일리 다이제스트 생성 (RAG 연동) 및 옵시디언 동기화
0 21 * * * cd {config.ROOT_DIR} && {sys.executable} daily_digest.py --rag >> logs/cron_digest.log 2>&1

# 21:05 시장 모멘텀 상위 Thesis 가설 신뢰도 스마트 자동 점검 및 마일스톤 감시
5 21 * * * cd {config.ROOT_DIR} && {sys.executable} thesis_checker.py --smart >> logs/cron_checker.log 2>&1
# ───────────────────────────────────────────────────────────"""


def run_cmd(args_list: list[str]):
    """파이썬 서브프로세스 실행"""
    cmd = [sys.executable] + args_list
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n  중단되었습니다.")
    except subprocess.CalledProcessError as e:
        print(f"\n  ❌ 실행 실패 (code {e.returncode})")


def show_crontab_guide():
    print("\n📋 [Crontab 자동화 설정 안내]")
    print("터미널에서 `crontab -e` 명령어를 입력하고 아래 내용을 붙여넣으세요:\n")
    print(CRONTAB_SAMPLE)
    print(f"\n설정 파일이 '{config.ROOT_DIR / 'crontab.txt'}'에도 저장되어 있습니다.\n")
    (config.ROOT_DIR / "crontab.txt").write_text(CRONTAB_SAMPLE, encoding="utf-8")


def interactive_menu():
    while True:
        vault_name = Path(config.OBSIDIAN_VAULT_PATH).name if config.OBSIDIAN_VAULT_PATH else "미설정"
        print(BANNER.format(llm=config.GEMINI_MODEL, vault=vault_name))
        choice = input("선택 번호 입력 [1~14, q]: ").strip().lower()

        if choice in ("q", "quit", "exit"):
            print("\n🦅 Argus Pulse를 종료합니다. 좋은 하루 되세요!\n")
            break
        elif choice == "1":
            run_cmd(["topic_generator.py", "--auto"])
        elif choice == "2":
            run_cmd(["topic_generator.py", "--raw"])
        elif choice == "3":
            run_cmd(["hourly_monitor.py", "--once"])
        elif choice == "4":
            rag = input("증권사 리포트 RAG 심층 모드를 사용할까요? (y/n, 기본 y): ").strip().lower()
            args = ["daily_digest.py"]
            if rag in ("y", ""):
                args.append("--rag")
            run_cmd(args)
        elif choice == "5":
            rag = input("증권사 리포트 RAG 심층 모드를 사용할까요? (y/n, 기본 y): ").strip().lower()
            args = ["review_generator.py"]
            if rag in ("y", ""):
                args.append("--rag")
            run_cmd(args)
        elif choice == "6":
            run_cmd(["obsidian_sync.py", "--all"])
        elif choice == "7":
            run_cmd(["scheduler.py"])
        elif choice == "8":
            show_crontab_guide()
        elif choice == "9":
            run_cmd(["thesis_checker.py"])
        elif choice == "10":
            run_cmd(["ingest.py", "--status"])
        elif choice == "11":
            run_cmd(["thesis_loader.py", "--rank"])
        elif choice == "12":
            run_cmd(["add_news.py"])
        elif choice == "13":
            run_cmd(["theme_discoverer.py"])
        elif choice == "14":
            tid = input("투자 메모를 작성할 Thesis ID (입력 안하면 변곡점 발생 테제 자동 대상): ").strip().upper()
            if tid:
                run_cmd(["thesis_brief_writer.py", "--id", tid])
            else:
                run_cmd(["thesis_brief_writer.py", "--inflection-only"])
        else:
            print("  ⚠️ 올바른 번호를 선택해주세요.")
        
        input("\n[Enter]를 누르면 메뉴로 돌아갑니다...")


def main():
    parser = argparse.ArgumentParser(description="Argus Pulse — 통합 제어 센터")
    parser.add_argument("--topic",    action="store_true", help="아침 주제 추천")
    parser.add_argument("--raw",      action="store_true", help="99.raw 자료 기반 주제 추천")
    parser.add_argument("--monitor",  action="store_true", help="실시간 뉴스 모니터링 1회 실행")
    parser.add_argument("--digest",   action="store_true", help="데일리 다이제스트 생성")
    parser.add_argument("--review",   action="store_true", help="과거 블로그 검증 리뷰 생성")
    parser.add_argument("--sync",     action="store_true", help="옵시디언 전체 동기화")
    parser.add_argument("--schedule", action="store_true", help="스케줄러 시작")
    parser.add_argument("--crontab",  action="store_true", help="크론탭 가이드 출력")
    parser.add_argument("--checker",  action="store_true", help="Thesis 가설 신뢰도 자동 점검")
    parser.add_argument("--ingest",   action="store_true", help="RAG 지식 DB 인제스트 현황 확인")
    parser.add_argument("--rank",     action="store_true", help="시장 모멘텀(News Momentum) Thesis 랭킹 조회")
    parser.add_argument("--add-news", action="store_true", help="수기 뉴스 직접 등록 (news.sqlite)")
    parser.add_argument("--discover", action="store_true", help="미매칭 뉴스 기반 신규 테마 발굴")
    parser.add_argument("--brief",    type=str, nargs="?", const="inflection", help="1-Page 투자 메모 생성 (ID 지정 가능)")
    parser.add_argument("--rag",      action="store_true", help="RAG 심층 검색 활성화")
    args = parser.parse_args()

    if args.topic:
        run_cmd(["topic_generator.py", "--auto"])
    elif args.raw:
        run_cmd(["topic_generator.py", "--raw"])
    elif args.monitor:
        run_cmd(["hourly_monitor.py", "--once"])
    elif args.discover:
        run_cmd(["theme_discoverer.py"])
    elif args.brief:
        if args.brief == "inflection":
            run_cmd(["thesis_brief_writer.py", "--inflection-only"])
        else:
            run_cmd(["thesis_brief_writer.py", "--id", args.brief])
    elif args.digest:
        cmd = ["daily_digest.py"]
        if args.rag:
            cmd.append("--rag")
        run_cmd(cmd)
    elif args.review:
        cmd = ["review_generator.py"]
        if args.rag:
            cmd.append("--rag")
        run_cmd(cmd)
    elif args.sync:
        run_cmd(["obsidian_sync.py", "--all"])
    elif args.schedule:
        run_cmd(["scheduler.py"])
    elif args.crontab:
        show_crontab_guide()
    elif args.checker:
        run_cmd(["thesis_checker.py"])
    elif args.ingest:
        run_cmd(["ingest.py", "--status"])
    elif args.rank:
        run_cmd(["thesis_loader.py", "--rank"])
    elif args.add_news:
        run_cmd(["add_news.py"])
    else:
        interactive_menu()


if __name__ == "__main__":
    main()

