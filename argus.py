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
  ──────────────────────────────────────────────────────────────────
  [q] 종료
======================================================================
"""

CRONTAB_SAMPLE = f"""# ── Argus Pulse Crontab 스케줄 ─────────────────────────────
# 08:00 아침 주제 추천 (알림 발송)
0 8 * * * cd {config.ROOT_DIR} && {sys.executable} topic_generator.py --auto >> logs/cron_topic.log 2>&1

# 09:00~21:00 매시간 뉴스 모니터링 (80점 이상 즉시 알림)
0 9-21 * * * cd {config.ROOT_DIR} && {sys.executable} hourly_monitor.py --once >> logs/cron_monitor.log 2>&1

# 21:00 데일리 다이제스트 생성 (RAG 연동) 및 옵시디언 동기화
0 21 * * * cd {config.ROOT_DIR} && {sys.executable} daily_digest.py --rag >> logs/cron_digest.log 2>&1

# 21:05 Active Thesis 가설 신뢰도 자동 점검
5 21 * * * cd {config.ROOT_DIR} && {sys.executable} thesis_checker.py >> logs/cron_checker.log 2>&1
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
        choice = input("선택 번호 입력 [1~10, q]: ").strip().lower()

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
    parser.add_argument("--rag",      action="store_true", help="RAG 심층 검색 활성화")
    args = parser.parse_args()

    if args.topic:
        run_cmd(["topic_generator.py", "--auto"])
    elif args.raw:
        run_cmd(["topic_generator.py", "--raw"])
    elif args.monitor:
        run_cmd(["hourly_monitor.py", "--once"])
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
    else:
        interactive_menu()


if __name__ == "__main__":
    main()
