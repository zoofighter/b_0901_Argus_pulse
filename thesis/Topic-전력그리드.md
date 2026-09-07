---
aliases:
  - 변압기
  - 초고압그리드
  - HVDC
  - 전력망
  - Power Grid
type: topic
category: AI 인프라 / 전력
created: 2026-09-06
---

# 💡 전력 그리드 & 변압기·HVDC 인프라

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 개념 개요 및 산업 변곡점
데이터센터 전력 인입 지연을 유발하는 초고압 변압기, 전력망 인터커넥션 큐, HVDC 초고압 직류 송전망 쇼티지 생태계.

---

## 🔗 연관 투자 테제 매핑 (Theses Network)
- [[T1-01-데이터센터의-변화|T1-01]]
- [[T6-01-금리와-데이터센터|T6-01]]
- [[T1-03-SMR과-데이터센터-무탄소-전력-PPA|T1-03]]
- [[T1-04-AI-전력망용-대용량-ESS와-LFP-공급망|T1-04]]
- [[T1-05-변압기-초고압-그리드-쇼티지-장기화|T1-05]]
- [[T6-04-10년금리-5%-재진입-가능성|T6-04]]

---

## 🏢 핵심 플레이어 및 공급망
- **주요 기업**: [[Company-HD현대일렉트릭|HD현대일렉트릭]], [[Company-Eaton|Eaton]], [[Company-효성중공업|효성중공업]], [[Company-LS일렉트릭|LS일렉트릭]], [[Company-Schneider|Schneider]]

---

## 📑 관련 분석 리포트 (Dataview)

```dataview
TABLE file.mtime AS "작성일", title AS "제목", angle AS "관점"
FROM "argus" OR "output" OR ""
WHERE contains(file.tags, "변압기") OR contains(file.text, "변압기")
SORT file.mtime DESC
LIMIT 8
```
