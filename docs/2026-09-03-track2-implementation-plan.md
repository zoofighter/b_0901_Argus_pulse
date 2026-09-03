# 트랙 2: 심층 엔진 고도화 — 구현 계획서

> **작성일**: 2026-09-03  
> **Phase**: 설계서 Phase 4 ("RAG + LangGraph", 콘텐츠 50편+ 후)를 현 시점에 맞게 재설계  
> **목표**: 단순 뉴스 요약 → **증권사 리포트·웹 자료를 근거로 인용하는 '장기 시장 인텔리전스 엔진'**으로 진화

---

## 현재 상태 점검

### ✅ 완료된 것 (Phase 1~3)
- 핵심 생성 파이프라인 전체: `topic_generator → blog_writer / thread_writer → obsidian_sync`
- 듀얼 LLM 대체(Gemini + Muse-Spark), 디스코드 알림, 자동화 스케줄러
- Thesis 38개 등록, 뉴스 DB 연동, 아카이빙 시스템
- 통합 런처 `argus.py` / `run.sh`

### ❌ 미구현 (Phase 4 — 본 계획의 범위)
| 기능 | 설계 문서 참조 | 현재 상태 |
|---|---|---|
| **ChromaDB 벡터 인제스트** | [`requirements_spec.md` FR-01, FR-03](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/docs/requirements_spec.md) | `db/` 폴더 비어 있음, chromadb 미설치 |
| **PDF 리포트 파싱** | [`requirements_spec.md` R-01](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/docs/requirements_spec.md) | PDF 42개 존재(`a_langragh/reports/`), 파서 미구현 |
| **RAG 검색 엔진** | [`wiki-vs-rag.md`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/docs/2026-09-02-wiki-vs-rag.md) | 하이브리드 RAG 결론 확정됨, 코드 미작성 |
| **Thesis Confidence 자동 갱신** | [`thesis_management.md` §5.ⓑ](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/docs/thesis_management.md) | `update_thesis_confidence()` 함수 있으나 자동 호출 미연결 |
| **블로그 작성 시 RAG 컨텍스트 주입** | [`wiki-vs-rag.md` 하이브리드 설계](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/docs/2026-09-02-wiki-vs-rag.md) | 현재 뉴스만 참조, 과거 리포트 인용 불가 |
| **생성 콘텐츠 재인제스트 (지식 순환)** | [`requirements_spec.md` R-10, R-14](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/docs/requirements_spec.md) | 미구현 |

### 🔍 인프라 현황
- **이미 설치됨**: `google-genai`, `transformers`, `langchain-core`, `langsmith`
- **설치 필요**: `chromadb`, `pymupdf` (또는 `pdfplumber`), `sentence-transformers` (임베딩)
- **PDF 자산**: `/Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/a_langragh/reports/2026-04-08/` 에 증권사 리포트 42개

---

## 구현 로드맵 (3단계)

### Step 1: PDF 파서 + ChromaDB 인제스트 파이프라인 구축

> 증권사 리포트 PDF를 텍스트로 추출하고, ChromaDB 벡터 DB에 청킹+임베딩하여 저장

#### [NEW] `pdf_parser.py`
- PyMuPDF(`fitz`)로 PDF → 텍스트 추출
- 테이블 감지: 표 형태 데이터를 마크다운 테이블로 변환 시도
- 메타데이터 자동 추출: 파일명에서 날짜, 종목명, 증권사명 파싱
  - 파일명 패턴: `26.04.08_삼성전자_키움증권_너무 좋아도 걱정.pdf`
  - → `{"date": "2026-04-08", "company": "삼성전자", "broker": "키움증권", "title": "너무 좋아도 걱정"}`

#### [NEW] `rag_engine.py`
- ChromaDB 로컬 영속 저장소 (`db/chromadb/`)
- 2개 컬렉션 구성 ([`wiki-vs-rag.md`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/docs/2026-09-02-wiki-vs-rag.md) 설계 그대로):
  - `argus_knowledge`: 기초 지식 (PDF 리포트, 웹 자료, 99.raw 파싱본)
  - `argus_reports`: 축적 지식 (시스템이 생성한 블로그/스레드/다이제스트)
- 청킹: 1,000자 단위, 200자 오버랩
- 임베딩: Gemini `text-embedding-004` (무료 티어 충분) 또는 `sentence-transformers` 로컬
- 중복 방지: SHA256 해시 기반 이미 인제스트된 파일 스킵

#### [NEW] `ingest.py` (CLI 인제스트 도구)
```bash
python ingest.py --pdf ../a_langragh/reports/    # PDF 폴더 일괄 인제스트
python ingest.py --raw 99.raw/                    # 수동 자료 인제스트
python ingest.py --output                         # 생성 콘텐츠 재인제스트 (지식 순환)
python ingest.py --status                         # DB 현황 조회
```

#### [MODIFY] `config.py`
- `CHROMA_DB_PATH`, `EMBEDDING_MODEL`, `CHUNK_SIZE`, `CHUNK_OVERLAP` 설정 추가
- `PDF_REPORTS_DIR` 경로 추가

---

### Step 2: RAG 컨텍스트를 블로그/스레드 생성에 주입

> 블로그를 쓸 때 **"뉴스 + 과거 증권사 리포트에서 관련 수치와 분석"**을 함께 참조

#### [MODIFY] `blog_writer.py`
- `build_blog_prompt()` 함수에 RAG 검색 결과 주입 섹션 추가:
  ```
  [관련 증권사 리포트 인사이트]
  - 삼성전자_키움증권 (2026-04-08): "HBM4 점유율 확대에 따라..."
  - SK하이닉스_하나증권 (2026-04-08): "DRAM ASP 상승률 전분기 대비..."
  ```
- `rag_engine.search()` 호출로 Thesis 키워드 + 주제 관련 상위 5개 청크 검색

#### [MODIFY] `thread_writer.py`
- 동일하게 RAG 컨텍스트 주입 (스레드는 압축 인용)

#### [MODIFY] `review_generator.py`
- 리뷰 시 **원래 블로그 작성 당시 참조했던 리포트 + 이후 발행된 리포트** 양쪽 대조

---

### Step 3: Thesis Confidence 자동 갱신 루프

> 매일 21:00 다이제스트 생성 후, 각 active Thesis의 신뢰도를 뉴스+RAG 근거로 자동 재평가

#### [NEW] `thesis_checker.py`
- 각 active Thesis에 대해:
  1. 최근 7일 관련 뉴스 수집 (기존 `hourly_monitor` 로직 재활용)
  2. RAG에서 관련 증권사 리포트 청크 검색
  3. LLM에게 "지지 근거 / 반박 근거 / 신뢰도 변화량(±0~15)" 판단 요청
  4. `thesis_loader.update_thesis_confidence()` 호출하여 실제 Thesis MD 파일 갱신
  5. 지지/반박 근거를 Thesis 파일의 `## 지지 근거` / `## 반박 근거` 섹션에 자동 추가
- **안전 장치**: 1회 최대 ±15 변동 제한, 사용자 확인 없이 `status` 변경 불가

#### [MODIFY] `scheduler.py`
- 21:00 다이제스트 생성 직후 `thesis_checker.py` 자동 호출 추가

#### [MODIFY] `daily_digest.py`
- 다이제스트 하단에 "오늘의 Thesis 신뢰도 변화 요약" 섹션 자동 삽입

---

## 파일 구조 (구현 후)

```
b_0901_Argus_pulse/
├── (기존 파일들 유지)
├── pdf_parser.py          ← [NEW] PDF 텍스트 추출 + 메타데이터 파싱
├── rag_engine.py          ← [NEW] ChromaDB 벡터 검색 엔진 (인제스트 + 검색)
├── ingest.py              ← [NEW] CLI 인제스트 도구 (PDF/자료/생성물)
├── thesis_checker.py      ← [NEW] Thesis 자동 점검 및 Confidence 갱신
├── db/
│   └── chromadb/           ← [NEW] ChromaDB 영속 저장소
└── (수정 파일: config.py, blog_writer.py, thread_writer.py, 
     review_generator.py, scheduler.py, daily_digest.py)
```

---

## 구현 우선순위

> [!IMPORTANT]
> ### 사용자 검토 필요
> 1. **임베딩 모델 선택**: Gemini `text-embedding-004` (API, 무료 티어 1,500 RPM) vs `sentence-transformers` (로컬, 오프라인 가능)?
> 2. **PDF 리포트 경로 확정**: `a_langragh/reports/` 폴더 42개 PDF를 그대로 사용할지, 별도 폴더로 복사할지?
> 3. **Thesis Confidence 자동 갱신 범위**: active 9개 Thesis만 대상? 또는 watch 포함 전체 38개?

---

## 검증 계획

### 자동화 테스트
```bash
pytest tests/test_rag.py          # ChromaDB 인제스트/검색 단위 테스트
pytest tests/test_pdf_parser.py   # PDF 파싱 정확도 테스트
pytest -m "not llm"               # 기존 62개 테스트 회귀 확인
```

### 수동 검증
1. 삼성전자 관련 PDF 3개 인제스트 후 `rag_engine.search("HBM4 점유율")` 검색 정확도 확인
2. RAG 컨텍스트 주입된 블로그와 주입 없는 블로그의 품질 비교 (수치 인용 여부)
3. `thesis_checker.py` 실행 후 Thesis MD 파일의 `confidence` 값 변화 및 근거 추가 확인
