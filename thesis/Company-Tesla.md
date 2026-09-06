---
aliases:
  - Tesla
  - 테슬라
  - TSLA
type: company
ticker: "TSLA"
sector: 피지컬 AI / 모빌리티
created: 2026-09-06
---

# 🏢 Tesla (테슬라 | TSLA)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
FSD(자율주행), Optimus(휴머노이드 로봇), Megapack(대용량 ESS)을 아우르는 피지컬 AI 및 에너지 통합 기업.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- [[T3-03-휴머노이드-로봇과-액추에이터-공급망|T3-03]]
- [[T3-04-End-to-End-AI-자율주행과-로보택시|T3-04]]
- [[T3-05-피지컬-AI와-공간지능-반도체|T3-05]]
- [[T2-04-AI-전력망용-대용량-ESS와-LFP-공급망|T3-04]]
- [[T3-09-피지컬AI와-로봇의-상용화|T3-09]]

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "output" OR ""
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "Tesla")
SORT file.mtime DESC
LIMIT 8
```
