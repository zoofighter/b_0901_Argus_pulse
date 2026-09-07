---
title: "Company: GE Vernova (GEV)"
type: hub-company
ticker: "GEV"
sector: "에너지 & 전력 인프라"
related_theses:
  - "[[T1-08-온사이트-가스터빈과-연료전지-자체발전|T1-08]]"
  - "[[T1-05-변압기-초고압-그리드-쇼티지-장기화|T1-05]]"
  - "[[T1-01-데이터센터의-변화|T1-01]]"
tags:
  - company
  - energy
  - power-grid
  - gas-turbine
---

# 🏢 Company Hub: GE Vernova (GEV)

> **전세계 가스터빈 및 전력 그리드 인프라 1위 기업**  
> AI 데이터센터 급증에 따른 유틸리티 전력망 연결 지연을 해결하는 온사이트(On-site) 가스터빈 및 초고압 변전 솔루션의 핵심 공급자입니다.

---

## 📌 핵심 투자 포인트 & 연관 테제
- **온사이트 자체 발전 가속**: **[[T1-08-온사이트-가스터빈과-연료전지-자체발전|T1-08]]** (Behind-the-Meter 가스터빈 및 복합화력 PPA)
- **변압기 및 초고압 그리드**: **[[T1-05-변압기-초고압-그리드-쇼티지-장기화|T1-05]]** (전세계 그리드 쇼티지 수혜)
- **데이터센터 전력 병목 해소**: **[[T1-01-데이터센터의-변화|T1-01]]** (GW급 AI 캠퍼스 기저부하 공급)

---

## 📊 관련 분석 글 및 다이제스트
```dataview
TABLE file.mtime AS "수정일", tags AS "태그"
FROM "argus" OR "outputs"
WHERE contains(file.outlinks, this.file.link) OR contains(companies, "GE Vernova") OR contains(companies, "GEV")
SORT file.mtime DESC
```
