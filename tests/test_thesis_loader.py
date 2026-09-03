"""
tests/test_thesis_loader.py
TC-01: thesis_loader.py 기본 동작 테스트

실행:
    pytest tests/test_thesis_loader.py -v
"""

import pytest
import sys
from pathlib import Path

# 루트 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from thesis_loader import (
    load_theses,
    load_thesis_by_id,
    get_active_keywords,
    update_thesis_confidence,
)

EXPECTED_TOTAL = 38      # 현재 등록된 전체 Thesis 수
EXPECTED_ACTIVE_MIN = 30  # active 상태 최소 수 (watch 포함 시 다름)


class TestLoadTheses:
    """TC-01-1: 전체 로드 테스트"""

    def test_load_all_returns_list(self):
        """None 필터: 전체 반환"""
        theses = load_theses(status_filter=None)
        assert isinstance(theses, list), "리스트가 아님"

    def test_load_all_count(self):
        """전체 Thesis 수 일치"""
        theses = load_theses(status_filter=None)
        assert len(theses) == EXPECTED_TOTAL, (
            f"기대: {EXPECTED_TOTAL}개, 실제: {len(theses)}개\n"
            f"thesis/ 폴더 파일 수를 확인하세요."
        )

    def test_load_active_only(self):
        """active 상태만 필터링"""
        theses = load_theses(status_filter="active")
        assert len(theses) >= EXPECTED_ACTIVE_MIN
        assert all(t["status"] == "active" for t in theses), (
            "active가 아닌 Thesis가 포함됨"
        )

    def test_load_watch_only(self):
        """watch 상태 필터링"""
        theses = load_theses(status_filter="watch")
        assert all(t["status"] == "watch" for t in theses)

    def test_required_fields_present(self):
        """필수 필드 존재 확인"""
        required = ["id", "title", "hypothesis", "direction",
                    "confidence", "priority", "status", "keywords"]
        theses = load_theses(status_filter=None)
        for t in theses:
            for field in required:
                assert field in t, f"[{t.get('id', '?')}] '{field}' 필드 없음"

    def test_confidence_range(self):
        """Confidence 값 0~100 범위"""
        theses = load_theses(status_filter=None)
        for t in theses:
            c = t["confidence"]
            assert 0 <= c <= 100, (
                f"[{t['id']}] confidence={c} — 0~100 범위를 벗어남"
            )

    def test_direction_valid(self):
        """direction 값은 bullish/bearish/neutral 중 하나"""
        valid = {"bullish", "bearish", "neutral"}
        theses = load_theses(status_filter=None)
        for t in theses:
            assert t["direction"] in valid, (
                f"[{t['id']}] direction='{t['direction']}' — 유효하지 않음"
            )

    def test_id_format(self):
        """ID 형식: T-숫자"""
        import re
        theses = load_theses(status_filter=None)
        for t in theses:
            assert re.match(r"T-\d+$", t["id"]), (
                f"ID 형식 오류: '{t['id']}'"
            )

    def test_no_duplicate_ids(self):
        """중복 ID 없음"""
        theses = load_theses(status_filter=None)
        ids = [t["id"] for t in theses]
        assert len(ids) == len(set(ids)), (
            f"중복 ID 발견: {[x for x in ids if ids.count(x) > 1]}"
        )


class TestLoadThesisById:
    """TC-01-2: 단건 조회 테스트"""

    def test_load_t01(self):
        """T-01 조회"""
        t = load_thesis_by_id("T-01")
        assert t is not None
        assert t["id"] == "T-01"
        assert isinstance(t["confidence"], int) and 0 <= t["confidence"] <= 100
        assert "데이터센터" in t["keywords"]

    def test_load_t32_ess(self):
        """T-32 ESS 조회 (신규 추가 Thesis)"""
        t = load_thesis_by_id("T-32")
        assert t is not None
        assert t["id"] == "T-32"
        assert "ESS" in t["title"] or "배터리" in t["title"]

    def test_load_bearish_theses(self):
        """Bearish Thesis (T-35~T-38) 조회"""
        for tid in ["T-35", "T-36", "T-37", "T-38"]:
            t = load_thesis_by_id(tid)
            assert t is not None, f"{tid} 없음"
            assert t["direction"] == "bearish", f"{tid} direction 오류"

    def test_load_nonexistent_id(self):
        """존재하지 않는 ID → None 반환"""
        result = load_thesis_by_id("T-99")
        assert result is None

    def test_load_empty_id(self):
        """빈 ID → None 반환"""
        result = load_thesis_by_id("")
        assert result is None


class TestGetActiveKeywords:
    """TC-01-3: 키워드 맵 테스트"""

    def test_returns_dict(self):
        kmap = get_active_keywords()
        assert isinstance(kmap, dict)

    def test_keys_are_thesis_ids(self):
        import re
        kmap = get_active_keywords()
        for key in kmap:
            assert re.match(r"T-\d+$", key), f"키 형식 오류: '{key}'"

    def test_values_are_lists(self):
        kmap = get_active_keywords()
        for tid, kws in kmap.items():
            assert isinstance(kws, list), f"{tid} 키워드가 리스트가 아님"
            assert len(kws) > 0, f"{tid} 키워드가 비어 있음"

    def test_t01_keywords(self):
        """T-01 키워드에 핵심 단어 포함"""
        kmap = get_active_keywords()
        assert "T-01" in kmap
        keywords_str = " ".join(kmap["T-01"])
        assert any(k in keywords_str for k in ["데이터센터", "전력", "HBM"])

    def test_t02_hbm_keywords(self):
        """T-02 키워드에 HBM 포함"""
        kmap = get_active_keywords()
        assert "T-02" in kmap
        assert any("HBM" in k for k in kmap["T-02"])


class TestUpdateConfidence:
    """TC-01-4: Confidence 업데이트 테스트"""

    def test_update_and_restore(self):
        """업데이트 후 원복 (부작용 없음)"""
        original = load_thesis_by_id("T-01")["confidence"]
        new_val = min(original + 5, 100)

        result = update_thesis_confidence("T-01", new_val)
        assert result is True

        updated = load_thesis_by_id("T-01")["confidence"]
        assert updated == new_val

        # 원복
        update_thesis_confidence("T-01", original)
        restored = load_thesis_by_id("T-01")["confidence"]
        assert restored == original

    def test_update_nonexistent_returns_false(self):
        """없는 ID 업데이트 → False"""
        result = update_thesis_confidence("T-99", 50)
        assert result is False

    def test_last_checked_updated(self):
        """업데이트 후 last_checked 갱신"""
        update_thesis_confidence("T-02", 75)
        t = load_thesis_by_id("T-02")
        assert t["last_checked"] is not None, "last_checked가 갱신되지 않음"


class TestPerformance:
    """TC-01-5: 성능 테스트"""

    def test_load_all_speed(self):
        """전체 로드 3초 이내"""
        import time
        start = time.time()
        load_theses(status_filter=None)
        elapsed = time.time() - start
        assert elapsed < 3.0, f"로드 시간 {elapsed:.2f}초 — 3초 초과"

    def test_load_by_id_speed(self):
        """단건 조회 0.5초 이내"""
        import time
        start = time.time()
        load_thesis_by_id("T-01")
        elapsed = time.time() - start
        assert elapsed < 0.5, f"조회 시간 {elapsed:.3f}초 — 0.5초 초과"
