# Argus Pulse — 멀티에이전트 상세 시퀀스 다이어그램

> **작성일자**: 2026-09-02  
> **프로젝트**: Argus Pulse (LangGraph Multi-Agent Market Intelligence Engine)  
> **문서 버전**: v1.0

---

## 1. 전체 실행 흐름 (End-to-End Sequence)

시스템 스케줄러(Cron/이벤트)에 의해 구동되어 자료 수집, 6개 에이전트의 협업 분석, 품질 검수, 배포 및 지식 재인제스트까지의 전체 흐름입니다.

```mermaid
sequenceDiagram
    autonumber
    actor Scheduler as ⏰ Scheduler / User
    participant Orch as 🎯 Orchestrator
    participant Res as 🔍 Researcher
    participant Chroma as 💾 ChromaDB
    participant SQLite as 🗄️ SQLite (News)
    participant Ana as 📊 Analyst
    participant Thesis as 🔬 Thesis Checker
    participant Writer as ✍️ Report Writer
    participant Critic as 🧐 Critic
    participant Out as 📤 Delivery (Obsidian/Discord)

    Note over Scheduler, Orch: [Phase 1: 태스크 시작 및 라우팅]
    Scheduler->>Orch: 분석 태스크 트리거 (주기별 리포트 / 속보 분석)
    Orch->>Orch: 태스크 범위 및 대상 테제(Thesis) 식별

    Note over Orch, SQLite: [Phase 2: 다중 소스 리서치]
    Orch->>Res: 리서치 지시 (키워드, 기간, 테제 ID)
    Res->>Chroma: 유사도 검색 (PDF/웹 벡터 컨텍스트)
    Chroma-->>Res: 관련 지식 청크 반환
    Res->>SQLite: 최근 뉴스/공시 SQL 쿼리
    SQLite-->>Res: 최신 뉴스 기사 리스트
    Res->>Res: 컨텍스트 정합성 필터링 및 병합
    Res-->>Ana: 수집된 원천 데이터 및 정제 컨텍스트 전달

    Note over Ana, Thesis: [Phase 3: 심층 분석 및 가설 검증]
    Ana->>Ana: 시장 동향 파악, 이상 신호(Anomaly) 및 팩트 추출
    Ana-->>Thesis: 시장 동향 분석 리포트 전달
    Thesis->>Thesis: thesis.yaml 로드 & 지지(+) / 반박(-) 근거 매핑
    Thesis->>Thesis: 테제 유효성 신뢰도 점수(Confidence Score) 계산
    Thesis-->>Writer: 분석 결과 + 테제 검증 팩트셋 전달

    Note over Writer, Critic: [Phase 4: 작성 및 품질 보증 (Evaluator-Optimizer)]
    loop 최대 2회 품질 피드백 루프 (Score < 80)
        Writer->>Writer: 구조화된 마크다운 리포트/블로그 초안 작성
        Writer->>Critic: 초안 보고서 검수 요청
        Critic->>Critic: 팩트 일치성, 논리성, 할루시네이션, 출처 명시 점검
        alt 품질 기준 미달 (Feedback Required)
            Critic-->>Writer: ❌ 반려 및 구체적 수정 지침 (Feedback)
        else 품질 통과 (Approved, Score >= 80)
            Critic-->>Orch: ✅ 최종 승인 통보
        end
    end

    Note over Orch, Chroma: [Phase 5: 배포 및 지식 순환 (Flywheel)]
    Orch->>Out: 최종 보고서 발행 (Obsidian 저장 & Discord 알림)
    Orch->>Chroma: 신규 작성된 리포트 임베딩 & 지식베이스 재인제스트
    Chroma-->>Orch: 지식 갱신 완료
    Orch-->>Scheduler: 전체 파이프라인 정상 종료
```

---

## 2. 세부 상호작용: Critic 검수 및 피드백 루프 (Quality Gate)

`Report Writer`와 `Critic` 사이의 반복적인 품질 교정 과정을 상세화한 시퀀스입니다.

```mermaid
sequenceDiagram
    autonumber
    participant W as ✍️ Report Writer
    participant C as 🧐 Critic
    participant S as 📊 State Store

    W->>S: Draft Report 저장
    W->>C: evaluate_draft(draft_content, fact_sheet)

    Note over C: 검수 항목 점검<br/>1. Fact Consistency (근거 일치도)<br/>2. Source Attribution (출처 명기)<br/>3. Thesis Argument Quality (논리성)

    alt Score < 80점 (품질 미달)
        C->>S: evaluation_result(status="NEEDS_REVISION", score=72, feedback="...")
        C-->>W: 피드백 전달 (예: "3번 문단의 수율 근거 출처 미비, 반박 논리 보강 필요")
        W->>W: 피드백 반영 후 재작성 (Revision)
        W->>C: evaluate_draft(revised_draft, fact_sheet)
        Note over C: 재평가 수행 (Re-evaluating)
    end

    C->>S: evaluation_result(status="PASSED", score=92)
    C-->>W: 최종 승인 완료
```

---

## 3. 세부 상호작용: Thesis(가설) 검증 및 지식 순환 (Knowledge Flywheel)

새로운 뉴스와 지식을 바탕으로 기존 가설을 업데이트하고, 완성된 리포트가 다시 RAG의 컨텍스트로 흡수되는 구조입니다.

```mermaid
sequenceDiagram
    autonumber
    participant TC as 🔬 Thesis Checker
    participant YAML as 📐 thesis.yaml
    participant CHROMA as 🔍 ChromaDB
    participant REPO as 📑 Report Storage

    TC->>YAML: 현재 활성 가설 9종 로드
    YAML-->>TC: 가설 정의, 핵심 지표, 기존 신뢰도(Confidence)
    TC->>TC: 신규 수집된 뉴스/데이터와 가설 비교
    
    rect rgb(240, 248, 255)
        Note over TC: 가설 지지/반박 신호 분기
        alt 새로운 지지 신호 발견
            TC->>TC: 지지 근거 누적 (+ Confidence 증가)
        else 새로운 반박/경쟁 신호 발견
            TC->>TC: 반박 근거 누적 (- Confidence 감소 또는 리스크 태그)
        end
    end

    TC->>YAML: 가설 상태 업데이트 (Status / Evidence Update)
    
    Note over REPO, CHROMA: 보고서 승인 완료 후 지식 축적
    REPO->>CHROMA: 생성된 완결 보고서 Chunking & Embedding
    CHROMA-->>CHROMA: 'internal_reports' 컬렉션에 벡터 저장
    Note over CHROMA: 다음 회차 분석 시 이전 보고서가<br/>Historical Context로 자동 활용됨
```

---

## 4. 컴포넌트별 상태(State) 전이 규격

| 단계 | 입력 State | 출력 State | 주요 처리 내용 |
|---|---|---|---|
| **Researcher** | `query`, `thesis_ids`, `timeframe` | `rag_chunks`, `news_records` | 벡터 유사도 검색 + SQLite 질의 |
| **Analyst** | `rag_chunks`, `news_records` | `insights`, `market_signals` | 데이터 요약 및 이상 패턴 추출 |
| **Thesis Checker** | `insights`, `thesis_yaml` | `thesis_eval_results`, `confidence` | 가설 지지/반박 근거 매핑 |
| **Report Writer** | `insights`, `thesis_eval_results`, `feedback` | `draft_report`, `revision_count` | 템플릿 기반 리포트 생성 및 수정 |
| **Critic** | `draft_report`, `insights` | `critic_score`, `feedback`, `is_approved` | 품질 점수 산출 및 승인 판정 |
