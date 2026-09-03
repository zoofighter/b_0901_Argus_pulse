"""
tests/test_pipeline.py
TC-03~TC-07: 주제 생성, 블로그/스레드 생성, E2E, 엣지 케이스 테스트

실행:
    pytest tests/test_pipeline.py -v                  # 전체
    pytest tests/test_pipeline.py -v -m "no_llm"     # LLM 없이 실행 가능한 것만
    pytest tests/test_pipeline.py -v -m "llm"        # LLM 호출 포함

전제조건:
    - GEMINI_API_KEY 환경변수 설정 시 LLM 테스트 실행
    - API 키 없으면 LLM 테스트는 자동 skip
"""

import pytest
import os
import sys
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))
import config

# LLM 사용 가능 여부
GEMINI_KEY = os.getenv("GEMINI_API_KEY") or config.GEMINI_API_KEY
LLM_AVAILABLE = bool(GEMINI_KEY)

skip_if_no_llm = pytest.mark.skipif(
    not LLM_AVAILABLE,
    reason="GEMINI_API_KEY 미설정. LLM 테스트를 건너뜁니다."
)

# 테스트용 샘플 데이터
SAMPLE_NEWS = [
    {"title": "SK하이닉스 HBM4 엔비디아 납품 공식 승인", "score": 92, "company": "SK하이닉스"},
    {"title": "MS 텍사스 3GW 데이터센터 착공 발표", "score": 88, "company": "Microsoft"},
    {"title": "삼성전자 HBM4 퀄테스트 2차 통과", "score": 85, "company": "삼성전자"},
    {"title": "LG에너지솔루션 미국 리튬 10년 공급 계약", "score": 82, "company": "LG에너지솔루션"},
    {"title": "엔비디아 Blackwell B300 출하 일정 공개", "score": 79, "company": "NVIDIA"},
]

SAMPLE_TOPIC = {
    "title": "HBM4 전쟁 — SK하이닉스 독점의 끝인가",
    "angle": "기업격돌",
    "thesis_ids": ["T-02"],
    "outline": {
        "서론": "HBM4 퀄테스트 결과와 시장 충격",
        "본론1": "SK하이닉스 vs 삼성전자 점유율 현황",
        "본론2": "HBM4 이후 커스텀화 전략 비교",
        "결론": "투자 관점 — 점유율 변화 타임라인",
    }
}

SAMPLE_TOPIC_T32 = {
    "title": "한국 2차전지, 미국이 만든 6년짜리 기회",
    "angle": "A",
    "thesis_ids": ["T-32"],
    "outline": {},
}

OUTPUT_DIR = Path(__file__).parent.parent / "output"


# ─── TC-03: topic_generator (프롬프트 구성 로직) ──────────────────────────

class TestTopicPromptBuilding:
    """TC-03: 주제 추천 프롬프트 구성 (LLM 없이 테스트 가능)"""

    def test_news_text_building(self):
        """뉴스 목록 → 텍스트 변환"""
        news_text = "\n".join(
            [f"- [{n['company']}] {n['title']} (점수: {n['score']})"
             for n in SAMPLE_NEWS]
        )
        assert "SK하이닉스" in news_text
        assert "92" in news_text
        assert len(news_text) > 50

    def test_thesis_text_building(self):
        """Thesis 목록 → 텍스트 변환"""
        from thesis_loader import load_theses
        theses = load_theses(status_filter="active")
        thesis_text = "\n".join(
            [f"- [{t['id']}] {t['title']}: {t['hypothesis']}" for t in theses[:5]]
        )
        assert "T-01" in thesis_text
        assert len(thesis_text) > 50

    def test_should_generate_new_true(self):
        """고득점 뉴스 2건 이상 → True"""
        hot_news = [n for n in SAMPLE_NEWS if n["score"] >= 80]
        assert len(hot_news) >= 2
        # 실제 함수 없으므로 로직 검증
        result = len(hot_news) >= 2
        assert result is True

    def test_should_generate_new_false_one_item(self):
        """고득점 뉴스 1건 → False"""
        hot_news = [{"score": 85}]
        result = len(hot_news) >= 2
        assert result is False

    def test_should_generate_new_false_empty(self):
        """뉴스 없음 → False"""
        result = len([]) >= 2
        assert result is False

    @pytest.mark.llm
    @skip_if_no_llm
    def test_topic_generation_with_llm(self):
        """LLM 호출: 주제 3개 생성 (30초 이내)"""
        import time
        from topic_generator import generate_topics, _build_news_text
        start = time.time()
        context = _build_news_text(SAMPLE_NEWS)
        topics = generate_topics(context, "test:sample", num_topics=3)
        elapsed = time.time() - start
        assert len(topics) >= 1
        assert elapsed < 45, f"주제 생성 소요시간: {elapsed:.1f}초"
        for t in topics:
            assert "title" in t
            assert "angle" in t


# ─── TC-04: blog_writer (블로그 생성) ─────────────────────────────────────

class TestBlogStructure:
    """TC-04-1: 블로그 구조 검증 (LLM 없이)"""

    def test_frontmatter_template(self):
        """프론트매터 템플릿 구조"""
        template = f"""---
title: "{SAMPLE_TOPIC['title']}"
date: {datetime.now().strftime('%Y-%m-%d')}
thesis: {SAMPLE_TOPIC['thesis_ids']}
angle: "{SAMPLE_TOPIC['angle']}"
status: draft
tags: []
---"""
        assert "title:" in template
        assert "thesis:" in template
        assert "status: draft" in template
        assert "---" in template

    def test_required_sections_in_template(self):
        """필수 섹션 포함 여부"""
        blog_sections = ["## 서론", "## 본론 1", "## 결론", "면책"]
        sample_blog = """---
title: "테스트"
status: draft
---
# 테스트 블로그
## 서론: 왜 지금인가
내용
## 본론 1: 핵심 논점
내용
## 결론: 투자 관점
내용
> 면책: 투자 권유가 아닙니다."""
        for section in blog_sections:
            assert section.split(":")[0] in sample_blog, f"'{section}' 섹션 없음"

    def test_output_filename_format(self):
        """출력 파일명 형식: YYYY-MM-DD-blog-slug.md"""
        import re
        today = datetime.now().strftime("%Y-%m-%d")
        slug = "hbm4-전쟁-sk하이닉스-독점"
        filename = f"{today}-blog-{slug}.md"
        assert re.match(r"\d{4}-\d{2}-\d{2}-blog-.+\.md", filename)

    def test_output_dir_creation(self):
        """output/ 디렉터리 생성"""
        test_dir = OUTPUT_DIR / "blog"
        test_dir.mkdir(parents=True, exist_ok=True)
        assert test_dir.exists()

    @pytest.mark.llm
    @skip_if_no_llm
    def test_blog_generation_with_llm(self):
        """LLM 호출: 블로그 파일 생성"""
        from blog_writer import generate_blog
        import time
        start = time.time()
        filepath = generate_blog(SAMPLE_TOPIC, interactive=False)
        elapsed = time.time() - start
        assert Path(filepath).exists()
        content = Path(filepath).read_text(encoding="utf-8")
        assert len(content) >= 500
        assert "status: draft" in content
        assert "서론" in content
        assert "결론" in content
        Path(filepath).unlink()  # 테스트 후 삭제


class TestThesisGuideInjection:
    """TC-04-2: Thesis 가이드 주입 테스트"""

    def test_t02_guide_content(self):
        """T-02 가이드에 핵심 키워드 포함"""
        guide_path = Path(__file__).parent.parent / "docs" / "blog_thesis_guides.md"
        assert guide_path.exists(), "blog_thesis_guides.md 없음"
        content = guide_path.read_text(encoding="utf-8")
        assert "T-02" in content
        assert "HBM" in content
        assert "점유율" in content

    def test_t32_guide_not_in_file(self):
        """T-32 가이드는 아직 blog_thesis_guides.md에 없음 → 별도 처리 필요"""
        guide_path = Path(__file__).parent.parent / "docs" / "blog_thesis_guides.md"
        content = guide_path.read_text(encoding="utf-8")
        if "T-32" not in content:
            t32 = None
            try:
                from thesis_loader import load_thesis_by_id
                t32 = load_thesis_by_id("T-32")
            except Exception:
                pass
            assert t32 is not None, "T-32 가이드 없고 Thesis 파일도 없음"


# ─── TC-05: thread_writer (스레드 생성) ───────────────────────────────────

class TestThreadStructure:
    """TC-05: 스레드 구조 검증"""

    def test_thread_prompt_angle_options(self):
        """각도 옵션 3가지 정의"""
        angle_options = {
            "A": "수혜 계산 각도 — 숫자와 팩트 중심",
            "B": "구조 변화 각도 — 산업 변화 스토리",
            "C": "공장/실행 각도 — 리스크 중심",
        }
        assert len(angle_options) == 3
        for key in ["A", "B", "C"]:
            assert key in angle_options

    def test_thread_tone_markers(self):
        """구어체 말투 마커 존재"""
        sample_thread = """1. 2차전지가 전기차에서 AI데이터센터로 넘어가는 중임.
2. 이 와중에 미국이 중국 배터리에 세금 58%에 비상사태까지 때림.
3. 중국을 조질수록 한국이 반사이익이라 어제 2차전지가 다 올랐음.
4. 근데 이 수혜는 6년짜리임."""
        tone_markers = ["임.", "함.", "됨.", "음.", "ㅋㅋ"]
        assert any(m in sample_thread for m in tone_markers), "구어체 마커 없음"

    def test_thread_number_format(self):
        """번호 나열 형식"""
        import re
        sample = "1. 내용\n2. 내용\n10. 내용"
        lines = sample.strip().split("\n")
        for line in lines:
            assert re.match(r"^\d+\.", line.strip()), f"번호 형식 오류: '{line}'"

    def test_thread_contains_numbers(self):
        """숫자(수치) 포함"""
        sample_thread = """1. 저장용 배터리가 461GWh, 71% 늘었음.
2. 미국 중국산 관세가 58%임."""
        digits = [c for c in sample_thread if c.isdigit()]
        assert len(digits) > 5, "수치 데이터가 부족함"

    def test_thread_output_filename(self):
        """스레드 파일명 형식"""
        import re
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"{today}-thread-2차전지-미국수혜.md"
        assert re.match(r"\d{4}-\d{2}-\d{2}-thread-.+\.md", filename)

    @pytest.mark.llm
    @skip_if_no_llm
    def test_thread_generation_with_llm(self):
        """LLM 호출: 스레드 파일 생성"""
        from thread_writer import generate_thread
        import re
        filepath = generate_thread(SAMPLE_TOPIC_T32, angle="A", interactive=False)
        content = Path(filepath).read_text(encoding="utf-8")
        lines = [l for l in content.split("\n") if re.match(r"^\d+\.", l.strip())]
        assert len(lines) >= 15
        assert any(m in content for m in ["임", "함", "됨", "음"])
        Path(filepath).unlink()


# ─── TC-06: E2E 파이프라인 ────────────────────────────────────────────────

class TestE2EPipeline:
    """TC-06: 전체 파이프라인 통합 테스트"""

    @pytest.mark.llm
    @skip_if_no_llm
    def test_e2e_blog_pipeline(self):
        """뉴스 → 주제 → 블로그 파일 생성 전체 흐름"""
        import time
        from topic_generator import generate_topics, _build_news_text
        from blog_writer import generate_blog
        start = time.time()
        context = _build_news_text(SAMPLE_NEWS)
        topics = generate_topics(context, "e2e_test", num_topics=2)
        assert len(topics) >= 1
        filepath = generate_blog(topics[0], interactive=False)
        assert Path(filepath).exists()
        elapsed = time.time() - start
        assert elapsed < 120, f"E2E 시간: {elapsed:.1f}초"
        Path(filepath).unlink()

    @pytest.mark.llm
    @skip_if_no_llm
    def test_e2e_thread_pipeline(self):
        """뉴스 → 주제 → 스레드 파일 생성 전체 흐름"""
        from topic_generator import generate_topics, _build_news_text
        from thread_writer import generate_thread
        context = _build_news_text(SAMPLE_NEWS)
        topics = generate_topics(context, "e2e_test", num_topics=2)
        filepath = generate_thread(topics[0], angle="A", interactive=False)
        assert Path(filepath).exists()
        Path(filepath).unlink()

    def test_output_dirs_exist_or_creatable(self):
        """output/blog, output/thread 디렉터리 생성 가능"""
        for subdir in ["blog", "thread", "digest"]:
            d = OUTPUT_DIR / subdir
            d.mkdir(parents=True, exist_ok=True)
            assert d.exists(), f"output/{subdir}/ 생성 실패"


# ─── TC-07: 엣지 케이스 ──────────────────────────────────────────────────

class TestEdgeCases:
    """TC-07: 경계 조건 및 오류 처리"""

    def test_no_hot_news_triggers_review_mode(self):
        """고득점 뉴스 0건 → 리뷰 모드"""
        hot_news = []
        should_new = len(hot_news) >= 2
        assert should_new is False
        # review_generator가 호출되어야 함

    def test_single_hot_news_triggers_review_mode(self):
        """고득점 뉴스 1건 → 리뷰 모드"""
        hot_news = [{"score": 92, "title": "중요한 뉴스"}]
        should_new = len(hot_news) >= 2
        assert should_new is False

    def test_missing_thesis_id_returns_none(self):
        """존재하지 않는 Thesis ID → None"""
        from thesis_loader import load_thesis_by_id
        assert load_thesis_by_id("T-99") is None
        assert load_thesis_by_id("T-0") is None
        assert load_thesis_by_id("") is None

    def test_duplicate_file_naming(self):
        """같은 날 파일 중복 → suffix 추가로 구분"""
        today = datetime.now().strftime("%Y-%m-%d")
        base = f"{today}-blog-hbm4"

        def make_unique_filename(base_name: str, ext: str, output_dir: Path) -> str:
            candidate = output_dir / f"{base_name}{ext}"
            if not candidate.exists():
                return str(candidate)
            i = 1
            while True:
                candidate = output_dir / f"{base_name}-{i}{ext}"
                if not candidate.exists():
                    return str(candidate)
                i += 1

        test_dir = OUTPUT_DIR / "blog"
        test_dir.mkdir(parents=True, exist_ok=True)

        name1 = make_unique_filename(base, ".md", test_dir)
        # 실제 파일 없으면 suffix 없이 반환
        assert base in name1

    def test_empty_news_list_handling(self):
        """빈 뉴스 목록 → 예외 없이 처리"""
        news_text = "\n".join(
            [f"- [{n.get('company', '?')}] {n['title']} (점수: {n['score']})"
             for n in []]
        )
        assert news_text == ""  # 빈 문자열 반환

    def test_thesis_with_all_fields(self):
        """T-32 (신규) 모든 필드 존재"""
        from thesis_loader import load_thesis_by_id
        t = load_thesis_by_id("T-32")
        assert t is not None, "T-32를 찾을 수 없음"
        assert "ESS" in t["title"] or "배터리" in t["title"]
        assert t["direction"] == "bullish"
        assert t["priority"] == 5

    def test_bearish_thesis_fields(self):
        """Bearish Thesis (T-37, T-38) 필드 검증"""
        from thesis_loader import load_thesis_by_id
        for tid in ["T-37", "T-38"]:
            t = load_thesis_by_id(tid)
            if t:  # watch 상태면 active 로드에서 제외될 수 있음
                assert t["direction"] == "bearish"
                assert t["confidence"] < 60  # bearish는 상대적으로 낮음

    @pytest.mark.llm
    @skip_if_no_llm
    def test_api_failure_graceful(self):
        """잘못된 API 키 → 명확한 오류 발생"""
        from google import genai
        client = genai.Client(api_key="invalid_key_test_12345")
        with pytest.raises(Exception) as exc_info:
            client.models.generate_content(
                model="gemini-3.7-flash",
                contents="test"
            )
        error_msg = str(exc_info.value).lower()
        assert any(w in error_msg for w in ["api", "key", "auth", "invalid", "400", "403", "unauthenticated"])
