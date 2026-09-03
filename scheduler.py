"""
scheduler.py — Argus Pulse 일일 자동화 스케줄러

동작 스케줄:
  - 08:00: 아침 주제 추천 생성 & 알림 (topic_generator.py --auto)
  - 09:00 ~ 21:00 (매시간 00분): 실시간 뉴스 감시 & 고득점 즉시 알림 (hourly_monitor.py --once)
  - 21:00: 일일 데일리 다이제스트 생성 & 옵시디언 동기화 (daily_digest.py)

실행:
  python scheduler.py           # 무한 루프 실행 (백그라운드용)
  python scheduler.py --test    # 각 작업 1회 순차 테스트 실행
"""

import argparse
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import config


def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def run_job(script_name: str, args: list[str] = None):
    """지정 스크립트 실행"""
    cmd = [sys.executable, script_name] + (args or [])
    log(f"▶️ [작업 시작] {' '.join(cmd)}")
    try:
        res = subprocess.run(cmd, check=True)
        log(f"✅ [작업 완료] {script_name} (종료 코드: {res.returncode})")
    except subprocess.CalledProcessError as e:
        log(f"❌ [작업 실패] {script_name} (종료 코드: {e.returncode})")
    except Exception as e:
        log(f"⚠️ [실행 예외] {script_name}: {e}")


def test_all_jobs():
    """모든 정기 작업을 1회 테스트"""
    print("\n🧪 [Argus Pulse 스케줄러 테스트 모드]")
    print("1. 매시간 뉴스 감시 테스트...")
    run_job("hourly_monitor.py", ["--once"])

    print("\n2. 데일리 다이제스트 생성 테스트...")
    run_job("daily_digest.py")

    print("\n3. 옵시디언 전체 동기화 테스트...")
    run_job("obsidian_sync.py", ["--all"])
    print("\n🎉 모든 테스트 완료!\n")


def scheduler_loop():
    log("🦅 Argus Pulse 자동화 스케줄러를 시작합니다.")
    log("   - 08:00 : 아침 블로그 주제 추천 및 알림")
    log("   - 09:00~21:00 (매 정각) : 뉴스 감시 및 80점+ 즉시 알림")
    log("   - 21:00 : 일일 다이제스트 생성 및 옵시디언 동기화")
    log("   (종료하려면 Ctrl+C 를 누르세요)\n")

    last_hourly_hour = -1
    last_topic_date = ""
    last_digest_date = ""

    while True:
        try:
            now = datetime.now()
            today_str = now.strftime("%Y-%m-%d")
            hour = now.hour
            minute = now.minute

            # 1. 08:00 아침 주제 추천 (하루 1회)
            if hour == 8 and minute == 0 and last_topic_date != today_str:
                log("🌅 [08:00] 아침 블로그 주제 추천 시작")
                run_job("topic_generator.py", ["--auto", "--n", "3"])
                last_topic_date = today_str

            # 2. 09:00 ~ 21:00 매시간 뉴스 감시 (매 정각 1회)
            if 9 <= hour <= 21 and minute == 0 and last_hourly_hour != hour:
                log(f"🔍 [{hour:02d}:00] 매시간 뉴스 감시 실행")
                run_job("hourly_monitor.py", ["--once"])
                last_hourly_hour = hour

            # 3. 21:00 데일리 다이제스트 (하루 1회) + Thesis 자동 점검
            if hour == 21 and minute == 0 and last_digest_date != today_str:
                log("📊 [21:00] 데일리 다이제스트 생성 시작 (RAG 연동)")
                run_job("daily_digest.py", ["--rag"])
                log("🧠 [21:05] Active Thesis 가설 신뢰도 및 근거 자동 점검 시작")
                run_job("thesis_checker.py")
                last_digest_date = today_str

            time.sleep(30)

        except KeyboardInterrupt:
            log("🛑 스케줄러가 사용자에 의해 중단되었습니다.")
            break
        except Exception as e:
            log(f"⚠️ 스케줄러 루프 예외: {e}")
            time.sleep(30)


def main():
    parser = argparse.ArgumentParser(description="Argus Pulse — 스케줄러")
    parser.add_argument("--test", action="store_true", help="모든 작업 1회 즉시 실행 테스트")
    args = parser.parse_args()

    if args.test:
        test_all_jobs()
    else:
        scheduler_loop()


if __name__ == "__main__":
    main()
