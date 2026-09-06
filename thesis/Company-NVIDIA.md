---
aliases:
  - NVIDIA
  - 엔비디아
  - NVDA
type: company
ticker: "NVDA"
sector: AI 반도체 / 컴퓨팅
created: 2026-09-06
---

# 🏢 NVIDIA (엔비디아 | NVDA)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
CUDA 생태계와 Hopper/Blackwell/Vera Rubin 아키텍처를 앞세워 전 세계 AI 가속기 시장을 80%+ 점유하는 글로벌 AI 대장주.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- [[T-01-데이터센터의-변화|T-01]]
- [[T-02-메모리-산업의-변화|T-02]]
- [[T-06-TPU-증가와-GPU-수요-둔화|T-06]]
- [[T-08-엔비디아와-네오클라우드|T-08]]
- [[T-09-엔비디아와-GPU-금융|T-09]]
- [[T-19-피지컬-AI와-공간지능-반도체|T-19]]
- [[T-26-소버린-AI와-국가-단위-컴퓨트-인프라|T-26]]
- [[T-29-초고속-AI-네트워킹-UEC-vs-인피니밴드|T-29]]
- [[T-37-AI-버블-가능성|T-37]]

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "output"
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "NVIDIA")
SORT file.mtime DESC
LIMIT 8
```
