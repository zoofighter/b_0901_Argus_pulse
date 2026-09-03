# Argus Pulse — 2026-09-03 작업 요약 및 운영 가이드

> **날짜**: 2026-09-03  
> **프로젝트**: Argus Pulse (시장 인텔리전스 & 콘텐츠 생성 엔진)  
> **상태**: 파이프라인 전 모듈 완성, 듀얼 LLM 대체 구축, 옵시디언 실시간 볼트 연동, 자동화 스케줄러 구축 완료

---

## 1. 오늘 구현 완료된 핵심 기능

```
[Argus Pulse 통합 아키텍처]

       [수동 자료 (99.raw/)]              [실시간 뉴스 DB (news.sqlite)]
                │                                      │
                ▼                                      ▼
     [html_parser / 아카이빙]             [hourly_monitor (매시간 감시)]
                │                                      │
                ├──────────► [topic_generator] ◄───────┤
                │             (듀얼 LLM 분석)          │
                │                    │                 │
                ▼                    ▼                 ▼
          [아카이브 보관]      [Human-in-the-Loop]    [80점+ 즉시 알림]
                                ├─ 1b: 블로그 작성 (blog_writer)
                                ├─ 2t: 스레드 작성 (thread_writer)
                                └─ s: 검증 리뷰 (review_generator)
                                     │
                                     ▼
                     [obsidian_sync 실시간 자동 연동]
                     (agent_vault: Blog / Thread / Digest / Review)
```

| 모듈 | 파일 | 주요 역할 |
|---|---|---|
| **통합 런처** | [`argus.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/argus.py) / [`run.sh`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/run.sh) | 대화형 콘솔 메뉴 및 단축 명령어 실행기 |
| **자동화 스케줄러** | [`scheduler.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/scheduler.py) | 08:00 추천, 09~21시 정각 모니터링, 21:00 다이제스트 백그라운드 구동 |
| **옵시디언 동기화** | [`obsidian_sync.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/obsidian_sync.py) | 생성 즉시 실제 iCloud Obsidian 볼트로 복사/동기화 |
| **수동 자료 아카이빙** | [`html_parser.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/html_parser.py) | `99.raw/` 처리 후 중복 방지를 위한 `archive/` 자동 격리 |
| **듀얼 LLM 엔진** | [`llm_client.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/llm_client.py) | Gemini 3.7 Flash ↔ OpenCode Muse-Spark 1.2 무중단 자동 Fallback |
| **스레드 생성기** | [`thread_writer.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/thread_writer.py) | X/트위터 5~7트윗 타래 자동 생성 (수혜/구조/공장 3대 각도) |
| **일일 다이제스트** | [`daily_digest.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/daily_digest.py) | 하루 뉴스 집계 및 테제별 인사이트 브리프 |
| **예측 검증 리뷰** | [`review_generator.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/review_generator.py) | 뉴스 부족 시 과거 블로그 예측 검증 콘텐츠 생성 |
| **품질 검수 위원 (Critic)** | [`critic.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/critic.py) | 5대 기준 100점 만점 자가 채점 및 80점 미달 시 1회 자동 보완 루프 |

---

## 2. 간편 사용법

### 🚀 간편 통합 런처 실행
```bash
./run.sh
# 또는
python argus.py
```
실행 시 대화형 메뉴가 표시되며 원하는 작업 번호를 입력하여 즉시 실행할 수 있습니다.

### 📋 개별 CLI 명령어
```bash
# 1. 아침 주제 추천 (뉴스 기반)
./run.sh --topic

# 2. 99.raw 폴더 수동 자료 분석 및 아카이빙
./run.sh --raw

# 3. 실시간 뉴스 감시 1회 즉시 실행
./run.sh --monitor

# 4. 데일리 다이제스트 생성 (오늘 종합)
./run.sh --digest

# 5. 과거 블로그 검증 리뷰 생성
./run.sh --review

# 6. 옵시디언 전체 수동 동기화
./run.sh --sync

# 7. 백그라운드 스케줄러 실행
./run.sh --schedule
```

---

## 3. 맥(Mac) Crontab 자동화 등록 방법

터미널에서 `crontab -e` 실행 후 붙여넣기:
```cron
# 08:00 아침 주제 추천 (알림 발송)
0 8 * * * cd /Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse && /opt/anaconda3/bin/python topic_generator.py --auto >> logs/cron_topic.log 2>&1

# 09:00~21:00 매시간 뉴스 모니터링 (80점 이상 즉시 알림)
0 9-21 * * * cd /Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse && /opt/anaconda3/bin/python hourly_monitor.py --once >> logs/cron_monitor.log 2>&1

# 21:00 데일리 다이제스트 생성 및 옵시디언 동기화
0 21 * * * cd /Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse && /opt/anaconda3/bin/python daily_digest.py >> logs/cron_digest.log 2>&1
```
(위 설정 내용은 [`crontab.txt`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/crontab.txt) 파일에도 저장되어 있습니다.)

---

## 4. 트랙 2: 심층 엔진(RAG + Thesis Auto-Update) 고도화 완료

| 신규/수정 모듈 | 파일 | 주요 역할 |
|---|---|---|
| **증권사 PDF 파서** | [`pdf_parser.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/pdf_parser.py) | 증권사 리포트 파일명 메타데이터(일자, 기업, 증권사, 제목) 및 본문 텍스트 자동 추출 |
| **RAG 벡터 검색 엔진** | [`rag_engine.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/rag_engine.py) | ChromaDB 기반 2개 컬렉션(`argus_knowledge`, `argus_reports`) 관리 및 하이브리드 검색 |
| **지식 인제스트 도구** | [`ingest.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/ingest.py) | 42개 증권사 PDF, 수동 스크랩, 자체 생성 산출물 일괄 인제스트 (총 665개 청크 보유) |
| **Thesis 자동 점검기** | [`thesis_checker.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/thesis_checker.py) | 뉴스+리포트 근거 기반 Thesis 신뢰도(-15~+15) 및 지지/반박 근거 자동 기록 |

### 🚀 RAG 사용/미사용 선택 기능 (`--rag` 토글)
- **일반 모드 (기본)**: 속보성 뉴스만 참조하여 빠른 생성 (약 5~10초)
- **RAG 심층 모드 (`--rag`)**: 증권사 리포트 및 과거 산출물 수치까지 검색 인용

```bash
# RAG 심층 모드로 블로그 작성
python blog_writer.py --topic '...' --rag

# RAG 심층 모드로 스레드 작성
python thread_writer.py --topic '...' --angle A --rag

# RAG 심층 모드로 다이제스트 생성
python daily_digest.py --rag

# Thesis 신뢰도 및 근거 자동 점검
python thesis_checker.py

# 주제 추천기 HitL 메뉴에서 선택
# 1b : 일반 블로그
# 1br: RAG 심층 블로그
# 2t : 일반 스레드
# 2tr: RAG 심층 스레드
```

---

## 5. 최종 검증 결과

- **RAG 지식 DB**: 42개 증권사 리포트 + Raw 파일 + 산출물 = **총 665개 청크 인제스트 완료**
- **단위 테스트**: `pytest -m "not llm"` → **72개 테스트 전원 통과 (100% PASSED in 4.37s)**
- **Thesis 점검 실증**: `T-02`(메모리 산업의 변화) 신뢰도 75% → 80% 자동 갱신 및 지지/반박 근거 MD 파일 기록 확인
- **다이제스트 실증**: `daily_digest.py --rag` 실행 결과 리서치 지식 인용 블록 자동 결합 확인
- **콘텐츠 톤 & 서식 고도화**:
  - 블로그: 시니어 애널리스트 톤, 마크다운 비교 표(Table) 필수 탑재, 기초 금융 약어 괄호 풀이 생략, 볼드 첫머리 강조 반영
  - 스레드: `--length compact`(10~15줄 완독형) 및 `--length deep`(25~35줄 심층형) 분량 선택 옵션 추가
- **Critic 자가 검수 에이전트 ([`critic.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/critic.py))**: 5대 평가 기준 100점 만점 평가 및 80점 미달 시 자동 1회 수정(Refine) 루프 구축 (`python blog_writer.py --critic`)
- **옵시디언 `argus/` 전용 폴더 체계 구축**: 모든 산출물(`Blog`, `Thread`, `Digest`, `Review`, `Theses`)을 `agent_vault/argus/` 단일 하위 디렉터리로 완전 통합 격리 완료

