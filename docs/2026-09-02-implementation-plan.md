# Argus Pulse — 구현 계획서 (상세)

> **작성일**: 2026-09-02  
> **버전**: v1.0  
> **목적**: 설계 완료된 Argus Pulse 시스템의 단계별 구현 계획 및 테스트 기준 정의

---

## 1. 현황 점검 (2026-09-02 기준)

### ✅ 완료된 것

| 항목 | 상태 | 위치 |
|---|---|---|
| Thesis 파일 38개 (T-01~T-38) | ✅ 완료 | `thesis/` |
| `thesis_loader.py` | ✅ 동작 확인 | 루트 |
| 프롬프트 설계 5종 (P-01~P-05) | ✅ 설계 완료 | `docs/2026-09-02-prompt-design.md` |
| 블로그 템플릿 & Thesis 가이드 | ✅ 설계 완료 | `docs/blog_writing_template.md` |
| 워크플로우 계획 | ✅ 설계 완료 | `docs/2026-09-02-workflow-plan.md` |

### ❌ 미결 사항 (구현 전 필수)

| 항목 | 이유 | 조치 |
|---|---|---|
| **Gemini API 키** | LLM 호출 불가 | `.env` 파일에 `GEMINI_API_KEY=` 설정 |
| **b_0826 SQLite DB 경로** | 뉴스 데이터 없음 | `db/` 폴더 비어 있음 — 경로 연결 필요 |
| **옵시디언 Vault 경로** | 산출물 저장 불가 | 로컬 옵시디언 폴더 경로 확인 |
| **디스코드 웹훅 URL** | 알림 채널 없음 | `.env`에 `DISCORD_WEBHOOK_URL=` 설정 |

---

## 2. 아키텍처 최종 확정

```
[b_0826 SQLite]     [thesis/ MD 38개]     [ChromaDB (향후)]
      ↓                    ↓                      ↓
      └──────────────────────────────────────────┘
                           ↓
                  topic_generator.py
                  (P-01: 주제 추천)
                           ↓
              🧑 Human in the Loop (각도 선택)
                           ↓
              ┌────────────┴────────────┐
              ↓                         ↓
        blog_writer.py          thread_writer.py
        (P-02+P-03: 블로그)     (P-04: 스레드)
              └────────────┬────────────┘
                           ↓
                  옵시디언 저장 + 디스코드 알림
                           ↓
              (새 뉴스 없는 날: review_generator.py)
                           ↓
                  ChromaDB 재인제스트 (향후)
```

**에이전트 구성 여부**: Phase 1은 단순 스크립트. LangGraph는 Phase 4 이후.

---

## 3. 구현 로드맵

### Phase 1: 핵심 생성 파이프라인 (Day 1~3)

#### Day 1: 환경 설정 및 뉴스 연결

**목표**: 뉴스 데이터를 Python에서 읽을 수 있는 상태

```
tasks:
  1. .env 파일 생성 (API 키, 경로, 웹훅)
  2. b_0826 SQLite DB 경로 확인 및 연결 테스트
  3. thesis_loader.py 동작 확인 (이미 완료)
  4. config.py 작성
```

**config.py 구조**:
```python
# config.py
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# 경로
ROOT_DIR       = Path(__file__).parent
THESIS_DIR     = ROOT_DIR / "thesis"
OUTPUT_DIR     = ROOT_DIR / "output"
NEWS_DB_PATH   = Path(os.getenv("NEWS_DB_PATH", "../b_0826_news_research/db/news.sqlite"))
OBSIDIAN_PATH  = Path(os.getenv("OBSIDIAN_PATH", "~/Documents/Obsidian/Argus"))

# API
GEMINI_API_KEY     = os.getenv("GEMINI_API_KEY")
DISCORD_WEBHOOK    = os.getenv("DISCORD_WEBHOOK_URL")

# 설정
NEWS_SCORE_THRESHOLD = 70   # 고득점 뉴스 기준
NEWS_HOT_THRESHOLD   = 80   # 새 블로그 생성 트리거 기준
NEWS_LOOKBACK_DAYS   = 2    # 최근 N일 뉴스 참조
MAX_NEWS_FOR_PROMPT  = 15   # 프롬프트에 넣을 최대 뉴스 수
```

#### Day 2: topic_generator.py (P-01)

**목표**: 터미널에서 "오늘의 주제 3~5개" 출력

```python
# topic_generator.py 구조
def load_recent_hot_news(db_path, days, threshold, limit) -> list[dict]
def load_active_theses() -> list[dict]          # thesis_loader.py 활용
def build_topic_prompt(news, theses) -> str      # P-01 프롬프트
def call_gemini(prompt) -> str
def parse_topics(response) -> list[dict]         # JSON 파싱
def display_topics(topics)                       # 터미널 출력
def should_generate_new(news) -> bool            # 고득점 뉴스 >= 2건?
def main()
```

**실행 방식**:
```bash
$ python topic_generator.py
# 출력: 주제 3~5개 + 번호 입력 대기
# 입력: 1 → blog_writer.py 자동 호출
#       2t → thread_writer.py 자동 호출
#       s → 건너뜀 (review_generator.py로 전환)
```

#### Day 3: blog_writer.py + thread_writer.py (P-02, P-04)

**목표**: 선택한 주제로 블로그/스레드 파일 생성

```python
# blog_writer.py 구조
def load_thesis_guide(thesis_ids) -> str         # blog_thesis_guides.md 로드
def build_blog_prompt(outline, guide, news) -> str  # P-02+P-03 프롬프트
def call_gemini(prompt) -> str
def save_to_obsidian(content, filename)
def send_to_discord(title, excerpt, filepath)
def main(selected_topic: dict, format: str)

# thread_writer.py 구조  
def build_thread_prompt(outline, angle, news) -> str  # P-04 프롬프트
def show_intro_preview(lines_1_to_5)             # 도입부 확인 (HitL)
def show_outro_preview(last_5_lines)             # 결말 확인 (HitL)
def main(selected_topic: dict, angle: str)
```

**산출물 파일명 규칙**:
```
blog:   output/YYYY-MM-DD-blog-{slug}.md
thread: output/YYYY-MM-DD-thread-{slug}.md
```

---

### Phase 2: 자동화 + 모니터링 (Day 4~6)

#### Day 4~5: hourly_monitor.py

```python
# hourly_monitor.py
def collect_news()          # b_0826 수집기 호출
def score_and_match(news)   # 4축 스코어링 + Thesis 매칭
def alert_urgent(news)      # 점수 80+ → 즉시 디스코드 알림
def save_to_daily_log()     # 일간 로그 누적

# 크론 설정
# 0 9-21 * * * cd /path && python hourly_monitor.py
```

#### Day 6: daily_digest.py

```python
# daily_digest.py
def load_daily_log()
def group_by_thesis()
def generate_digest()       # LLM으로 Thesis별 오늘의 변화 정리
def save_and_send()

# 크론 설정
# 0 15 * * * python daily_digest.py --mode midday
# 0 21 * * * python daily_digest.py --mode full
```

---

### Phase 3: 과거 블로그 리뷰 (Day 7~8, 콘텐츠 10편+ 후)

```python
# review_generator.py
def select_review_target(output_dir) -> dict     # 선정 기준 적용
def build_review_prompt(original, recent_news) -> str  # P-05 프롬프트
def generate_review() -> str
def save_review()
```

**리뷰 대상 선정 로직**:
```python
# 우선순위 점수 계산
score = 0
if days_elapsed in [30, 90, 180]:  score += 30   # milestone
if abs(confidence_delta) >= 20:    score += 40   # confidence 변화
if days_since_last_review > 60:    score += 20   # 방치 기간
if original_confidence < 60:      score += 10   # 당시 불확실성
```

---

### Phase 4: RAG + LangGraph (미래, 콘텐츠 50편+ 후)

```
- ChromaDB 인제스트 파이프라인 (PDF + 웹 + 산출물)
- LangGraph 멀티에이전트 전환
- Thesis Confidence 자동 업데이트
```

---

## 4. 파일 구조 (구현 후)

```
b_0901_Argus_pulse/
├── .env                        ← API 키, 경로 (gitignore)
├── config.py                   ← 설정 중앙화
├── thesis_loader.py            ← ✅ 완료
├── topic_generator.py          ← Phase 1 (Day 2)
├── blog_writer.py              ← Phase 1 (Day 3)
├── thread_writer.py            ← Phase 1 (Day 3)
├── hourly_monitor.py           ← Phase 2 (Day 4~5)
├── daily_digest.py             ← Phase 2 (Day 6)
├── review_generator.py         ← Phase 3 (Day 7~8)
├── notifier.py                 ← 디스코드/텔레그램 공통 모듈
├── thesis/                     ← ✅ 38개 완료
├── output/                     ← 생성된 블로그/스레드/다이제스트
│   ├── blog/
│   ├── thread/
│   └── digest/
├── logs/                       ← 일간 뉴스 로그
└── docs/                       ← ✅ 설계 문서 26개
```

---

## 5. 테스트 케이스

### TC-01: thesis_loader.py 기본 동작

```python
# test_thesis_loader.py
def test_load_all():
    """전체 Thesis 로드"""
    theses = load_theses(status_filter=None)
    assert len(theses) == 38, f"38개 기대, {len(theses)}개 로드됨"

def test_load_active():
    """active 상태만 로드"""
    theses = load_theses(status_filter="active")
    assert all(t["status"] == "active" for t in theses)

def test_load_by_id():
    """특정 ID 로드"""
    t = load_thesis_by_id("T-01")
    assert t["id"] == "T-01"
    assert t["confidence"] == 80
    assert "데이터센터" in t["keywords"]

def test_keyword_map():
    """키워드 맵 생성"""
    kmap = get_active_keywords()
    assert "T-01" in kmap
    assert isinstance(kmap["T-01"], list)

def test_update_confidence():
    """Confidence 업데이트"""
    original = load_thesis_by_id("T-01")["confidence"]
    update_thesis_confidence("T-01", original + 5)
    updated = load_thesis_by_id("T-01")["confidence"]
    assert updated == original + 5
    update_thesis_confidence("T-01", original)  # 원복
```

**합격 기준**: 전체 통과, 실행 3초 이내

---

### TC-02: 뉴스 DB 연결

```python
def test_news_db_connection():
    """SQLite 연결 및 기본 쿼리"""
    conn = get_news_db()
    result = conn.execute("SELECT COUNT(*) FROM news").fetchone()
    assert result[0] > 0, "뉴스 데이터가 없음"

def test_hot_news_query():
    """고득점 뉴스 조회"""
    news = load_recent_hot_news(days=2, threshold=60, limit=15)
    assert isinstance(news, list)
    assert all(n["score"] >= 60 for n in news)
    assert len(news) <= 15

def test_thesis_matching():
    """Thesis 키워드 매칭"""
    news = {"title": "SK하이닉스 HBM4 엔비디아 납품 승인"}
    matched = match_thesis(news, get_active_keywords())
    assert "T-02" in matched  # 메모리 Thesis 매칭 확인
```

**합격 기준**: 전체 통과, DB 연결 1초 이내

---

### TC-03: topic_generator.py (LLM 호출)

```python
def test_topic_generation():
    """블로그 주제 3~5개 생성"""
    topics = generate_blog_topics(days=2, num_topics=3)
    assert len(topics) >= 3
    for t in topics:
        assert "title" in t
        assert "angle" in t      # 4대 관점 중 하나
        assert "thesis_ids" in t  # 관련 Thesis ID
        assert "outline" in t    # 2-Page 목차

def test_angle_variety():
    """관점이 다양하게 나오는지"""
    topics = generate_blog_topics(num_topics=5)
    angles = [t["angle"] for t in topics]
    assert len(set(angles)) >= 2  # 최소 2가지 다른 관점

def test_trigger_condition():
    """새 블로그 생성 여부 판단"""
    assert should_generate_new([{"score": 85}, {"score": 82}]) == True
    assert should_generate_new([{"score": 85}]) == False  # 1건 미달
    assert should_generate_new([]) == False
```

**합격 기준**: 전체 통과, LLM 응답 30초 이내

---

### TC-04: blog_writer.py (블로그 생성)

```python
def test_blog_generation():
    """블로그 파일 생성"""
    sample_topic = {
        "title": "HBM4 전쟁, SK하이닉스 독점의 끝?",
        "thesis_ids": ["T-02"],
        "angle": "기업격돌",
        "outline": "서론-본론1-본론2-결론"
    }
    filepath = generate_blog(sample_topic)
    assert Path(filepath).exists()
    content = Path(filepath).read_text()
    
    # 프론트매터 확인
    assert "title:" in content
    assert "thesis:" in content
    assert "status: draft" in content
    
    # 구조 확인
    assert "## 서론" in content
    assert "## 결론" in content
    assert "면책" in content
    
    # 길이 확인 (최소 800자)
    assert len(content) >= 800

def test_thesis_guide_injection():
    """T-02 Thesis 가이드가 프롬프트에 포함되는지"""
    guide = load_thesis_guide(["T-02"])
    assert "HBM" in guide
    assert "점유율" in guide
```

**합격 기준**: 파일 생성 성공, 구조 요소 포함, 60초 이내

---

### TC-05: thread_writer.py (스레드 생성)

```python
def test_thread_generation():
    """스레드 파일 생성"""
    sample_topic = {
        "title": "한국 2차전지, 미국이 만든 6년짜리 기회",
        "thesis_ids": ["T-32"],
        "angle": "A"  # 수혜 계산 각도
    }
    filepath = generate_thread(sample_topic, angle="A")
    content = Path(filepath).read_text()
    
    # 번호 나열 형식 확인
    assert "1." in content
    assert "2." in content
    
    # 구어체 확인
    assert any(w in content for w in ["임.", "함.", "됨.", "음."])
    
    # 숫자 포함 확인
    assert any(c.isdigit() for c in content)

def test_thread_length():
    """스레드 적정 길이 (30~150번)"""
    lines = [l for l in content.split("\n") if l.strip().startswith(tuple("0123456789"))]
    assert 30 <= len(lines) <= 160
```

**합격 기준**: 파일 생성 성공, 구어체·숫자 포함, 60초 이내

---

### TC-06: 전체 파이프라인 통합 테스트 (E2E)

```python
def test_e2e_blog_pipeline():
    """전체 흐름: 뉴스 → 주제 추천 → 블로그 생성 → 파일 저장"""
    # Step 1: 뉴스 로드
    news = load_recent_hot_news(days=2, threshold=60, limit=10)
    assert len(news) > 0, "테스트용 뉴스 필요"
    
    # Step 2: 주제 생성
    topics = generate_blog_topics(news=news, num_topics=3)
    assert len(topics) >= 1
    
    # Step 3: 첫 번째 주제로 블로그 생성
    filepath = generate_blog(topics[0])
    assert Path(filepath).exists()
    
    # Step 4: 파일 내용 검증
    content = Path(filepath).read_text()
    assert len(content) >= 500
    
    print(f"✅ E2E 통과: {filepath}")

def test_e2e_thread_pipeline():
    """전체 흐름: 뉴스 → 주제 추천 → 스레드 생성 → 파일 저장"""
    news = load_recent_hot_news(days=2, threshold=60, limit=10)
    topics = generate_blog_topics(news=news, num_topics=3)
    filepath = generate_thread(topics[0], angle="A")
    assert Path(filepath).exists()
    print(f"✅ E2E Thread 통과: {filepath}")
```

**합격 기준**: 전체 흐름 완주, 총 120초 이내

---

### TC-07: 엣지 케이스

```python
def test_no_hot_news():
    """고득점 뉴스가 없는 날 → 리뷰 모드 전환"""
    hot_news = []
    assert should_generate_new(hot_news) == False
    # review_generator 호출되는지 확인

def test_missing_thesis_id():
    """존재하지 않는 Thesis ID"""
    result = load_thesis_by_id("T-99")
    assert result is None

def test_gemini_api_failure():
    """API 키 오류 시 graceful 처리"""
    with pytest.raises(Exception) as exc:
        call_gemini("test", api_key="invalid")
    assert "API" in str(exc.value)

def test_duplicate_date_file():
    """같은 날 두 번 실행 시 파일 덮어쓰기 방지"""
    topic = {"title": "테스트", "thesis_ids": ["T-01"]}
    filepath1 = generate_blog(topic)
    filepath2 = generate_blog(topic)
    assert filepath1 != filepath2  # 번호 suffix 추가됨
```

---

## 6. 구현 체크리스트

```
Phase 1 (Day 1~3):
[ ] .env 파일 작성 (API 키, DB 경로, 웹훅)
[ ] config.py 작성
[ ] 뉴스 DB 연결 테스트 (TC-02 통과)
[ ] topic_generator.py 구현 (TC-03 통과)
[ ] blog_writer.py 구현 (TC-04 통과)
[ ] thread_writer.py 구현 (TC-05 통과)
[ ] E2E 테스트 (TC-06 통과)

Phase 2 (Day 4~6):
[ ] notifier.py 구현 (디스코드 전송)
[ ] hourly_monitor.py 구현
[ ] daily_digest.py 구현
[ ] crontab 설정

Phase 3 (Day 7~8):
[ ] review_generator.py 구현
[ ] 리뷰 대상 선정 로직 구현
```

---

## 7. 비용 추정

| 항목 | 월 비용 (Gemini Flash 기준) |
|---|---|
| 주제 추천 (1~2회/일 × 30일) | ~$0.5 |
| 블로그 생성 (1편/일 × 30일) | ~$0.5 |
| 스레드 생성 (0~1편/일 × 30일) | ~$0.3 |
| 리뷰 생성 (뉴스 없는 날, ~10회/월) | ~$0.2 |
| 데일리 다이제스트 (2회/일 × 30일) | ~$1.0 |
| **월 합계** | **약 $2.5~3/월** |
