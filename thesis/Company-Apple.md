---
aliases:
  - Apple
  - 애플
  - AAPL
type: company
ticker: "AAPL"
sector: 온디바이스 AI / 디바이스
created: 2026-09-06
---

# 🏢 Apple (애플 | AAPL)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
Apple Intelligence와 차세대 Apple Silicon(M/A 시리즈)을 통해 20억 대 활성 기기 기반의 온디바이스 AI 슈퍼사이클을 주도.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- [[T5-01-온디바이스-AI의-변화|T5-01]]
- [[T5-02-행동형-AI-에이전트와-모바일-교체-슈퍼사이클|T5-02]]
- [[T5-04-AI-스마트-글래스와-경량-AR-광학계|T5-04]]

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "output" OR ""
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "Apple")
SORT file.mtime DESC
LIMIT 8
```
