---
aliases:
  - 액체냉각
  - DLC
  - CDU
  - 침전냉각
  - Direct Liquid Cooling
  - Liquid Cooling
type: topic
category: AI 인프라 / 냉각
created: 2026-09-06
---

# 💡 데이터센터 액체냉각 & DLC (Direct Liquid Cooling)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 개념 개요 및 산업 변곡점
랙당 100kW+ 시대를 맞아 공랭식의 한계를 극복하는 직접액체냉각(DLC), CDU, 침전냉각 기술. PUE 1.1 달성의 필수 솔루션.

---

## 🔗 연관 투자 테제 매핑 (Theses Network)
- [[T-01-데이터센터의-변화|T-01]]
- [[T-05-금리와-데이터센터|T-05]]
- [[T-12-데이터센터-액체냉각의-표준화|T-12]]

---

## 🏢 핵심 플레이어 및 공급망
- **주요 기업**: [[Company-Vertiv|Vertiv]], [[Company-Supermicro|Supermicro]], [[Company-Schneider|Schneider]], [[Company-CoolIT|CoolIT]]

---

## 📑 관련 분석 리포트 (Dataview)

```dataview
TABLE file.mtime AS "작성일", title AS "제목", angle AS "관점"
FROM "argus" OR "output"
WHERE contains(file.tags, "액체냉각") OR contains(file.text, "액체냉각")
SORT file.mtime DESC
LIMIT 8
```
