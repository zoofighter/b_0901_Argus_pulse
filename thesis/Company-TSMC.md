---
aliases:
  - TSMC
  - TSM
  - 대만적체전로
type: company
ticker: "TSM"
sector: 파운드리 / 첨단 패키징
created: 2026-09-06
---

# 🏢 TSMC (TSM)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
글로벌 파운드리 60%+ 점유율과 CoWoS 첨단 패키징 생태계를 독점하여 엔비디아, 애플, 빅테크 커스텀 칩을 전량 위탁 생산하는 핵심 인프라.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- [[T2-01-데이터센터의-변화|T3-01]]
- [[T1-01-메모리-산업의-변화|T1-01]]
- [[T1-04-첨단-패키징과-CoWoS의-병목|T1-04]]
- [[T1-05-유리기판의-차세대-패키징-침투|T1-05]]
- [[T1-06-실리콘-포토닉스와-CPO의-상용화|T1-06]]
- [[T1-08-파운드리-2nm-공정과-GAA-격돌|T1-08]]
- [[T1-09-빅테크-커스텀-ASIC-증가와-DSP-생태계|T1-09]]

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "output" OR ""
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "TSMC")
SORT file.mtime DESC
LIMIT 8
```
