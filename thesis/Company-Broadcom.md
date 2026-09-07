---
aliases:
  - Broadcom
  - 브로드컴
  - AVGO
type: company
ticker: "AVGO"
sector: 커스텀 ASIC / 네트워킹
created: 2026-09-06
---

# 🏢 Broadcom (AVGO)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
구글 TPU, 메타 MTIA 등 빅테크 커스텀 ASIC 설계 및 CPO/초고속 네트워킹 칩셋 시장의 절대 강자.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- [[T2-11-TPU-증가와-GPU-수요-둔화|T4-04]]
- [[T3-01-실리콘-포토닉스와-CPO의-상용화|T3-01]]
- [[T2-08-빅테크-커스텀-ASIC-증가와-DSP-생태계|T2-08]]
- [[T3-02-초고속-AI-네트워킹-UEC-vs-인피니밴드|T3-02]]

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "output" OR ""
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "Broadcom")
SORT file.mtime DESC
LIMIT 8
```
