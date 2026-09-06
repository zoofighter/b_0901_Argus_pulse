# 📊 옵시디언 Dataview 다차원 쿼리 작성법 및 실전 레시피북 (Cookbook)

> **작성일**: 2026-09-06  
> **시스템**: Argus Pulse / Obsidian Knowledge Graph System  
> **목적**: 옵시디언 Dataview 플러그인을 활용하여 테제 문서의 Frontmatter 메타데이터(`sector`, `thesis_nature`, `stack_layer`, `geography`, `momentum` 등)를 바탕으로 다차원 투자 분석 대시보드를 구축하는 종합 실전 가이드

---

## 1. Dataview 쿼리 기본 문법 구조 (DQL 기초)

옵시디언의 Dataview는 마크다운 문서의 Frontmatter(YAML) 속성을 데이터베이스 테이블처럼 조회하는 쿼리 언어(DQL)입니다.

````markdown
```dataview
TABLE 필드1 AS "표시이름", 필드2 AS "표시이름"
FROM "폴더경로" OR #태그
WHERE 조건문
SORT 정렬기준 ASC|DESC
LIMIT 개수
```
````

### 핵심 키워드 설명

| 절 (Clause) | 설명 | 주요 예시 |
|:---|:---|:---|
| **`TABLE`** / **`LIST`** | 결과물을 표(Table) 또는 목록(List)으로 렌더링 | `TABLE confidence + "%" AS "신뢰도", momentum AS "모멘텀"` |
| **`FROM`** | 탐색할 대상 폴더나 태그 범위 지정 | `FROM "argus/Theses"` 또는 `FROM #invest` |
| **`WHERE`** | 특정 조건의 데이터만 필터링 (AND, OR, contains, !=, >, <) | `WHERE thesis_nature = "contrarian" AND confidence >= 60` |
| **`FLATTEN`** | 리스트/배열 속성(예: `geography: [KR, US]`)을 1개씩 행으로 분해 | `FLATTEN geography AS geo` |
| **`GROUP BY`** | 특정 속성 기준으로 묶어서 그룹화 | `GROUP BY sector` |
| **`SORT`** | 정렬 기준 (오름차순 `ASC`, 내림차순 `DESC`) | `SORT momentum DESC` |
| **`LIMIT`** | 출력할 최대 행 개수 제한 | `LIMIT 10` |

---

## 2. 실전 다차원 뷰 레시피 6종 (Copy & Paste)

아래 쿼리 블록들을 옵시디언 노트의 원하는 위치에 그대로 복사하여 붙여넣으시면 실시간 대시보드가 동작합니다.

---

### 📌 레시피 1: 🛡️ 역발상 & 헷지 테제 전용 대시보드 (Contrarian Dashboard)
> 시장 과열 국면에서 꼬리 리스크를 방어하고 헷지할 수 있는 가설 7종을 모아보는 뷰입니다.

````markdown
```dataview
TABLE 
    hypothesis AS "핵심 가설",
    sector AS "소속 섹터",
    confidence + "%" AS "신뢰도",
    momentum AS "모멘텀 점수",
    related_vs AS "연관 대결"
FROM "argus/Theses"
WHERE thesis_nature = "contrarian"
SORT momentum DESC
```
````

---

### 📌 레시피 2: 🧱 6계층 밸류체인 수직 스택 파이프라인 뷰 (Stack Layer View)
> 원자재/소부장(L0)부터 엔드 디바이스(L5)까지 산업의 병목 흐름 순으로 전체 테제를 정렬합니다.

````markdown
```dataview
TABLE 
    stack_name AS "스택 레이어",
    title AS "가설 제목",
    priority AS "우선도 (1~5)",
    related_companies AS "핵심 기업"
FROM "argus/Theses"
SORT stack_layer ASC, rank ASC
```
````

---

### 📌 레시피 3: 📂 6대 섹터별 자동 그룹화 뷰 (GROUP BY Sector)
> 6대 섹터별로 묶어서 하위 소속 테제들의 목록과 개수를 자동 집계합니다.

````markdown
```dataview
TABLE 
    length(rows) AS "테제 수",
    rows.file.link AS "소속 테제 목록"
FROM "argus/Theses"
GROUP BY sector
SORT length(rows) DESC
```
````

---

### 📌 레시피 4: 🗺️ 한국(KR) 핵심 공급망 수혜 뷰 (Korea Alpha View)
> `geography` 배열에 `KR`이 포함된 테제만 필터링하여 모멘텀 순으로 상위 10개를 출력합니다.

````markdown
```dataview
TABLE 
    title AS "가설 제목",
    stack_name AS "스택 레이어",
    thesis_nature AS "성격",
    momentum AS "모멘텀 점수",
    rank AS "시장 순위"
FROM "argus/Theses"
WHERE contains(geography, "KR")
SORT momentum DESC
LIMIT 10
```
````

---

### 📌 레시피 5: 🔥 최근 시장 모멘텀 Top 10 랭킹 뷰
> 최근 2일간 뉴스 데이터 점수와 신뢰도가 결합된 최상위 10개 핫 테제를 추적합니다.

````markdown
```dataview
TABLE 
    rank AS "순위",
    sector AS "섹터",
    news_count AS "뉴스(건)",
    momentum AS "모멘텀 종합점수",
    direction AS "방향성"
FROM "argus/Theses"
WHERE rank != null
SORT rank ASC
LIMIT 10
```
````

---

### 📌 레시피 6: 🏢 특정 기업(예: SK하이닉스) 맞춤형 교차 집계 뷰
> 기업 허브 문서(`SK하이닉스.md`) 안에서 해당 기업과 얽힌 테제 및 최근 블로그를 자동으로 불러옵니다.

````markdown
```dataview
TABLE 
    title AS "가설 제목",
    thesis_nature AS "성격",
    stack_name AS "스택",
    momentum AS "모멘텀"
FROM "argus/Theses"
WHERE contains(related_companies, "SK하이닉스") OR contains(file.text, "SK하이닉스")
SORT momentum DESC
```
````

---

## 3. 고급 활용: DataviewJS로 시각적 프로그레스 바(Progress Bar) 만들기

`dataviewjs`를 활용하면 자바스크립트로 **신뢰도 게이지 바(`████░░░░ 75%`)**와 뱃지를 렌더링할 수 있습니다.

````markdown
```dataviewjs
let pages = dv.pages('"argus/Theses"')
    .where(p => p.confidence != null)
    .sort(p => p.confidence, 'desc')
    .slice(0, 10);

function renderBar(score) {
    const total = 10;
    const filled = Math.round((score / 100) * total);
    return "█".repeat(filled) + "░".repeat(total - filled) + ` ${score}%`;
}

dv.table(
    ["테제", "섹터", "신뢰도 게이지", "성격", "스택"],
    pages.map(p => [
        p.file.link,
        p.sector_id || p.sector,
        renderBar(p.confidence),
        p.thesis_nature === "consensus" ? "🚀 주류" : "🛡️ 헷지",
        p.stack_name || p.stack_layer
    ])
);
```
````

---

## 4. 옵시디언 Dataview 플러그인 활성화 설정

Dataview 쿼리가 정상적으로 표 형태로 보이려면 옵시디언 앱에서 아래 2가지 설정이 활성화되어 있어야 합니다:

1. **설정(Settings ⚙️)** ➔ **커뮤니티 플러그인(Community plugins)** ➔ **Dataview** 검색 후 설치 및 활성화
2. **Dataview 세부 옵션**:
   - ✅ **Enable JavaScript Queries (`dataviewjs` 허용)**: 활성화 (프로그레스 바 및 JS 쿼리 사용 시 필수)
   - ✅ **Enable Inline Queries**: 활성화
   - ✅ **Enable Inline JavaScript Queries**: 활성화
