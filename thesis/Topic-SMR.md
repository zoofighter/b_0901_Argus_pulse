---
aliases:
  - SMR
  - 소형모듈원전
  - 원자력PPA
  - 무탄소전력
  - Small Modular Reactor
type: topic
category: 에너지 / 전력
created: 2026-09-06
---

# 💡 SMR (소형 모듈 원자로) & 무탄소 전력 PPA

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 개념 개요 및 산업 변곡점
AI 데이터센터의 24/7 무탄소 기저부하 전력 공급을 위한 차세대 소형 원전 및 빅테크 전력구매계약(PPA) 생태계.

---

## 🔗 연관 투자 테제 매핑 (Theses Network)
- [[T1-01-데이터센터의-변화|T1-01]]
- [[T1-03-SMR과-데이터센터-무탄소-전력-PPA|T1-03]]
- [[T1-05-변압기-초고압-그리드-쇼티지-장기화|T1-05]]

---

## 🏢 핵심 플레이어 및 공급망
- **주요 기업**: [[Company-NuScale|NuScale]], [[Company-Constellation Energy|Constellation Energy]], [[Company-Oklo|Oklo]], [[Company-두산에너빌리티|두산에너빌리티]]

---

## 📑 관련 분석 리포트 (Dataview)

```dataview
TABLE file.mtime AS "작성일", title AS "제목", angle AS "관점"
FROM "argus" OR "output" OR ""
WHERE contains(file.tags, "SMR") OR contains(file.text, "SMR")
SORT file.mtime DESC
LIMIT 8
```
