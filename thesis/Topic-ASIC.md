---
aliases:
  - ASIC
  - 커스텀ASIC
  - LPU
  - DSP
  - 디자인하우스
  - 주문형반도체
type: topic
category: 반도체 아키텍처
created: 2026-09-06
---

# 💡 빅테크 커스텀 ASIC & LPU·DSP 생태계

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 개념 개요 및 산업 변곡점
엔비디아 GPU 의존도를 낮추고 추론 비용을 절감하기 위한 구글 TPU, 메타 MTIA 등 빅테크 맞춤형 가속기 및 DSP 디자인 생태계.

---

## 🔗 연관 투자 테제 매핑 (Theses Network)
- [[T3-02-온디바이스-AI의-변화|T3-02]]
- [[T1-02-TPU-증가와-GPU-수요-둔화|T1-02]]
- [[T4-02-엔비디아와-네오클라우드|T4-02]]
- [[T1-07-AI-추론-시장-폭발과-LPU-ASIC-분화|T1-07]]
- [[T1-09-빅테크-커스텀-ASIC-증가와-DSP-생태계|T1-09]]
- [[T5-02-AI-소프트웨어-레이어의-과점화|T5-02]]
- [[T5-03-바이오AI와-신약개발-가속|T5-03]]
- [[T4-04-AI-버블-가능성|T4-04]]

---

## 🏢 핵심 플레이어 및 공급망
- **주요 기업**: [[Company-Broadcom|Broadcom]], [[Company-Marvell|Marvell]], [[Company-Groq|Groq]], [[Company-ARM|ARM]], [[Company-가온칩스|가온칩스]], [[Company-에이직랜드|에이직랜드]]

---

## 📑 관련 분석 리포트 (Dataview)

```dataview
TABLE file.mtime AS "작성일", title AS "제목", angle AS "관점"
FROM "argus" OR "output" OR ""
WHERE contains(file.tags, "ASIC") OR contains(file.text, "ASIC")
SORT file.mtime DESC
LIMIT 8
```
