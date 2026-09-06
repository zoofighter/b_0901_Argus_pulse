---
aliases:
  - 3D DRAM
  - 3DDRAM
  - 400단낸드
  - V-NAND
  - 3D메모리
type: topic
category: 차세대 메모리
created: 2026-09-06
---

# 💡 3D DRAM & 400단 V-NAND 고단화

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 개념 개요 및 산업 변곡점
셀을 수직으로 세우는 3D D램 아키텍처와 400단 이상 초고단 V-NAND 적층을 통한 메모리 미세화 한계 극복 기술.

---

## 🔗 연관 투자 테제 매핑 (Theses Network)
- [[T-02-메모리-산업의-변화|T-02]]
- [[T-07-CXL-메모리의-확대|T-07]]
- [[T-28-3D-DRAM-기술-전환과-400단-V-NAND|T-28]]

---

## 🏢 핵심 플레이어 및 공급망
- **주요 기업**: [[Company-SK하이닉스|SK하이닉스]], [[Company-삼성전자|삼성전자]], [[Company-Micron|Micron]], [[Company-Tokyo Electron|Tokyo Electron]], [[Company-Applied Materials|Applied Materials]]

---

## 📑 관련 분석 리포트 (Dataview)

```dataview
TABLE file.mtime AS "작성일", title AS "제목", angle AS "관점"
FROM "argus" OR "output"
WHERE contains(file.tags, "3D DRAM") OR contains(file.text, "3D DRAM")
SORT file.mtime DESC
LIMIT 8
```
