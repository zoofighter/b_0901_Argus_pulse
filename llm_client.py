"""
llm_client.py — 통합 LLM 클라이언트 (Gemini + OpenCode Muse-Spark 자동 대체)

특징:
  1. 기본 엔진: Gemini 3.7 Flash
  2. Fallback(대체) 엔진: opencode/muse-spark-1.2-contributor-free (무료 모델)
     - Gemini 503 과부하, Quota 초과, 네트워크 장애 시 자동 대체
     - 또는 .env에서 LLM_PROVIDER=opencode 설정 시 바로 1순위 사용
"""

import os
import re
import subprocess
import time
from pathlib import Path
import config

OPENCODE_BIN = Path.home() / ".opencode" / "bin" / "opencode"
OPENCODE_MODEL = os.getenv("OPENCODE_MODEL", "opencode/muse-spark-1.2-contributor-free")


def call_opencode(prompt: str) -> str:
    """OpenCode CLI (muse-spark-1.2-contributor-free) 호출"""
    if not OPENCODE_BIN.exists():
        raise FileNotFoundError(f"OpenCode 실행 파일을 찾을 수 없습니다: {OPENCODE_BIN}")

    cmd = [
        str(OPENCODE_BIN),
        "run",
        "--pure",
        "-m", OPENCODE_MODEL
    ]

    print(f"  🤖 OpenCode 호출 중... ({OPENCODE_MODEL})")
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = proc.communicate(input=prompt, timeout=120)

    if proc.returncode != 0:
        raise RuntimeError(f"OpenCode 실행 실패 (code {proc.returncode}): {stderr.strip()}")

    # OpenCode 헤더 라인 제거 (예: > build · muse-spark...)
    lines = stdout.splitlines()
    clean_lines = []
    for line in lines:
        if line.strip().startswith("> ") and ("·" in line or "muse-spark" in line):
            continue
        clean_lines.append(line)

    return "\n".join(clean_lines).strip()


def call_gemini(prompt: str, max_retries: int = 2) -> str:
    """Gemini 3.7 Flash 호출"""
    if not config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY 미설정")

    from google import genai
    client = genai.Client(api_key=config.GEMINI_API_KEY)

    for attempt in range(1, max_retries + 1):
        try:
            resp = client.models.generate_content(
                model=config.GEMINI_MODEL,
                contents=prompt
            )
            return resp.text
        except Exception as e:
            err_msg = str(e)
            if attempt < max_retries and ("503" in err_msg or "UNAVAILABLE" in err_msg):
                wait = 5 * attempt
                print(f"  ⚠️  Gemini 과부하 (503), {wait}초 후 재시도 ({attempt}/{max_retries})...")
                time.sleep(wait)
            else:
                raise


def call_llm(prompt: str, fallback_to_opencode: bool = True) -> str:
    """
    통합 LLM 호출 함수:
    - 기본: Gemini 호출 -> 실패 시 자동으로 OpenCode Muse-Spark로 대체
    - LLM_PROVIDER=opencode 인 경우 바로 OpenCode 호출
    """
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()

    # 1. 사용자가 명시적으로 OpenCode를 지정한 경우
    if provider == "opencode":
        return call_opencode(prompt)

    # 2. 기본: Gemini 시도 후 실패 시 OpenCode 대체
    try:
        return call_gemini(prompt)
    except Exception as gemini_err:
        if not fallback_to_opencode:
            raise

        print(f"\n  ⚠️  Gemini 호출 실패 ({gemini_err})")
        print(f"  🔄 대체 모델 ({OPENCODE_MODEL})로 자동 전환합니다...")
        try:
            return call_opencode(prompt)
        except Exception as opencode_err:
            raise RuntimeError(
                f"Gemini와 OpenCode 모두 실패했습니다.\n"
                f"- Gemini 에러: {gemini_err}\n"
                f"- OpenCode 에러: {opencode_err}"
            )


if __name__ == "__main__":
    print("=== OpenCode Muse-Spark 연결 테스트 ===")
    try:
        ans = call_opencode("한국의 2차전지 산업에 대해 한 문장으로 정의해줘.")
        print(f"✅ OpenCode 응답 확인:\n{ans}")
    except Exception as e:
        print(f"❌ OpenCode 실패: {e}")
