---
aliases:
  - UEC
  - 인피니밴드
  - Ultra Ethernet
  - InfiniBand
  - AI네트워킹
type: topic
category: AI 인프라 / 네트워킹
created: 2026-09-06
---

# 💡 초고속 AI 네트워킹 (UEC vs 인피니밴드)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 개념 개요 및 산업 변곡점
수만 개 가속기를 묶는 AI 클러스터에서 엔비디아 인피니밴드 독점망과 빅테크 연합의 울트라 이더넷(UEC) 간 표준 경쟁.

---

## 🔗 연관 투자 테제 매핑 (Theses Network)
- [[T1-01-데이터센터의-변화|T1-01]]
- [[T3-01-실리콘-포토닉스와-CPO의-상용화|T3-01]]
- [[T3-02-초고속-AI-네트워킹-UEC-vs-인피니밴드|T3-02]]

---

## 🏢 핵심 플레이어 및 공급망
- **주요 기업**: [[Company-Arista Networks|Arista Networks]], [[Company-NVIDIA|NVIDIA]], [[Company-Cisco|Cisco]], [[Company-Broadcom|Broadcom]], [[Company-Marvell|Marvell]]

---

## 📑 관련 분석 리포트 (Dataview)

```dataview
TABLE file.mtime AS "작성일", title AS "제목", angle AS "관점"
FROM "argus" OR "output" OR ""
WHERE contains(file.tags, "UEC") OR contains(file.text, "UEC")
SORT file.mtime DESC
LIMIT 8
```
