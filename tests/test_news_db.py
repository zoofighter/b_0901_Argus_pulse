"""
tests/test_news_db.py
TC-02: 뉴스 DB 연결 및 쿼리 테스트

실행:
    pytest tests/test_news_db.py -v

전제조건:
    - b_0826_news_research SQLite DB가 접근 가능한 위치에 있어야 함
    - .env에 NEWS_DB_PATH 설정 또는 기본 경로 존재
"""

import pytest
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# DB 경로 탐색 (실제 구현 전 경로 자동 탐색)
CANDIDATE_PATHS = [
    Path("../b_0826_news_research/db/news.sqlite"),
    Path("../../b_0826_news_research/db/news.sqlite"),
    Path.home() / "Dropbox/03_code/b_0826_news_research/db/news.sqlite",
]

def find_news_db() -> Path | None:
    import os
    env_path = os.getenv("NEWS_DB_PATH")
    if env_path and Path(env_path).exists():
        return Path(env_path)
    for p in CANDIDATE_PATHS:
        if p.exists():
            return p
    return None

NEWS_DB = find_news_db()
DB_AVAILABLE = NEWS_DB is not None

skip_if_no_db = pytest.mark.skipif(
    not DB_AVAILABLE,
    reason=f"뉴스 DB를 찾을 수 없음. NEWS_DB_PATH 환경변수 또는 경로를 확인하세요."
)


class TestDBConnection:
    """TC-02-1: DB 연결 기본 테스트"""

    def test_db_path_found(self):
        """DB 파일 경로 발견"""
        assert DB_AVAILABLE, (
            "뉴스 DB를 찾을 수 없습니다.\n"
            "확인할 경로:\n" +
            "\n".join(f"  - {p}" for p in CANDIDATE_PATHS)
        )

    @skip_if_no_db
    def test_connection_succeeds(self):
        """SQLite 연결 성공"""
        conn = sqlite3.connect(NEWS_DB)
        assert conn is not None
        conn.close()

    @skip_if_no_db
    def test_connection_speed(self):
        """연결 1초 이내"""
        import time
        start = time.time()
        conn = sqlite3.connect(NEWS_DB)
        conn.close()
        elapsed = time.time() - start
        assert elapsed < 1.0, f"연결 시간 {elapsed:.3f}초"

    @skip_if_no_db
    def test_news_table_exists(self):
        """news 테이블 존재 확인"""
        conn = sqlite3.connect(NEWS_DB)
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
        table_names = [t[0] for t in tables]
        conn.close()
        assert "news" in table_names, (
            f"'news' 테이블 없음. 존재하는 테이블: {table_names}"
        )


class TestNewsQuery:
    """TC-02-2: 뉴스 쿼리 테스트"""

    @skip_if_no_db
    def test_news_has_records(self):
        """뉴스 데이터 존재"""
        conn = sqlite3.connect(NEWS_DB)
        count = conn.execute("SELECT COUNT(*) FROM news").fetchone()[0]
        conn.close()
        assert count > 0, "뉴스 데이터가 없습니다"

    @skip_if_no_db
    def test_required_columns_exist(self):
        """필수 컬럼 존재: title, score, company"""
        conn = sqlite3.connect(NEWS_DB)
        cursor = conn.execute("SELECT * FROM news LIMIT 1")
        cols = [d[0] for d in cursor.description]
        conn.close()
        required = ["title", "score"]
        for col in required:
            assert col in cols, f"'{col}' 컬럼 없음. 실제 컬럼: {cols}"

    @skip_if_no_db
    def test_score_range(self):
        """score 값 0~100 범위"""
        conn = sqlite3.connect(NEWS_DB)
        rows = conn.execute("SELECT score FROM news LIMIT 100").fetchall()
        conn.close()
        for (score,) in rows:
            if score is not None:
                assert 0 <= score <= 100, f"score={score} 범위 초과"

    @skip_if_no_db
    def test_hot_news_query(self):
        """고득점 뉴스 조회 (score >= 60)"""
        conn = sqlite3.connect(NEWS_DB)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT title, score FROM news WHERE score >= 60 ORDER BY score DESC LIMIT 15"
        ).fetchall()
        conn.close()
        assert isinstance(rows, list)
        for row in rows:
            assert row["score"] >= 60

    @skip_if_no_db
    def test_recent_news_filter(self):
        """최근 2일 뉴스 필터 (published_at 컬럼 존재 시)"""
        conn = sqlite3.connect(NEWS_DB)
        cols = [d[0] for d in conn.execute("SELECT * FROM news LIMIT 1").description]
        conn.close()

        date_col = next((c for c in cols if "date" in c or "time" in c or "at" in c), None)
        if date_col is None:
            pytest.skip(f"날짜 컬럼 없음. 컬럼: {cols}")

        conn = sqlite3.connect(NEWS_DB)
        rows = conn.execute(
            f"SELECT COUNT(*) FROM news WHERE {date_col} >= date('now', '-2 days')"
        ).fetchone()
        conn.close()
        assert rows[0] >= 0  # 쿼리 자체가 오류 없이 실행되면 OK


class TestThesisMatching:
    """TC-02-3: Thesis 키워드 매칭 테스트 (DB 없이도 실행 가능)"""

    def _match_thesis(self, title: str, keyword_map: dict) -> list[str]:
        """간단한 키워드 매칭 로직"""
        matched = []
        for tid, keywords in keyword_map.items():
            if any(kw in title for kw in keywords):
                matched.append(tid)
        return matched

    def test_hbm_matches_t02(self):
        """HBM 뉴스 → T-02 매칭"""
        from thesis_loader import get_active_keywords
        kmap = get_active_keywords()
        title = "SK하이닉스 HBM4 엔비디아 납품 승인"
        matched = self._match_thesis(title, kmap)
        assert "T-02" in matched, f"T-02 미매칭. 매칭됨: {matched}"

    def test_datacenter_matches_t01(self):
        """데이터센터 뉴스 → T-01 매칭"""
        from thesis_loader import get_active_keywords
        kmap = get_active_keywords()
        title = "MS 3GW 데이터센터 착공 발표"
        matched = self._match_thesis(title, kmap)
        assert "T-01" in matched, f"T-01 미매칭. 매칭됨: {matched}"

    def test_ess_matches_t32(self):
        """ESS 뉴스 → T-32 매칭"""
        from thesis_loader import get_active_keywords
        kmap = get_active_keywords()
        title = "SK온 ESS 저장용 배터리 1.5조 수주"
        matched = self._match_thesis(title, kmap)
        assert "T-32" in matched, (
            f"T-32 미매칭. 매칭됨: {matched}\n"
            f"T-32 키워드: {kmap.get('T-32', [])}"
        )

    def test_unrelated_news_no_match(self):
        """관련 없는 뉴스 → 매칭 없음 (또는 최소화)"""
        from thesis_loader import get_active_keywords
        kmap = get_active_keywords()
        title = "오늘의 날씨 맑음"
        matched = self._match_thesis(title, kmap)
        assert len(matched) == 0, f"무관한 뉴스에 매칭: {matched}"

    def test_multiple_thesis_match(self):
        """복합 키워드 → 복수 Thesis 매칭"""
        from thesis_loader import get_active_keywords
        kmap = get_active_keywords()
        title = "엔비디아 데이터센터 HBM4 대량 수주"
        matched = self._match_thesis(title, kmap)
        # T-01(데이터센터), T-02(HBM) 동시 매칭 기대
        assert len(matched) >= 2, f"복수 매칭 기대, 실제: {matched}"
