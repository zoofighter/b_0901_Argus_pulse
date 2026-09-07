---
title: "Company: LS ELECTRIC (010120)"
type: hub-company
ticker: "010120.KS"
sector: "전력 인프라 & 배전·HVDC"
related_theses:
  - "[[T1-07-800V-48V-HVDC-전력-아키텍처-혁신|T1-07]]"
  - "[[T1-05-변압기-초고압-그리드-쇼티지-장기화|T1-05]]"
  - "[[T1-01-데이터센터의-변화|T1-01]]"
tags:
  - company
  - power-grid
  - hvdc
  - distribution
---

# 🏢 Company Hub: LS ELECTRIC (LS일렉트릭)

> **한국 대표 전력기기 및 초고압 직류 송전(HVDC)·배전 선도 기업**  
> AI 데이터센터 내부의 800V 직류 배전, 초고압 변압기 및 글로벌 전력망 업그레이드 수혜를 집중적으로 받는 핵심 기업입니다.

---

## 📌 핵심 투자 포인트 & 연관 테제
- **800V/HVDC 전력 아키텍처**: **[[T1-07-800V-48V-HVDC-전력-아키텍처-혁신|T1-07]]** (초고압 직류 송전 및 데이터센터 직류 배전반)
- **변압기·배전 쇼티지**: **[[T1-05-변압기-초고압-그리드-쇼티지-장기화|T1-05]]** (북미 배전반 및 초고압 변압기 수주 잔고 폭증)
- **데이터센터 인프라**: **[[T1-01-데이터센터의-변화|T1-01]]** (국내외 AI 데이터센터 전력 공급 레퍼런스)

---

## 📊 관련 분석 글 및 다이제스트
```dataview
TABLE file.mtime AS "수정일", tags AS "태그"
FROM "argus" OR "outputs"
WHERE contains(file.outlinks, this.file.link) OR contains(companies, "LS ELECTRIC") OR contains(companies, "LS일렉트릭")
SORT file.mtime DESC
```
