"""
tests/test_milestone_falsification.py
Phase 1 마일스톤 및 가설 기각(Falsification) 감시 엔진 & 디스코드 긴급 경보 단위 테스트
"""

import pytest
from unittest.mock import patch, MagicMock
from thesis_loader import update_thesis_evaluation, load_thesis_by_id
from notifier import notify_thesis_inflection
import config


def test_update_thesis_evaluation_milestone_achieved(tmp_path):
    """마일스톤 달성 시 프론트매터 및 라이프사이클 갱신 테스트"""
    sample_thesis = tmp_path / "T99-01-테스트가설.md"
    sample_thesis.write_text("""---
id: T99-01
title: 테스트 가설
hypothesis: 테스트 핵심 가설
direction: bullish
confidence: 70
status: active
milestone: "공급 퀄 테스트 통과"
milestone_status: NONE
falsification_condition: "수율 20% 미만 고착화"
falsification_triggered: false
lifecycle_stage: Catalyst Active
---

## 핵심 가설
가설 본문 내용입니다.
""", encoding="utf-8")

    with patch("thesis_loader.THESIS_DIR", tmp_path):
        ok = update_thesis_evaluation(
            thesis_id="T99-01",
            new_confidence=85,
            milestone_status="ACHIEVED",
            milestone_evidence="엔비디아 퀄 테스트 공식 통과 발표",
            falsification_triggered=False,
        )
        assert ok is True

        updated = load_thesis_by_id("T99-01")
        assert updated is not None
        assert updated["confidence"] == 85
        assert updated["milestone_status"] == "ACHIEVED"
        assert updated["milestone_evidence"] == "엔비디아 퀄 테스트 공식 통과 발표"
        assert updated["falsification_triggered"] is False
        assert updated["lifecycle_stage"] == "Priced-in"


def test_update_thesis_evaluation_falsification_triggered(tmp_path):
    """기각 조건 도달 시 프론트매터 및 라이프사이클 Falsified 전환 테스트"""
    sample_thesis = tmp_path / "T99-02-기각테스트가설.md"
    sample_thesis.write_text("""---
id: T99-02
title: 기각 테스트 가설
hypothesis: 테스트 핵심 가설
direction: bullish
confidence: 60
status: active
milestone: "2nm 양산 성공"
milestone_status: NONE
falsification_condition: "수율 20% 미만 고착화"
falsification_triggered: false
lifecycle_stage: Catalyst Active
---

## 핵심 가설
가설 본문 내용입니다.
""", encoding="utf-8")

    with patch("thesis_loader.THESIS_DIR", tmp_path):
        ok = update_thesis_evaluation(
            thesis_id="T99-02",
            new_confidence=30,
            milestone_status="NONE",
            falsification_triggered=True,
            falsification_reason="수율 15% 수준에서 6개월간 개선 정체",
        )
        assert ok is True

        updated = load_thesis_by_id("T99-02")
        assert updated is not None
        assert updated["confidence"] == 30
        assert updated["falsification_triggered"] is True
        assert updated["falsification_reason"] == "수율 15% 수준에서 6개월간 개선 정체"
        assert updated["lifecycle_stage"] == "Falsified"


def test_notify_thesis_inflection_triggers():
    """디스코드 변곡점 경보 발송 조건 검증"""
    thesis = {
        "id": "T2-01",
        "title": "메모리 산업의 변화",
        "hypothesis": "HBM4는 커스텀 ASIC화된다.",
    }

    # 1. 일반 변동(변화 미미 5%p) -> 경보 미발송(True 반환)
    with patch("notifier.send_discord") as mock_send:
        eval_res_normal = {
            "milestone_status": "NONE",
            "falsification_triggered": False,
            "reason": "소소한 뉴스 유입",
        }
        notify_thesis_inflection(thesis, eval_res_normal, old_conf=70, new_conf=75)
        mock_send.assert_not_called()

    # 2. 10%p 이상 급변 -> 경보 발송 (황색 임베드)
    with patch("notifier.send_discord") as mock_send:
        mock_send.return_value = True
        eval_res_inflection = {
            "milestone_status": "PROGRESS",
            "milestone_evidence": "테스트 샘플 인도 확인",
            "falsification_triggered": False,
            "supporting_evidence": "주요 고객사향 납품 개시",
            "counter_evidence": "없음",
            "reason": "단기 강력 모멘텀 발생",
        }
        notify_thesis_inflection(thesis, eval_res_inflection, old_conf=70, new_conf=85)
        assert mock_send.called
        call_kwargs = mock_send.call_args[1]
        embed = call_kwargs["embeds"][0]
        assert embed["color"] == 0xFFA500  # 황색

    # 3. 마일스톤 달성 -> 경보 발송 (녹색 임베드)
    with patch("notifier.send_discord") as mock_send:
        mock_send.return_value = True
        eval_res_milestone = {
            "milestone_status": "ACHIEVED",
            "milestone_evidence": "엔비디아 퀄 테스트 공식 통과",
            "falsification_triggered": False,
            "supporting_evidence": "공식 승인",
            "reason": "핵심 촉매 달성",
        }
        notify_thesis_inflection(thesis, eval_res_milestone, old_conf=70, new_conf=75)
        assert mock_send.called
        embed = mock_send.call_args[1]["embeds"][0]
        assert embed["color"] == 0x00FF00  # 녹색

    # 4. 기각 발생 -> 경보 발송 (적색 임베드 Red Flag)
    with patch("notifier.send_discord") as mock_send:
        mock_send.return_value = True
        eval_res_falsified = {
            "milestone_status": "NONE",
            "falsification_triggered": True,
            "falsification_reason": "프로젝트 전면 취소 공시",
            "reason": "가설 훼손",
        }
        notify_thesis_inflection(thesis, eval_res_falsified, old_conf=70, new_conf=40)
        assert mock_send.called
        embed = mock_send.call_args[1]["embeds"][0]
        assert embed["color"] == 0xFF0000  # 적색
