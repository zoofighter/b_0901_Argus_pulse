---
aliases:
  - CoreWeave
  - 코어위브
type: company
ticker: "Private"
sector: GPU 특화 클라우드
created: 2026-09-06
---

# 🏢 CoreWeave (코어위브)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
엔비디아 GPU를 담보로 대규모 차입을 일으켜 GPU 클라우드 인프라를 확장하는 네오클라우드의 대표 주자.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- [[T6-09-엔비디아와-네오클라우드|T3-04]]
- [[T6-02-엔비디아와-GPU-금융|T6-02]]
- [[T6-03-AI-버블-가능성|T6-03]]

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "output" OR ""
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "CoreWeave")
SORT file.mtime DESC
LIMIT 8
```
