---
aliases:
  - 자율주행
  - FSD
  - 로보택시
  - E2E자율주행
  - Autonomous Driving
type: topic
category: 모빌리티 / AI
created: 2026-09-06
---

# 💡 End-to-End AI 자율주행 & 로보택시

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 개념 개요 및 산업 변곡점
센서 데이터 입력부터 제어 출력까지 하나의 신경망으로 처리하는 End-to-End 신경망 자율주행 및 상용 로보택시 네트워크.

---

## 🔗 연관 투자 테제 매핑 (Theses Network)
- [[T3-02-온디바이스-AI의-변화|T3-02]]
- [[T3-04-End-to-End-AI-자율주행과-로보택시|T3-04]]
- [[T3-05-피지컬-AI와-공간지능-반도체|T3-05]]

---

## 🏢 핵심 플레이어 및 공급망
- **주요 기업**: [[Company-Tesla|Tesla]], [[Company-Waymo|Waymo]], [[Company-Cruise|Cruise]], [[Company-현대차|현대차]], [[Company-모빌아이|모빌아이]]

---

## 📑 관련 분석 리포트 (Dataview)

```dataview
TABLE file.mtime AS "작성일", title AS "제목", angle AS "관점"
FROM "argus" OR "output" OR ""
WHERE contains(file.tags, "자율주행") OR contains(file.text, "자율주행")
SORT file.mtime DESC
LIMIT 8
```
