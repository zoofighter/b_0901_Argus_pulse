# Argus Pulse — 2026-09-02 작업 요약

> **날짜**: 2026-09-02  
> **프로젝트**: Argus Pulse (LangGraph 멀티에이전트 시장 인텔리전스 엔진)  
> **상태**: 설계 및 콘텐츠 프로토타이핑 완료 / 구현 대기

---

## 1. 오늘 하루 작업 흐름

```
08:04  요건정의서 생성 (requirements_spec.md)
08:10  프로젝트 현황 쉬운 요약 (2026-09-02-summary.md)
08:19  LLM 위키 vs RAG 분석 (2026-09-02-wiki-vs-rag.md)
08:44  2-Page 블로그 생성 전략 논의
08:46  Thesis 4개 블로그 샘플 작성 (blog_samples_thesis_4.md)
10:04  블로그 주제 자동 생성기 설계 (blog_topic_generator_design.md)
10:06  블로그 제목(3종)+목차 기획안 (2026-09-02-blog-topic-outlines.md)
10:07  개별 블로그: 삼성 zHBM (blog_samsung_zhbm.md)
10:20  개별 블로그: 엔비디아 NVHBM (blog_nvidia_nvhbm.md)
13:03  Thesis 5개 추가 → 9개 전체 블로그 샘플 (blog_samples_thesis_9.md)
13:12  오늘 작업 요약 (본 문서)
```

---

## 2. 생성된 문서 목록 (13개)

### 📋 기획/설계 문서 (4개)

| 문서 | 용도 | 크기 |
|---|---|---|
| [human.md](file:///Users/boon/Dropbox/03_code/b_0901_Argus_pulse/docs/human.md) | 원본 요구사항 (사용자 메모) | 1.5KB |
| [asking.md](file:///Users/boon/Dropbox/03_code/b_0901_Argus_pulse/docs/asking.md) | 미결 질문 목록 | 0.3KB |
| [requirements_spec.md](file:///Users/boon/Dropbox/03_code/b_0901_Argus_pulse/docs/requirements_spec.md) | 요건정의서 (15개 요건, FR 8개, NFR 5개) | 11.8KB |
| [implementation_plan.md](file:///Users/boon/Dropbox/03_code/b_0901_Argus_pulse/docs/implementation_plan.md) | LangGraph 멀티에이전트 구현 계획서 | 13.5KB |

### 📊 분석/연구 문서 (2개)

| 문서 | 용도 | 크기 |
|---|---|---|
| [2026-09-02-summary.md](file:///Users/boon/Dropbox/03_code/b_0901_Argus_pulse/docs/2026-09-02-summary.md) | 프로젝트 현황 쉬운 요약 | 4.3KB |
| [2026-09-02-wiki-vs-rag.md](file:///Users/boon/Dropbox/03_code/b_0901_Argus_pulse/docs/2026-09-02-wiki-vs-rag.md) | LLM 위키 vs RAG 비교 분석 (비용, 확장성, 하이브리드 권장) | 13.8KB |

### ✍️ 블로그 콘텐츠 (5개)

| 문서 | 용도 | 크기 |
|---|---|---|
| [blog_topic_generator_design.md](file:///Users/boon/Dropbox/03_code/b_0901_Argus_pulse/docs/blog_topic_generator_design.md) | 블로그 주제 자동 생성기 설계서 | 5.4KB |
| [2026-09-02-blog-topic-outlines.md](file:///Users/boon/Dropbox/03_code/b_0901_Argus_pulse/docs/2026-09-02-blog-topic-outlines.md) | 4대 테제 × 제목 3종 × 2-Page 세부 목차 기획안 | 10.8KB |
| [blog_samples_thesis_9.md](file:///Users/boon/Dropbox/03_code/b_0901_Argus_pulse/docs/blog_samples_thesis_9.md) | **9대 Thesis 2-Page 블로그 시리즈 완결판** | 20.7KB |
| [blog_samsung_zhbm.md](file:///Users/boon/Dropbox/03_code/b_0901_Argus_pulse/docs/blog_samsung_zhbm.md) | 개별 블로그: 삼성전자 zHBM 3D 적층 | 5.7KB |
| [blog_nvidia_nvhbm.md](file:///Users/boon/Dropbox/03_code/b_0901_Argus_pulse/docs/blog_nvidia_nvhbm.md) | 개별 블로그: 엔비디아 NVHBM 아키텍처 | 6.1KB |

---

## 3. 핵심 의사결정 사항

### ✅ 확정된 것

| 항목 | 결정 |
|---|---|
| 지식 저장 방식 | **하이브리드** (안정 지식 = 옵시디언 위키, 동적 데이터 = RAG/ChromaDB) |
| 첫 번째 산출물 | 심층 보고서 전에 **2-Page 블로그부터 시작** (단순 스크립트로 바로 구현 가능) |
| Thesis 주제 | 기존 4개 → **9개로 확대** |
| 구현 계획서 | `implementation_plan.md` 확정 (7단계 Phase) |
| 요건정의서 | `requirements_spec.md` 확정 (FR 8개, NFR 5개) |

### 🔄 오늘 추가된 Thesis 5개 (human.md 22줄)

| # | 새 테제 | 핵심 관점 |
|---|---|---|
| ⑤ | 금리와 데이터센터 | CAPEX 7,200억$, ROIC 검증 vs 전력 인프라 병목 |
| ⑥ | TPU 증가와 GPU 수요 둔화 | 추론 시대 진입, TPU v6 가성비 4배, CUDA 벽 |
| ⑦ | CXL 메모리의 확대 | 제3 메모리 계층, 메모리 풀링, Azure 프로덕션 도입 |
| ⑧ | 엔비디아와 네오클라우드 | CoreWeave 혈맹, GPU 수요 방어 전략 |
| ⑨ | 엔비디아와 GPU 금융 | 칩담대 5,000억$, AI 서브프라임 리스크 |

---

## 4. 오늘 다룬 주요 질의응답 (Q&A)

| 질문 | 답변 핵심 |
|---|---|
| LLM 위키 vs RAG 어느 것이 좋은가? | 둘 다 쓰는 **하이브리드**가 최적 (RAG 단독 대비 50% 비용 절감) |
| 위키도 초기에 LLM이 문서를 읽지 않는가? | **읽는다**. 차이는 읽는 시점과 횟수 (위키: 1회 정리 / RAG: 매번 원문) |
| 위키가 쌓이면 비용이 올라가지 않는가? | **맞다**. 문서 500개+ 시 결국 위키 안에서도 RAG 검색 필요 → 합쳐지는 구조 |
| 2-Page 블로그에 초점을 맞추면? | 전체 시스템 없이 **단순 스크립트**로 즉시 구현 가능 |
| 블로그 주제 생성기도 가능한가? | **가능**. 뉴스 + Thesis + 배경지식 교차 → 4가지 앵글로 주제 자동 발굴 |

---

## 5. 다음 단계 (미결 사항)

| 우선순위 | 항목 | 상태 |
|---|---|---|
| 🔴 높음 | 산업 PDF 파일 위치 확인 (20~30장) | ❓ 미확인 |
| 🔴 높음 | 웹 자료 형태 확인 (URL 목록 vs 저장 파일) | ❓ 미확인 |
| 🔴 높음 | Gemini API 키 발급/설정 | ❓ 필요 |
| 🟡 보통 | 블로그 생성 스크립트 구현 (Phase 1) | ⏳ 대기 |
| 🟡 보통 | 9개 Thesis → `thesis.yaml` 구조화 | ⏳ 대기 |
| 🟢 낮음 | 전체 시스템 7단계 Phase 구현 | ⏳ 대기 |

---

## 6. 폴더 구조 현황

```
b_0901_Argus_pulse/
├── db/                    (빈 폴더 — ChromaDB 저장 예정)
├── docs/                  (문서 13개)
│   ├── human.md                        ← 원본 요구사항
│   ├── asking.md                       ← 미결 질문
│   ├── requirements_spec.md            ← 요건정의서
│   ├── implementation_plan.md          ← 구현 계획서
│   ├── 2026-09-02-summary.md           ← 프로젝트 쉬운 요약
│   ├── 2026-09-02-wiki-vs-rag.md       ← 위키 vs RAG 분석
│   ├── 2026-09-02-blog-topic-outlines.md ← 제목+목차 기획안
│   ├── blog_topic_generator_design.md  ← 주제 생성기 설계서
│   ├── blog_samples_thesis_4.md        ← 블로그 시리즈 (초기 4개)
│   ├── blog_samples_thesis_9.md        ← 블로그 시리즈 (전체 9개) ★
│   ├── blog_samsung_zhbm.md            ← 개별: 삼성 zHBM
│   ├── blog_nvidia_nvhbm.md            ← 개별: 엔비디아 NVHBM
│   └── 2026-09-02-work-summary.md      ← 본 문서 (오늘 작업 요약)
└── reports/               (빈 폴더 — 생성된 보고서 저장 예정)
```
