# Argus Pulse — 추가 제안 사항

> **작성일**: 2026-09-02  
> **목적**: 현재 설계에서 아직 다루지 않은 영역의 추가 기능 제안  
> **관련 문서**: [thesis_management_suggestions.md](file:///Users/boon/Dropbox/03_code/b_0901_Argus_pulse/docs/thesis_management_suggestions.md)

---

## 1. 📈 블로그 성과 추적 (Performance Tracker)

현재 시스템은 **글 생성까지만** 설계되어 있습니다. 발행 후 반응을 추적하면 더 좋은 글감 추천이 가능합니다.

### 구현 방법

```yaml
# blog/ 폴더 각 MD 파일 프론트매터에 추가
published_url: "https://tistory.com/..."
published_at: "2026-09-02"
views: 1240          # 수동 입력 또는 API
comments: 8
shares: 24
best_performing: true
```

### 기대 효과
- 어떤 Thesis, 어떤 앵글(기술진화/기업격돌 등)의 글이 독자 반응이 좋은지 패턴 발견
- 다음 블로그 주제 추천 시 **성과 좋은 유형 우선** 추천
- 예: "T-02 + 기업격돌형 글이 평균 조회수 2배" → 해당 조합 우선 추천

---

## 2. 🗓️ 블로그 발행 캘린더 자동 관리

현재 글을 **언제 발행할지** 계획이 없습니다.

### 구현 방법

데일리 다이제스트에 발행 일정 제안 섹션 추가:

```markdown
## 📅 이번 주 추천 발행 일정

| 요일 | 추천 Thesis | 이유 |
|---|---|---|
| 월요일 | T-01/T-02 | 주초 반도체·산업 뉴스 집중 |
| 수요일 | T-05/T-06 | 경제·시장 구조 주제 |
| 금요일 | T-03/T-04 | 배터리·온디바이스, 주말 읽기 좋은 주제 |
```

### 기대 효과
- 블로그 발행 리듬이 생겨 독자가 정기 방문하는 패턴 형성
- 뉴스 흐름이 많은 요일에 맞는 Thesis 글 발행 → 검색 노출 최적화

---

## 3. 🔗 시리즈 연결 관리 (Series Tracker)

같은 Thesis로 글을 여러 편 쓰다 보면 **자연스러운 시리즈**가 됩니다. 현재는 각 글이 독립적입니다.

### 구현 방법

```yaml
# 프론트매터에 추가
series: "2026 메모리 전쟁"    # 시리즈 이름
series_part: 3                # 이 글이 시리즈 3편
series_prev: "2026-08-15-blog-HBM3E-vs-HBM4.md"
series_next: null             # 아직 없음
```

### 기대 효과
- 독자가 관련 글을 연달아 읽게 유도 → 체류 시간 증가
- Thesis별 서사(스토리라인)가 쌓여 **권위 있는 시리즈** 형성
- 옵시디언 Dataview로 시리즈 목록 자동 관리 가능

```dataview
TABLE series_part, title, published_at
FROM "01_Inbox/Argus/blog"
WHERE series = "2026 메모리 전쟁"
SORT series_part ASC
```

---

## 4. 🌐 외부 소스 품질 필터 (Source Credibility)

현재 뉴스 스코어링은 **내용의 중요도**를 평가하지만, **출처 신뢰도**가 따로 없습니다.

### 구현 방법

```yaml
# sources.yaml에 추가
sources:
  - name: "SemiAnalysis"
    credibility: 5      # 1~5, 가장 신뢰
    type: "tech_blog"
    url: "https://semianalysis.com/feed"
  - name: "Reuters"
    credibility: 4
    type: "news_wire"
  - name: "TheStreet"
    credibility: 2      # 자극적 헤드라인 많음
    type: "financial_media"
```

### 스코어링 반영 방식

```
최종 점수 = 뉴스 내용 점수(0~100) × 출처 신뢰도 가중치(0.6~1.2)
```

| credibility | 가중치 | 효과 |
|---|---|---|
| 5 (최고 신뢰) | ×1.2 | 점수 20% 보너스 |
| 4 | ×1.1 | 점수 10% 보너스 |
| 3 (기본값) | ×1.0 | 변화 없음 |
| 2 | ×0.8 | 점수 20% 감점 |
| 1 (낮음) | ×0.6 | 점수 40% 감점 |

### 기대 효과
- 자극적 헤드라인의 저품질 뉴스가 상위에 올라오는 것 방지
- 블로그 글 근거로 사용하는 뉴스의 **출처 품질** 향상

---

## 5. 💬 독자 질문 수집 → 다음 글감 (FAQ Loop)

블로그 댓글이나 독자 반응에서 **"이 부분이 궁금해요"** 패턴을 다음 글감으로 활용합니다.

### 구현 방법

`reader_questions.md` 또는 `ideas.yaml` 파일로 관리:

```yaml
# ideas.yaml
reader_questions:
  - question: "HBM4랑 HBM3E 실제 성능 차이가 얼마나 되나요?"
    source: "tistory_comment"
    date: "2026-09-01"
    related_thesis: "T-02"
    used: false

  - question: "전고체 배터리 투자로 가장 좋은 종목은?"
    source: "discord_dm"
    date: "2026-09-02"
    related_thesis: "T-03"
    used: false
```

### 시스템 연동
- `topic_generator.py`에서 `ideas.yaml`의 미사용 질문을 추가 입력으로 포함
- 독자 질문 기반 블로그 주제 추천 → **실제 독자 니즈 반영**
- 사용한 질문은 `used: true`로 표시

---

## 6. ⏱️ 글쓰기 시간 추정 vs 실제 측정

지금 `reading_time`은 있지만 **작성/수정 시간**이 없습니다.

### 구현 방법

```yaml
# 프론트매터에 추가
estimated_writing_time: "30분"   # 시스템이 초안 생성 후 예상치 제공
actual_writing_time: "45분"      # 사용자가 수정 완료 후 기록
draft_quality: 3                 # 초안 품질 평가 (1~5), 사용자 피드백
```

### 기대 효과
- 누적되면 **"T-06은 평균 수정 시간이 2배 길다"** 패턴 발견
- 초안 품질이 낮은 Thesis → LLM 프롬프트 개선 포인트 발견
- 현실적인 **블로그 작성 시간 계획** 수립 가능

---

## 우선순위 요약

| 제안 | 구현 난이도 | 즉시 가치 | 추천 시기 |
|---|---|---|---|
| **④ 출처 신뢰도 필터** | ⭐ (yaml만 추가) | 높음 | **Phase 1과 함께** |
| **③ 시리즈 연결** | ⭐ (yaml만 추가) | 보통 | **Phase 1과 함께** |
| **② 발행 캘린더** | ⭐⭐ | 높음 | Phase 2 이후 |
| **⑤ 독자 질문 수집** | ⭐⭐ | 높음 | Phase 2 이후 |
| **① 성과 추적** | ⭐⭐⭐ | 높음 (장기) | Phase 3 이후 |
| **⑥ 작성 시간 측정** | ⭐ | 낮음 | 여유 있을 때 |

> [!TIP]
> **즉시 적용 권장**: ④ 출처 신뢰도와 ③ 시리즈 연결은 YAML 필드 추가만으로 구현되므로, Phase 1 시작 시 `sources.yaml`과 블로그 프론트매터에 바로 반영하는 것을 권장합니다.
