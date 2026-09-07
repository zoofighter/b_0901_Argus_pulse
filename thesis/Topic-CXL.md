---
aliases:
  - CXL
  - 컴퓨트익스프레스링크
  - CMM-D
  - 메모리풀링
  - CXL2.0
  - CXL3.0
type: topic
category: 차세대 메모리
created: 2026-09-06
---

# 💡 CXL (Compute Express Link) 메모리 풀링

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 개념 개요 및 산업 변곡점
PCIe 기반으로 CPU·GPU·가속기 간 메모리를 공유하고 풀링(Pooling)하여 데이터센터 메모리 용량 한계를 극복하는 표준 인터커넥트.

---

## 🔗 연관 투자 테제 매핑 (Theses Network)
- [[T2-01-메모리-산업의-변화|T2-01]]
- [[T2-06-CXL-메모리의-확대|T2-06]]
- [[T2-05-3D-DRAM-기술-전환과-400단-V-NAND|T2-05]]
- [[T2-10-메모리-2028년-피크아웃|T2-10]]

---

## 🏢 핵심 플레이어 및 공급망
- **주요 기업**: [[Company-삼성전자|삼성전자]], [[Company-SK하이닉스|SK하이닉스]], [[Company-Micron|Micron]], [[Company-Astera Labs|Astera Labs]], [[Company-Montage|Montage]]

---

## 📑 관련 분석 리포트 (Dataview)

```dataview
TABLE file.mtime AS "작성일", title AS "제목", angle AS "관점"
FROM "argus" OR "output" OR ""
WHERE contains(file.tags, "CXL") OR contains(file.text, "CXL")
SORT file.mtime DESC
LIMIT 8
```
