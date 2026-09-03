"""
config.py — Argus Pulse 설정 중앙화

컬럼 확인된 news DB 스키마:
  id, url, title, snippet, source, company, ticker, query, score, published, collected_at
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── 경로 ─────────────────────────────────────────────────────────────────────
ROOT_DIR      = Path(__file__).parent
THESIS_DIR    = ROOT_DIR / "thesis"
OUTPUT_DIR    = ROOT_DIR / "output"
RAW_DIR       = ROOT_DIR / "99.raw"
LOG_DIR       = ROOT_DIR / "logs"

NEWS_DB_PATH  = Path(os.getenv(
    "NEWS_DB_PATH",
    str(ROOT_DIR.parent / "b_0826_news_research" / "db" / "news.sqlite")
))

CHROMA_DB_PATH = ROOT_DIR / "db" / "chromadb"
PDF_REPORTS_DIR = Path(os.getenv(
    "PDF_REPORTS_DIR",
    str(ROOT_DIR.parent / "a_langragh" / "reports")
))

OBSIDIAN_PATH = Path(os.getenv("OBSIDIAN_VAULT_PATH") or os.getenv("OBSIDIAN_PATH", str(Path.home() / "Documents" / "Obsidian" / "Argus")))

# ── RAG 엔진 설정 ─────────────────────────────────────────────────────────────
RAG_CHUNK_SIZE    = int(os.getenv("RAG_CHUNK_SIZE", "1000"))
RAG_CHUNK_OVERLAP = int(os.getenv("RAG_CHUNK_OVERLAP", "200"))
RAG_TOP_K         = int(os.getenv("RAG_TOP_K", "5"))

# ── API 및 모델 ───────────────────────────────────────────────────────────────
LLM_PROVIDER     = os.getenv("LLM_PROVIDER", "gemini") # "gemini" 또는 "opencode"
GEMINI_API_KEY   = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL     = os.getenv("GEMINI_MODEL", "gemini-3.7-flash")
OPENCODE_MODEL   = os.getenv("OPENCODE_MODEL", "opencode/muse-spark-1.2-contributor-free")
DISCORD_WEBHOOK  = os.getenv("DISCORD_WEBHOOK_URL", "")

# ── 뉴스 설정 ─────────────────────────────────────────────────────────────────
NEWS_SCORE_THRESHOLD   = int(os.getenv("NEWS_SCORE_THRESHOLD", "60"))   # 수집 기준
NEWS_HOT_THRESHOLD     = int(os.getenv("NEWS_HOT_THRESHOLD", "80"))     # 새 블로그 트리거
NEWS_LOOKBACK_DAYS     = int(os.getenv("NEWS_LOOKBACK_DAYS", "2"))      # 최근 N일
MAX_NEWS_FOR_PROMPT    = int(os.getenv("MAX_NEWS_FOR_PROMPT", "15"))    # 프롬프트 최대 건수
HOT_NEWS_MIN_COUNT     = int(os.getenv("HOT_NEWS_MIN_COUNT", "2"))      # 새 콘텐츠 생성 최소 건수

# ── 콘텐츠 설정 ───────────────────────────────────────────────────────────────
NUM_TOPICS    = int(os.getenv("NUM_TOPICS", "3"))     # 추천 주제 수
BLOG_MIN_CHARS = 800                                   # 블로그 최소 글자 수
THREAD_MIN_LINES = 20                                  # 스레드 최소 줄 수

# ── 출력 폴더 생성 ─────────────────────────────────────────────────────────────
for d in [OUTPUT_DIR / "blog", OUTPUT_DIR / "thread", OUTPUT_DIR / "digest",
          OUTPUT_DIR / "review", LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def validate() -> list[str]:
    """설정 유효성 검사. 문제 목록 반환 (빈 리스트면 OK)"""
    issues = []
    if not GEMINI_API_KEY:
        issues.append("❌ GEMINI_API_KEY 미설정 — .env 파일에 추가 필요")
    if not NEWS_DB_PATH.exists():
        issues.append(f"❌ 뉴스 DB 없음: {NEWS_DB_PATH}")
    if not THESIS_DIR.exists() or not list(THESIS_DIR.glob("T-*.md")):
        issues.append(f"❌ Thesis 파일 없음: {THESIS_DIR}")
    return issues


if __name__ == "__main__":
    print("=== Argus Pulse 설정 점검 ===")
    print(f"  ROOT_DIR      : {ROOT_DIR}")
    print(f"  NEWS_DB_PATH  : {NEWS_DB_PATH} ({'✅' if NEWS_DB_PATH.exists() else '❌'})")
    print(f"  THESIS_DIR    : {THESIS_DIR} ({len(list(THESIS_DIR.glob('T-*.md')))}개)")
    print(f"  OUTPUT_DIR    : {OUTPUT_DIR}")
    print(f"  RAW_DIR       : {RAW_DIR} ({len(list(RAW_DIR.glob('*'))) if RAW_DIR.exists() else 0}개 파일)")
    print(f"  GEMINI_API_KEY: {'✅ 설정됨' if GEMINI_API_KEY else '❌ 미설정'}")
    print(f"  DISCORD_WEBHOOK: {'✅ 설정됨' if DISCORD_WEBHOOK else '⚠️  미설정 (선택)'}")
    print()
    issues = validate()
    if issues:
        print("⚠️  설정 문제:")
        for i in issues:
            print(f"   {i}")
    else:
        print("✅ 모든 설정 정상")
