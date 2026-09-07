---
aliases:
  - Meta
  - 메타
  - META
type: company
ticker: "META"
sector: AI 소프트웨어 / 오픈소스
created: 2026-09-06
---

# 🏢 Meta Platforms (META)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
오픈소스 LLM(Llama) 생태계와 Ray-Ban 스마트글래스 및 자체 MTIA 가속기를 통해 AI 생태계를 주도.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- [[T6-01-금리와-데이터센터|T6-01]]
- [[T4-01-오픈소스-모델-고도화와-온프레미스-사설-AI|T4-01]]
- [[T5-04-AI-스마트-글래스와-경량-AR-광학계|T5-04]]
- [[T6-03-AI-버블-가능성|T6-03]]

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "output" OR ""
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "Meta")
SORT file.mtime DESC
LIMIT 8
```
