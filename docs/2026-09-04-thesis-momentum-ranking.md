# Argus Pulse — Thesis 시장 모멘텀 랭킹 및 Frontmatter 자동 갱신 명세서

> **문서 번호**: SPEC-20260904-02  
> **작성 일자**: 2026-09-04  
> **관련 모듈**: `thesis_loader.py`, `daily_digest.py`, `thesis_checker.py`, `argus.py`, `crontab.txt`  
> **상태**: 🟢 구현 및 전수 단위 테스트 완료 (79/79 Tests Passed)

---

## 1. 개요 (Overview)

투자 가설(Thesis)이 38개(Active 30개+)로 확장됨에 따라, 시장의 실시간 관심도와 뉴스 발생량을 반영하는 **시장 모멘텀 랭킹(News Momentum Rank)** 시스템을 구축하였습니다.

이 시스템은 매일 밤 다이제스트 발행 시와 가설 자동 점검 시, **모든 Thesis 마크다운(`T-*.md`) 파일의 YAML Frontmatter에 최신 순위(`rank`)와 모멘텀 점수(`momentum`)를 자동으로 갱신**하고 옵시디언 볼트로 실시간 동기화합니다.

```
                  [시장 뉴스 DB (news.sqlite)]
                               │
                               ▼
            [get_thesis_momentum_ranking() 랭킹 엔진]
            - 최근 24~48h 뉴스 매칭 & 점수 가중 합산
            - Priority & Confidence 복합 스코어링
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
 [T-*.md Frontmatter 갱신]             [파이프라인 최적화 연동]
 • rank: 1                             • daily_digest (Top 5 랭킹 브리프)
 • momentum: 8204.6                    • thesis_checker --smart (15초 초고속 점검)
 • news_count: 100                     • argus.py / run.sh --rank (CLI 뷰어)
 • last_ranked: 2026-09-04T22:28       • obsidian_sync (Theses 동기화)
```

---

## 2. 시장 모멘텀 랭킹 산출 알고리즘

각 Thesis $T$의 등록 키워드와 최근 $N$일간(기본 2일) 수집된 뉴스를 대조하여 점수를 산출합니다.

### 1) 산출 공식 (Formula)

$$\text{Momentum Score} = \sum_{n \in News(T)} (n.score \times \text{Weight}_{recency}) + (\text{Priority} \times 10) + (\text{Confidence} \times 0.2)$$

* **최신성 가중치 ($\text{Weight}_{recency}$)**: 최근 24시간 이내 발생한 뉴스에 **1.2배** 가중치 부여
* **우선도 가중치 ($\text{Priority}$)**: 사용자 지정 중요도 (1~5) $\times 10$점
* **신뢰도 가중치 ($\text{Confidence}$)**: 가설 신뢰도 (0~100) $\times 0.2$점
* **정렬 기준**: `raw_momentum_score` (뉴스 점수 합) $\rightarrow$ `momentum_score` $\rightarrow$ `priority` $\rightarrow$ `confidence` 순으로 내림차순 정렬 후 $1$위부터 순위(`rank`) 부여

---

## 3. 실시간 시장 모멘텀 랭킹 현황 (Top 10)

```
🔥 [Argus Pulse] 최근 2일간 시장 모멘텀(News Momentum) Thesis 랭킹 Top 10
══════════════════════════════════════════════════════════════════════════════════
 순위  |   ID   | 가설 제목                    |  뉴스   |   모멘텀 점수   |  신뢰도   |  우선도 
──────────────────────────────────────────────────────────────────────────────────
  1  |  T-01  | 데이터센터의 변화                |  100  |   8204.6   |  57  % | P5
  2  |  T-02  | 메모리 산업의 변화               |  85   |   7225.0   |  75  % | P5
  3  |  T-03  | 전고체 배터리의 변화              |  51   |   3800.2   |  60  % | P3
  4  |  T-32  | ESS와 한국 배터리의 미국 수혜       |  26   |   1872.0   |  73  % | P5
  5  |  T-22  | AI 전력망용 대용량 ESS와 LFP 공   |  16   |   1197.4   |  73  % | P4
  6  |  T-05  | 금리와 데이터센터                |  11   |   885.8    |  79  % | P4
  7  |  T-33  | 반도체 소부장의 내재화             |   4   |   334.6    |  60  % | P3
  8  |  T-31  | AI 소프트웨어 레이어의 과점화        |   4   |   260.0    |  55  % | P3
  9  |  T-30  | 피지컬 AI와 로봇의 상용화          |   3   |   236.2    |  56  % | P4
 10  |  T-23  | 변압기·초고압 그리드 쇼티지 장기화      |   2   |   175.0    |  85  % | P4
══════════════════════════════════════════════════════════════════════════════════
```

---

## 4. Thesis Frontmatter 스키마 및 자동 갱신 예시

### 1) 갱신되는 프론트매터 필드
| 필드명 | 타입 | 설명 |
|---|---|---|
| `rank` | `int` | 실시간 시장 모멘텀 순위 (1~N) |
| `momentum` | `float` | 모멘텀 종합 가중 점수 |
| `news_count` | `int` | 최근 분석 기간 내 매칭된 뉴스 건수 |
| `last_ranked` | `string` | 랭킹 갱신 시각 (ISO 포맷 `YYYY-MM-DDTHH:MM`) |

### 2) 실제 `T-01` 파일 갱신 결과
```yaml
---
id: T-01
title: 데이터센터의 변화
status: active
confidence: 57
priority: 5
rank: 1
momentum: 8204.6
news_count: 100
last_ranked: 2026-09-04T22:28
keywords:
- 데이터센터
- 전력
- 액체냉각
- HBM
- SMR
...
---
```

---

## 5. 파이프라인 자동화 및 실행 트리거

1. **일일 다이제스트 (`daily_digest.py` - 매일 21:00)**:
   * 다이제스트 본문 상단에 `[🔥 오늘의 시장 모멘텀 Thesis 랭킹 Top 5]` 브리프 자동 삽입
   * 다이제스트 완료 후 `sync_thesis_ranks_to_files()` 자동 호출로 MD 파일 갱신
2. **스마트 가설 점검기 (`thesis_checker.py --smart` - 매일 21:05)**:
   * 29개 순차 점검 대신 **모멘텀 상위(뉴스 발생) 테제만 선별하여 15초 내에 초고속 점검**
   * 점검 완료 후 신뢰도 변경분과 함께 랭킹 필드 동시 갱신
3. **통합 제어 센터 (`argus.py` / `run.sh`)**:
   * 메뉴 `[11] 🔥 시장 모멘텀 Thesis 랭킹 조회` 제공
   * 터미널 단축 명령어: `./run.sh --rank`

---

## 6. 사용 명령어 가이드

```bash
# 1. 시장 모멘텀 랭킹 콘솔 확인
./run.sh --rank
# 또는
python thesis_loader.py --rank --limit 10

# 2. 랭킹 계산 후 모든 Thesis MD 파일 프론트매터 강제 갱신
python thesis_loader.py --sync

# 3. 모멘텀 상위 가설 스마트 선별 점검 (15초 완료)
python thesis_checker.py --smart --top 5

# 4. 전체 단위 테스트 실행
pytest tests/test_thesis_ranking.py -v
```

---

## 7. 테스트 검증 결과

* **신규 테스트 모듈**: [`tests/test_thesis_ranking.py`](file:///Users/boon/Dropbox/03_code/b_0901_Argus_pulse/tests/test_thesis_ranking.py) (7개 테스트)
  * `test_ranking_returns_list`: 반환 타입 검증
  * `test_ranking_required_fields`: 필수 필드 존재 확인
  * `test_ranking_sequence`: 1위부터 순차적 랭크 부여 확인
  * `test_ranking_order_consistency`: 점수 내림차순 정렬 일치성 확인
  * `test_ranking_limit`: limit 옵션 검증
  * `test_fallback_when_db_missing`: DB 부재 시 안전한 Fallback 검증
  * `test_sync_thesis_ranks_to_files`: Frontmatter 파일 기록 및 읽기 검증
* **전체 테스트 결과**: **79개 테스트 전원 통과 (100% PASSED)**
