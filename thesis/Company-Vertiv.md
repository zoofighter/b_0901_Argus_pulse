---
aliases:
  - Vertiv
  - 버티브
  - VRT
type: company
ticker: "VRT"
sector: 데이터센터 전력·냉각
created: 2026-09-06
---

# 🏢 Vertiv Holdings (VRT)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
AI 고밀도 랙에 필수적인 액체냉각(CDU/DLC) 및 무정전 전원장치(UPS) 분야 글로벌 1위 기업.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- [[T1-01-데이터센터의-변화|T1-01]]
- [[T1-02-데이터센터-액체냉각의-표준화|T1-02]]

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "output" OR ""
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "Vertiv")
SORT file.mtime DESC
LIMIT 8
```
