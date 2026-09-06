# Argus Pulse — 2026-09-06 작업 요약 및 시스템 고도화 보고서

> **작성일자**: 2026-09-06  
> **프로젝트**: Argus Pulse (시장 인텔리전스 & 콘텐츠 생성 엔진)  
> **시스템 상태**: 크론/배치 안정화, 13:00 미드데이 파이프라인 신설, 실제 뉴스 URL 마크다운 링크 연동, 시장 모멘텀(News Momentum) 랭킹 엔진 구축 완료

---

## 1. 핵심 성과 및 고도화 요약

```
[Argus Pulse 일일 자동화 파이프라인 (24시간 풀 스케줄)]

08:00 ──► [아침 주제 추천 & 1위 블로그 자동 집필 (topic_generator)] ──► 기획안 3선 도출 + 1위 포스트 자동 생성 + 옵시디언 동기화 & 디스코드 알림
               │
09~21:00 ─► [매시간 뉴스 감시 (hourly_monitor)] ──► 80점+ 충격 뉴스 즉각 감지 & 디스코드 발송
               │
13:00 ──► [오후 사후 검증 리뷰 (review_generator)] ► 과거 블로그 예측 vs 오전 팩트 RAG 검증
13:05 ──► [오후 신규 주제 추천 (topic_generator)] ─► 오전장~점심 핫 뉴스 반영 오후 기획안 도출
               │
21:00 ──► [데일리 다이제스트 (daily_digest)] ────► 일일 모멘텀 랭킹 & Top 6 테제 종합 브리프
21:05 ──► [Thesis 가설 스마트 점검 (thesis_checker)]► 34개 투자 가설 신뢰도/근거/랭킹 자동 갱신
               │
           [전 모듈 실시간 옵시디언(Obsidian Vault) 미러링 동기화]
```

---

## 2. 세부 구현 및 개선 내역

### ① 아침 배치 결함 디버깅 및 비대화형 안정성 확보
* **`topic_generator.py` EOFError 해결**: 크론탭이나 백그라운드 스케줄러 환경(`not sys.stdin.isatty()`)에서 사용자 입력을 요구하다 발생하던 `EOFError`를 안전하게 건너뛰고, 주제 저장 및 알림 후 정상 종료(Exit code 0)하도록 개선.
* **`hourly_monitor.py` 쿼리 누락 개선**: 대량 뉴스 인입 시 고정 `LIMIT 100`으로 인해 80점짜리 핫 뉴스가 밀려나던 문제를 `ORDER BY score DESC, id DESC LIMIT 500` 및 최근 4시간(`collected_at >= ?`) 조건으로 개편하여 알림 누락을 원천 차단.

### ② 실제 뉴스 원문 URL 마크다운 하이퍼링크 자동 주입
* **실시간 링크 추출기 구현 (`fetch_related_news`, `format_news_references`)**: 뉴스 DB에서 해당 테제 및 기획안과 일치하는 실제 기사 제목, 언론사, 게시일, 원문 URL을 조회하여 LLM 프롬프트에 주입.
* **출처 섹션 강화**: 블로그(`blog_writer.py`), 기획 윤곽서(`outline`), 사후 검증 리뷰(`review_generator.py`) 최하단 `## 📚 참고 자료 및 출처 (References)` 섹션에 실제 클릭 가능한 마크다운 링크(`[기사제목](URL)`)가 자동으로 표기되도록 강제화.

### ③ 오후 1시(13:00) 미드데이 배치 파이프라인 신설
* **요구사항 반영**: 오전 장 마감 및 점심 시간대(13:00)의 시장 변동을 포착하여 정리하는 2단계 배치 구축.
  - **13:00**: `review_generator.py --rag` (과거 블로그 예측과 오전 시장 팩트 사후 검증)
  - **13:05**: `topic_generator.py --auto` (오전~점심 핫 뉴스 기반 오후 블로그/스레드 주제 3선 추천)
* **스케줄 등록**: Mac 시스템 `crontab`, [`crontab.txt`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/crontab.txt), [`scheduler.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/scheduler.py), [`argus.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/argus.py)에 정식 반영.

### ④ 시장 모멘텀(News Momentum) Thesis 랭킹 시스템 구축
* **실시간 모멘텀 산출 알고리즘 (`thesis_loader.py`)**:
  - 최근 N일간 뉴스 수집량(`news_count`), 최근 24시간 가중치(1.2배), 뉴스 평균 점수, 가설 우선순위(Priority) 및 신뢰도(Confidence)를 결합한 종합 모멘텀 점수 계산.
* **프론트매터 자동 갱신 (`sync_thesis_ranks_to_files`)**:
  - 34개 모든 `thesis/T-*.md` 파일 프론트매터에 `rank`, `momentum`, `news_count`, `last_ranked`를 자동 기록하고 옵시디언 동기화.
* **다이제스트 연동 (`daily_digest.py`)**: 일일 다이제스트 상단에 당일 시장 모멘텀 랭킹 Top 5를 자동 표기.
* **통합 제어 센터 연동 (`argus.py`)**: 대화형 메뉴 [11]번 및 CLI 플래그 `--rank` 추가.

### ⑤ 아침 크론 배치 진단 및 블로그 자동 집필(Auto-Write) 파이프라인 구축
* **배치 실행 진단**: 08:00 크론(`topic_generator.py --auto`)은 정상 작동하여 3대 기획안(`logs/2026-09-06-topics.json`) 저장 및 디스코드 알림을 발송했으나, 기존 Human-in-the-Loop 구조상 사용자 선택 전까지는 2-Page 블로그 마크다운 파일이 생성되지 않아 배치가 미작동한 것처럼 보였던 원인을 분석·규명.
* **1위 추천 주제 블로그 자동 집필 기능 신설**:
  - `topic_generator.py`에 `--auto-write` 및 `--rag` 플래그 추가.
  - 비대화형(크론/스케줄러) 모드 실행 시 당일 1순위(`Rank 1`) 추천 주제로 `blog_writer.py --auto --rag`를 자동 연계 호출하여 2-Page 완성형 블로그 포스트를 즉시 집필하고 옵시디언(`agent_vault/argus/Blog/`)에 자동 미러링하도록 파이프라인 확장.
* **스케줄 및 환경설정 반영**:
  - [`config.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/config.py): `AUTO_WRITE_BLOG` 설정 지원.
  - macOS 시스템 `crontab`, [`crontab.txt`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/crontab.txt), [`scheduler.py`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/scheduler.py): 08:00 아침 크론에 `--auto-write --rag` 옵션 정식 적용 완료.

---

## 3. 주요 생성 콘텐츠 산출물

| 카테고리 | 문서명 | 핵심 내용 |
|---|---|---|
| **오늘자 정식 블로그 (9/6)** | [`2026-09-06-blog-삼성전자의-33-맹추격-하지만-진짜-전쟁은-HBM4-커스텀-수주전이다.md`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/output/blog/2026-09-06-blog-%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90%EC%9D%98-33-%EB%A7%B9%EC%B6%94%EA%B2%A9-%ED%95%98%EC%A7%80%EB%A7%8C-%EC%A7%84%EC%A7%9C-%EC%A0%84%EC%9F%81%EC%9D%80-HBM4-%EC%BB%A4%EC%8A%A4%ED%85%80-%EC%88%98%EC%A3%BC%EC%A0%84%EC%9D%B4%EB%8B%A4.md) | 당일 1위 기획안 기반 2-Page 블로그. HBM3E 점유율 격차 축소 vs HBM4 커스텀 ASIC화 대조표, 3사 전략 비교, 증권사 리포트 RAG 연동, 실제 뉴스 원문 5건 URL 링크 포함 |
| **정식 블로그 (9/4)** | [`2026-09-04-blog-삼성의-33-맹추격-착시일-뿐-진짜-HBM-왕좌는-HBM4-커스텀에서-갈.md`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/output/blog/2026-09-04-blog-%EC%82%BC%EC%84%B1%EC%9D%98-33-%EB%A7%B9%EC%B6%94%EA%B2%A9-%EC%B0%A9%EC%8B%9C%EC%9D%BC-%EB%BF%90-%EC%A7%84%EC%A7%9C-HBM-%EC%99%95%EC%A2%8C%EB%8A%94-HBM4-%EC%BB%A4%EC%8A%A4%ED%85%80%EC%97%90%EC%84%9C-%EA%B0%88.md) | 최고 점수(80점) 뉴스 기반, HBM3E vs HBM4 비교 표, 3사 전략 대조, 실제 기사 URL 출처 포함 |
| **기획 윤곽서 (1-Page)** | [`2026-09-04-outline-삼성의-33-맹추격-착시일-뿐-진짜-HBM-왕좌는-HBM4-커스텀에서-갈.md`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/output/outline/2026-09-04-outline-%EC%82%BC%EC%84%B1%EC%9D%98-33-%EB%A7%B9%EC%B6%94%EA%B2%A9-%EC%B0%A9%EC%8B%9C%EC%9D%BC-%EB%BF%90-%EC%A7%84%EC%A7%9C-HBM-%EC%99%95%EC%A2%8C%EB%8A%94-HBM4-%EC%BB%A4%EC%8A%A4%ED%85%80%EC%97%90%EC%84%9C-%EA%B0%88.md) | 제목 3종(A/B/C), 4단계 논점 구조, 집필 체크포인트, 뉴스 원문 링크 배치 |
| **사후 검증 리뷰** | [`2026-09-04-review-금리-동결에-환호한-AI-랠리의-불편한-진실-돈은-풀렸.md`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/output/review/2026-09-04-review-%EA%B8%88%EB%8 contamination) | T-05/T-01 가설 사후 검증, 증권사 리포트 RAG 대조 분석 |
| **데일리 다이제스트** | [`output/digest/2026-09-04-digest.md`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/output/digest/2026-09-04-digest.md) | 453건 뉴스 및 Top 6 테제 종합 브리프, RAG 심층 참조 반영 |

---

## 4. 운영 및 실행 가이드

```bash
# 1. 아침/오후 추천 주제 확인
python topic_generator.py --auto

# 2. 실시간 뉴스 감시 1회 실행
python hourly_monitor.py --once

# 3. 시장 모멘텀 Thesis 랭킹 조회
python thesis_loader.py --rank

# 4. Thesis 프론트매터 랭킹 일괄 갱신 및 옵시디언 동기화
python thesis_loader.py --sync

# 5. 과거 블로그 사후 검증 리뷰 (RAG 심층)
python review_generator.py --rag

# 6. 옵시디언 전체 동기화
python obsidian_sync.py --all

# 7. 백그라운드 24시간 스케줄러 실행
python scheduler.py
```
