"""
tests/test_thesis_ranking.py
TC-06: Thesis 시장 모멘텀 랭킹 (News Momentum Rank) 기능 테스트

실행:
    pytest tests/test_thesis_ranking.py -v
"""

import pytest
import sys
from pathlib import Path

# 루트 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from thesis_loader import get_thesis_momentum_ranking, load_theses, sync_thesis_ranks_to_files


class TestThesisMomentumRanking:
    """시장 모멘텀 랭킹 기능 단위 테스트"""

    def test_ranking_returns_list(self):
        """랭킹 함수가 리스트를 반환하는지 확인"""
        ranked = get_thesis_momentum_ranking(days=2, status_filter="active")
        assert isinstance(ranked, list)
        assert len(ranked) > 0

    def test_ranking_required_fields(self):
        """반환된 테제 객체에 랭킹 및 모멘텀 필드가 모두 존재하는지 확인"""
        ranked = get_thesis_momentum_ranking(days=2, status_filter="active")
        required_fields = [
            "rank", "id", "title", "momentum_score",
            "raw_momentum_score", "news_count", "confidence", "priority"
        ]
        for t in ranked:
            for field in required_fields:
                assert field in t, f"[{t.get('id', '?')}] '{field}' 필드가 누락되었습니다."

    def test_ranking_sequence(self):
        """순위(rank)가 1부터 1씩 증가하며 올바르게 매겨지는지 확인"""
        ranked = get_thesis_momentum_ranking(days=2, status_filter="active", limit=10)
        ranks = [t["rank"] for t in ranked]
        assert ranks == list(range(1, len(ranked) + 1))

    def test_ranking_order_consistency(self):
        """상위 랭크의 모멘텀 점수가 하위 랭크보다 크거나 같은지 확인"""
        ranked = get_thesis_momentum_ranking(days=2, status_filter="active")
        for i in range(len(ranked) - 1):
            assert (
                ranked[i]["raw_momentum_score"] >= ranked[i+1]["raw_momentum_score"] or
                ranked[i]["momentum_score"] >= ranked[i+1]["momentum_score"]
            ), f"Rank {ranked[i]['rank']}와 {ranked[i+1]['rank']}의 점수 순서 불일치"

    def test_ranking_limit(self):
        """limit 인자가 정확히 적용되는지 확인"""
        limit_count = 5
        ranked = get_thesis_momentum_ranking(days=2, status_filter="active", limit=limit_count)
        assert len(ranked) == limit_count

    def test_fallback_when_db_missing(self):
        """DB 파일이 없거나 경로가 잘못되어도 예외 없이 안전하게 폴백하는지 확인"""
        fake_path = Path("/tmp/non_existent_news_db.sqlite")
        ranked = get_thesis_momentum_ranking(days=2, status_filter="active", db_path=fake_path)
        assert isinstance(ranked, list)
        assert len(ranked) > 0
        # 뉴스가 없어도 priority와 confidence 기반으로 기본 점수 부여 및 랭킹 정렬
        assert all(t["news_count"] == 0 for t in ranked)
        assert all(t["rank"] > 0 for t in ranked)

    def test_sync_thesis_ranks_to_files(self):
        """sync_thesis_ranks_to_files 실행 후 MD 파일 frontmatter에 rank, momentum 저장 확인"""
        ranked = sync_thesis_ranks_to_files(days=2)
        assert len(ranked) > 0
        # T-01 로드하여 rank, momentum 필드 확인
        theses = load_theses(status_filter=None)
        t01 = next((t for t in theses if t["id"] == "T-01"), None)
        assert t01 is not None
        assert "rank" in t01
        assert "momentum" in t01
        assert isinstance(t01["rank"], int)
        assert isinstance(t01["momentum"], (int, float))
