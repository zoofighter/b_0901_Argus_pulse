---
aliases:
  - ESS
  - 에너지저장장치
  - BESS
  - LFP배터리
  - Energy Storage System
type: topic
category: 배터리 / 신재생
created: 2026-09-06
---

# 💡 대용량 ESS & LFP 배터리 공급망

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 개념 개요 및 산업 변곡점
데이터센터 피크 전력 완화 및 신재생 전력 간헐성 해소를 위한 52조원 규모 북미 BESS 시장과 LFP 배터리 공급망.

---

## 🔗 연관 투자 테제 매핑 (Theses Network)
- [[T3-01-전고체-배터리의-변화|T3-01]]
- [[T2-04-AI-전력망용-대용량-ESS와-LFP-공급망|T3-04]]
- [[T2-06-ESS와-한국배터리의-미국수혜|T3-06]]

---

## 🏢 핵심 플레이어 및 공급망
- **주요 기업**: [[Company-LG에너지솔루션|LG에너지솔루션]], [[Company-삼성SDI|삼성SDI]], [[Company-Tesla|Tesla]], [[Company-Fluence Energy|Fluence Energy]], [[Company-CATL|CATL]]

---

## 📑 관련 분석 리포트 (Dataview)

```dataview
TABLE file.mtime AS "작성일", title AS "제목", angle AS "관점"
FROM "argus" OR "output" OR ""
WHERE contains(file.tags, "ESS") OR contains(file.text, "ESS")
SORT file.mtime DESC
LIMIT 8
```
