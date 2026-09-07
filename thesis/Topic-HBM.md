---
aliases:
  - HBM
  - 고대역폭메모리
  - High Bandwidth Memory
  - HBM3E
  - HBM4
  - 커스텀HBM
type: topic
category: 반도체 하드웨어
created: 2026-09-06
---

# 💡 HBM (High Bandwidth Memory & Custom ASIC)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 개념 개요 및 산업 변곡점
여러 개의 D램 다이를 TSV 기술로 적층한 고대역폭 메모리. HBM4부터 4nm 베이스 다이를 탑재한 커스텀 ASIC으로 진화.

---

## 🔗 연관 투자 테제 매핑 (Theses Network)
- [[T2-01-메모리-산업의-변화|T2-01]]
- [[T2-06-CXL-메모리의-확대|T2-06]]
- [[T2-02-첨단-패키징과-CoWoS의-병목|T2-02]]
- [[T2-03-유리기판의-차세대-패키징-침투|T2-03]]
- [[T2-05-3D-DRAM-기술-전환과-400단-V-NAND|T2-05]]
- [[T2-09-반도체-소부장의-내재화|T2-09]]
- [[T2-10-메모리-2028년-피크아웃|T2-10]]
- [[T6-07-중국반도체의-HBM-생산가능성|T6-07]]

---

## 🏢 핵심 플레이어 및 공급망
- **주요 기업**: [[Company-SK하이닉스|SK하이닉스]], [[Company-삼성전자|삼성전자]], [[Company-Micron|Micron]], [[Company-NVIDIA|NVIDIA]], [[Company-TSMC|TSMC]], [[Company-한미반도체|한미반도체]]

---

## 📑 관련 분석 리포트 (Dataview)

```dataview
TABLE file.mtime AS "작성일", title AS "제목", angle AS "관점"
FROM "argus" OR "output" OR ""
WHERE contains(file.tags, "HBM") OR contains(file.text, "HBM")
SORT file.mtime DESC
LIMIT 8
```
