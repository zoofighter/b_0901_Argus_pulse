---
aliases:
  - Alphabet
  - 구글
  - Google
  - GOOGL
type: company
ticker: "GOOGL"
sector: AI 가속기 / 클라우드
created: 2026-09-06
---

# 🏢 Alphabet (구글 | GOOGL)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
자체 TPU v5/v6 아키텍처와 Gemini 모델, Waymo 로보택시를 앞세워 하드웨어부터 서비스까지 풀스택 AI를 구축.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- [[T5-01-온디바이스-AI의-변화|T5-01]]
- [[T2-11-TPU-증가와-GPU-수요-둔화|T4-04]]
- [[T5-05-End-to-End-AI-자율주행과-로보택시|T5-05]]
- [[T4-02-AI-소프트웨어-레이어의-과점화|T4-02]]
- [[T6-03-AI-버블-가능성|T6-03]]

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "output" OR ""
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "Alphabet")
SORT file.mtime DESC
LIMIT 8
```
