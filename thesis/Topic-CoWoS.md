---
aliases:
  - CoWoS
  - 첨단패키징
  - 2.5D패키징
  - 인터포저
  - Advanced Packaging
type: topic
category: 반도체 패키징
created: 2026-09-06
---

# 💡 CoWoS 첨단 패키징 (Chip-on-Wafer-on-Substrate)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 개념 개요 및 산업 변곡점
실리콘 인터포저 위에 로직 다이와 HBM을 수평·수직으로 집적하는 TSMC의 독점적 첨단 2.5D 패키징 공정.

---

## 🔗 연관 투자 테제 매핑 (Theses Network)
- [[T2-01-데이터센터의-변화|T3-01]]
- [[T1-01-메모리-산업의-변화|T1-01]]
- [[T1-04-첨단-패키징과-CoWoS의-병목|T1-04]]
- [[T1-05-유리기판의-차세대-패키징-침투|T1-05]]
- [[T1-06-실리콘-포토닉스와-CPO의-상용화|T1-06]]
- [[T1-08-파운드리-2nm-공정과-GAA-격돌|T1-08]]
- [[T1-12-반도체-소부장의-내재화|T1-12]]

---

## 🏢 핵심 플레이어 및 공급망
- **주요 기업**: [[Company-TSMC|TSMC]], [[Company-ASE|ASE]], [[Company-Amkor|Amkor]], [[Company-삼성전자|삼성전자]], [[Company-SK하이닉스|SK하이닉스]], [[Company-한미반도체|한미반도체]]

---

## 📑 관련 분석 리포트 (Dataview)

```dataview
TABLE file.mtime AS "작성일", title AS "제목", angle AS "관점"
FROM "argus" OR "output" OR ""
WHERE contains(file.tags, "CoWoS") OR contains(file.text, "CoWoS")
SORT file.mtime DESC
LIMIT 8
```
