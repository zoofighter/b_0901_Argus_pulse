import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
import config
from pdf_parser import parse_report_filename, clean_pdf_text
from rag_engine import chunk_text, make_doc_id, format_rag_context, search
from thesis_loader import update_thesis_confidence, append_thesis_evidence, load_thesis_by_id


class TestPDFParser:
    def test_parse_report_filename_standard(self):
        fn = "26.04.08_삼성전자_키움증권_너무 좋아도 걱정.pdf"
        meta = parse_report_filename(fn)
        assert meta["date"] == "2026-04-08"
        assert meta["company"] == "삼성전자"
        assert meta["broker"] == "키움증권"
        assert meta["title"] == "너무 좋아도 걱정"

    def test_parse_report_filename_hyphen(self):
        fn = "26.04.08_LG에너지솔루션_iM증권_1Q26 저점으로 ESS 중심 실적 회복세 전망.pdf"
        meta = parse_report_filename(fn)
        assert meta["date"] == "2026-04-08"
        assert meta["company"] == "LG에너지솔루션"
        assert meta["broker"] == "iM증권"

    def test_clean_pdf_text(self):
        raw = "삼성전자   HBM4 \n\n\n\n 공급  확정 "
        cleaned = clean_pdf_text(raw)
        assert "삼성전자 HBM4" in cleaned
        assert "\n\n\n" not in cleaned


class TestRAGEngine:
    def test_chunk_text_basic(self):
        sample = "가" * 2500
        chunks = chunk_text(sample, chunk_size=1000, overlap=200)
        assert len(chunks) >= 3
        assert all(len(c) <= 1000 for c in chunks)

    def test_make_doc_id_unique(self):
        id1 = make_doc_id("file1.pdf", 0)
        id2 = make_doc_id("file1.pdf", 1)
        id3 = make_doc_id("file2.pdf", 0)
        assert id1 != id2
        assert id1 != id3

    def test_format_rag_context(self):
        mock_chunks = [
            {
                "text": "SK하이닉스 2026년 HBM3E 매출 15조원 전망.",
                "metadata": {"company": "SK하이닉스", "broker": "대신증권", "date": "2026-04-08", "title": "메모리 리포트"}
            }
        ]
        context = format_rag_context(mock_chunks)
        assert "SK하이닉스" in context
        assert "대신증권" in context
        assert "15조원" in context

    def test_search_returns_results(self):
        # 이미 인제스트된 DB에서 검색
        res = search("HBM 반도체", n_results=2)
        assert isinstance(res, list)
        if res:
            assert "text" in res[0]
            assert "metadata" in res[0]


class TestThesisUpdates:
    def test_confidence_bounds(self):
        original = load_thesis_by_id("T-01")["confidence"]
        # 초과치 테스트
        update_thesis_confidence("T-01", 150)
        assert load_thesis_by_id("T-01")["confidence"] == 100
        update_thesis_confidence("T-01", -20)
        assert load_thesis_by_id("T-01")["confidence"] == 0
        # 원복
        update_thesis_confidence("T-01", original)
        assert load_thesis_by_id("T-01")["confidence"] == original

    def test_append_thesis_evidence(self):
        success = append_thesis_evidence("T-01", "2026-09-03", supporting="테스트 지지 근거", counter="테스트 반박 근거")
        assert success is True
        t = load_thesis_by_id("T-01")
        # 파일 원문 확인
        md_file = config.THESIS_DIR / "T-01-데이터센터의-변화.md"
        content = md_file.read_text(encoding="utf-8")
        assert "테스트 지지 근거" in content
        assert "테스트 반박 근거" in content

        # 테스트 흔적 제거 원복
        clean_content = content.replace("- 2026-09-03: 테스트 지지 근거\n", "").replace("- 2026-09-03: 테스트 반박 근거\n", "")
        md_file.write_text(clean_content, encoding="utf-8")
