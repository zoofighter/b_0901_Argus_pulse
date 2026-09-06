---
aliases:
  - 실리콘포토닉스
  - CPO
  - 광인터커넥트
  - Optical Interconnect
  - Silicon Photonics
type: topic
category: 네트워킹 / 광학
created: 2026-09-06
---

# 💡 실리콘 포토닉스 & CPO (Co-Packaged Optics)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 개념 개요 및 산업 변곡점
전기 신호 대신 빛(광자)을 사용하여 칩 간 대용량 데이터를 초저지연·초저전력으로 전송하는 광반도체 기술.

---

## 🔗 연관 투자 테제 매핑 (Theses Network)
- [[T-01-데이터센터의-변화|T-01]]
- [[T-14-실리콘-포토닉스와-CPO의-상용화|T-14]]
- [[T-29-초고속-AI-네트워킹-UEC-vs-인피니밴드|T-29]]

---

## 🏢 핵심 플레이어 및 공급망
- **주요 기업**: [[Company-Broadcom|Broadcom]], [[Company-TSMC|TSMC]], [[Company-Marvell|Marvell]], [[Company-Coherent|Coherent]], [[Company-Cisco|Cisco]]

---

## 📑 관련 분석 리포트 (Dataview)

```dataview
TABLE file.mtime AS "작성일", title AS "제목", angle AS "관점"
FROM "argus" OR "output"
WHERE contains(file.tags, "실리콘포토닉스") OR contains(file.text, "실리콘포토닉스")
SORT file.mtime DESC
LIMIT 8
```
