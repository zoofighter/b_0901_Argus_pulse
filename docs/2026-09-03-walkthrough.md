# 🦅 Argus Pulse 트랙 2 심층 엔진 및 품질 검수 고도화 완료 워크스루

> **완료일**: 2026-09-03  
> **상태**: 구현 및 실증 테스트 전원 통과 (72/72 Tests Passed)

---

## 1. 구현 개요

단순 뉴스 요약 수준을 넘어, **42개 증권사 리서치 리포트와 자체 축적 콘텐츠를 기억·인용(RAG)하고, 투자 가설(Thesis)의 유효성을 매일 스스로 검증하며, AI 검수위원(Critic)이 팩트체크를 수행하는 차세대 인텔리전스 엔진**으로 고도화를 완료했습니다.

```
[Argus Pulse 심층 인텔리전스 아키텍처]

       [42개 증권사 리포트 (PDF)]          [자체 생성 산출물 (Blog/Digest)]
                 │                                      │
                 ▼                                      ▼
        [pdf_parser.py]                        [지식 순환 루프]
                 │                                      │
                 └──────────────┬───────────────────────┘
                                ▼
                    [rag_engine.py (ChromaDB)]
                    - argus_knowledge: 648개 청크
                    - argus_reports  : 17개 청크
                    👉 총 665개 지식 청크 보유
                                │
                 ┌──────────────┴──────────────┐
                 ▼                             ▼
        [--rag 옵션 활성화]            [thesis_checker.py]
        - blog_writer.py               - 뉴스 팩트 + RAG 대조
        - thread_writer.py             - 신뢰도 (±15%) 자동 갱신
        - daily_digest.py              - 지지/반박 근거 자동 기록
        - review_generator.py          - 옵시디언 Theses/ 동기화
                 │
                 ▼
          [critic.py (AI 검수위원)]
          - 5대 기준 100점 만점 채점
          - 80점 미만 시 자동 1회 수정(Refine) 후 발행
```

---

## 2. 신규 생성 및 수정된 핵심 모듈

| 모듈 | 파일 | 설명 |
|---|---|---|
| **증권사 PDF 파서** | [`pdf_parser.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/pdf_parser.py) | 파일명 메타데이터(일자, 기업, 증권사, 제목) 파싱 및 본문 텍스트 자동 추출 |
| **RAG 벡터 엔진** | [`rag_engine.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/rag_engine.py) | ChromaDB 영속 저장소 (`db/chromadb/`) 및 고속 로컬 ONNX 임베딩 검색 |
| **지식 인제스트 CLI** | [`ingest.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/ingest.py) | `--pdf`, `--raw`, `--output`, `--status` 일괄 인제스트 도구 |
| **Thesis 자동 점검기** | [`thesis_checker.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/thesis_checker.py) | 가설 지지/반박 팩트 수집 및 신뢰도 자동 갱신 |
| **품질 검수 위원** | [`critic.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/critic.py) | 5대 기준(팩트 밀도, 인용, 표 구조, 톤, 결론) 100점 만점 검수 및 자동 보완 |

---

## 3. 주요 기능 및 사용법

### 1) RAG 사용 / 미사용 선택 (`--rag` 토글)
```bash
# 기본 모드 (빠른 속보성 생성: 약 5~10초)
python blog_writer.py --topic '...'

# RAG 심층 모드 (증권사 리포트 수치 및 출처 인용)
python blog_writer.py --topic '...' --rag

# 주제 추천기 HitL 대화형 메뉴에서 선택 가능
# 1b : 일반 블로그
# 1br: RAG 심층 블로그
# 2t : 일반 스레드
# 2tr: RAG 심층 스레드
```

### 2) Critic(품질 자가 검수) 결합
```bash
# RAG 리포트 인용 + Critic 품질 자가 검수 및 자동 보완 루프 실행
python blog_writer.py --topic '...' --rag --critic
```

### 3) 스레드 분량 선택 (`--length`)
```bash
# 모바일 완독형 (10~15줄 압축 스레드)
python thread_writer.py --topic '...' --angle A --length compact

# 심층 리포트형 (25~35줄 롱폼 스레드, 기본값)
python thread_writer.py --topic '...' --angle A --length deep
```

### 4) Thesis 가설 자동 점검
```bash
# Active Thesis 전체 자동 점검 및 마크다운 파일 갱신
python thesis_checker.py

# 특정 Thesis 지정 점검
python thesis_checker.py --id T-02
```

---

## 4. 검증 결과

### 1) RAG 지식 DB 인제스트 현황
```
📊 [Argus Pulse ChromaDB 현황]
   위치: /Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/db/chromadb
   1. argus_knowledge (외부 지식: PDF/웹자료) : 648개 청크
   2. argus_reports   (내부 지식: 생성 리포트)   : 17개 청크
   👉 전체 보유 지식 청크: 665개
```

### 2) Thesis 점검 실증 (`T-02 메모리 산업의 변화`)
- **신뢰도 변동**: 75% → 80% (+5%) 자동 갱신
- **지지 근거 기록**: 커스텀 HBM4 베이스 다이 선단 공정 전환 및 북미 수요 증가
- **반박 근거 기록**: 중국 CXMT 5세대 HBM3E 진입 위험
- [T-02 마크다운 파일](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/thesis/T-02-메모리-산업의-변화.md)에 날짜별 자동 기록 완료

### 3) 일일 다이제스트 실증 (`daily_digest.py --rag`)
- 5개 증권사 리포트 청크가 프롬프트에 주입되어, 단순 뉴스를 넘어 증권사 분석 데이터가 인용된 [2026-09-03-digest.md](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/output/digest/2026-09-03-digest.md) 생성 및 옵시디언 동기화 완료

### 4) 단위 테스트
- `pytest -m "not llm"`: **72개 테스트 전원 통과 (100% PASSED in 4.37s)**
