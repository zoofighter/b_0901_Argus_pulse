"""
tests/test_critic.py — Critic 품질 검수 에이전트 단위 테스트
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from critic import evaluate_content, CRITIC_PROMPT_TEMPLATE


class TestCriticStructure:
    def test_prompt_template_contains_criteria(self):
        assert "수치 및 팩트 밀도" in CRITIC_PROMPT_TEMPLATE
        assert "인용 및 근거 충실도" in CRITIC_PROMPT_TEMPLATE
        assert "시각적 구조" in CRITIC_PROMPT_TEMPLATE
        assert "80점" in CRITIC_PROMPT_TEMPLATE

    @pytest.mark.llm
    def test_evaluate_content_fallback_on_empty(self):
        # 파싱 오류 시 안전 기본 통과 구조 확인
        res = evaluate_content("내용 없음")
        assert "total_score" in res
        assert "verdict" in res
        assert res["verdict"] in ("PASS", "REVISE")
