---
confidence: 75
direction: bullish
hypothesis: 전력망 부족에 직면한 빅테크들이 24/7 기저부하 확보를 위해 SMR 개발사와 장기 전력구매계약(PPA)을 직접 체결한다
id: T1-03
keywords:
- SMR
- 소형모듈원전
- 전력PPA
- 무탄소에너지
- 원자력발전
- 기저부하
last_checked: null
last_ranked: 2026-09-07T19:30
milestone: 빅테크-SMR 기업 간 상업적 전력 공급 계약(PPA) 공식 체결
momentum: 85.0
news_count: 1
priority: 4
rank: 31
related_companies:
- NuScale
- Oklo
- Constellation Energy
- 두산에너빌리티
- MS
- 아마존
related_theses:
- T5-09
- T6-06
status: active
time_horizon: 2027~2028
title: SMR과 데이터센터 무탄소 전력 PPA
aliases:
- T1-03
- T1-03 SMR과 데이터센터 무탄소 전력 PPA
- T2-06
- T2-06 SMR과 데이터센터 무탄소 전력 PPA
- T-13
- T-13 SMR과 데이터센터 무탄소 전력 PPA
- SMR과 데이터센터 무탄소 전력 PPA
sector: AI 데이터센터 & 전력·냉각 물리 인프라
sector_id: T1
thesis_nature: consensus
stack_layer: L2
stack_name: L2 (물리인프라)
geography:
- US
- KR
related_vs: []
old_id: T-13
previous_id: DC-03
---

# T1-03 SMR과 데이터센터 무탄소 전력 PPA

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]] ➔ [[00-Argus-Master-MOC#2-⚡-ai-데이터센터--전력냉각-인프라-power--infrastructure|AI 인프라 & 전력·냉각]]

> 🏷️ **교차 분석 메타데이터**:
> - **성격**: `🚀 주류 성장 (Consensus)` | **스택**: `L2 (물리인프라)` | **시계**: `2027~2028`
> - **공급망 권역**: `US`, `KR` | **핵심 대결 구도**: 해당 없음

---

## 🎯 핵심 가설
전력망 부족에 직면한 빅테크들이 24/7 기저부하 확보를 위해 SMR 개발사와 장기 전력구매계약(PPA)을 직접 체결한다

---

## 🔗 테제 네트워크 (상호 연관 가설)

```mermaid
graph LR
    P_T_01["[[T1-01-데이터센터의-변화|T1-01 데이터센터의 변화]]"] --> T_T_13["★ [[T1-03-SMR과-데이터센터-무탄소-전력-PPA|T1-03 SMR과 데이터센터 무탄소 전력 PPA]]"]
    T_T_13["★ [[T1-03-SMR과-데이터센터-무탄소-전력-PPA|T1-03 SMR과 데이터센터 무탄소 전력 PPA]]"] --> D_T_22["[[T1-04-AI-전력망용-대용량-ESS와-LFP-공급망|T1-04 AI 전력망용 대용량 ESS와 LFP 공급망]]"]
    T_T_13["★ [[T1-03-SMR과-데이터센터-무탄소-전력-PPA|T1-03 SMR과 데이터센터 무탄소 전력 PPA]]"] <.-> S_T_23["[[T1-05-변압기-초고압-그리드-쇼티지-장기화|T1-05 변압기·초고압 그리드 쇼티지 장기화]]"]
```

- 🔼 **선행 가설 (배경 요인 & 상위 인프라)**:
  - [[T1-01-데이터센터의-변화|T1-01 데이터센터의 변화]] — 기저부하 무탄소 전력 수요
- ➡️ **동반 및 대체·경쟁 가설**:
  - [[T1-05-변압기-초고압-그리드-쇼티지-장기화|T1-05 변압기·초고압 그리드 쇼티지 장기화]] — 그리드 접속 지연 대안
- 🔽 **파생 및 후행 병목 가설**:
  - [[T1-04-AI-전력망용-대용량-ESS와-LFP-공급망|T1-04 AI 전력망용 대용량 ESS와 LFP 공급망]] — 원전-ESS 하이브리드 PPA

---

## 🏢 연관 기업 & 핵심 기술 허브
- **핵심 기업**: [[Company-NuScale|NuScale]], [[Company-Oklo|Oklo]], [[Company-Constellation Energy|Constellation Energy]], [[Company-두산에너빌리티|두산에너빌리티]], [[Company-MS|MS]], [[Company-아마존|아마존]]
- **핵심 기술/토픽**: [[Topic-SMR|SMR]], [[Topic-전력그리드|전력그리드]]

---

## 📈 지지 근거


---

## 📉 반박 근거


---

## 📑 관련 산출물 (자동 집계)

### 🤖 Dataview 실시간 역방향 링크
```dataview
TABLE file.mtime AS "작성일", angle AS "관점", tags AS "태그"
FROM "argus" OR "output" OR ""
WHERE contains(thesis, "T3-03") OR contains(thesis, "T3-03") OR contains(file.outlinks, this.file.link)
SORT file.mtime DESC
LIMIT 7
```

### 📌 수동 링크 아카이브


---

## 📝 분석가 메모

