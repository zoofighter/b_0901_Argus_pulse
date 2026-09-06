---
aliases:
  - 공랭 vs 액랭
  - Air vs Liquid Cooling
  - 데이터센터 냉각 표준
type: vs_hub
category: 제로섬 대결 & 트레이드오프
created: 2026-09-06
---

# ⚔️ 레거시 공랭식 (Air Cooling) vs 직접액체냉각 (DLC & CDU)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]] ➔ [[00-Argus-Master-MOC#⚔️-핵심-기술--진영-대결-구도-versus-hubs|대결 허브]]

---

## 📌 대결 구도 개요 및 핵심 쟁점
랙당 40kW 이하 전통적 팬 공랭식 냉각과 블랙웰 GB200(랙당 120kW+) 시대를 맞아 PUE 1.1을 달성하기 위한 CDU 및 DLC(Direct Liquid Cooling) 직접 액체냉각 간의 인프라 전환 격돌.

> ⚡ **핵심 충돌 지점**:  
> **기존 레거시 설비의 감가상각 유지 vs 고밀도 연산 칩셋의 물리적 발열 임계 돌파**

---

## 🔗 관련 투자 테제군 (Theses Network)
- [[T2-01-데이터센터의-변화|T3-01]]
- [[T2-02-데이터센터-액체냉각의-표준화|T3-02]]

---

## 🏢 대결 진영별 핵심 기업 (Players)
- **주요 플레이어**: [[Company-Vertiv|Vertiv]], [[Company-Supermicro|Supermicro]], [[Company-Schneider|Schneider]], [[Company-CoolIT|CoolIT]]

---

## 📑 관련 분석 리포트 및 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", title AS "제목", tags AS "태그"
FROM "argus" OR "output" OR ""
WHERE contains(file.text, "공랭 vs 액랭") OR contains(file.outlinks, this.file.link)
SORT file.mtime DESC
LIMIT 8
```
