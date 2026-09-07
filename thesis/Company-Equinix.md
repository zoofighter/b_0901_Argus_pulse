---
title: "Company: Equinix (EQIX)"
type: hub-company
ticker: "EQIX"
sector: "데이터센터 코로케이션 & 리츠"
related_theses:
  - "[[T3-03-전력-포화와-분산형-AI-데이터센터-코로케이션|T3-03]]"
  - "[[T1-01-데이터센터의-변화|T1-01]]"
  - "[[T6-01-금리와-데이터센터|T6-01]]"
tags:
  - company
  - datacenter
  - colocation
  - reit
---

# 🏢 Company Hub: Equinix (EQIX)

> **글로벌 1위 데이터센터 코로케이션 및 인터커넥션 리츠**  
> 전세계 260개 이상의 하이퍼스케일 및 엔터프라이즈 데이터센터를 운영하며, 전력 포화 국면에서 렌트비 상승과 분산형 AI 컴퓨트 인프라의 최대 수혜 기업입니다.

---

## 📌 핵심 투자 포인트 & 연관 테제
- **분산형 AI 코로케이션**: **[[T3-03-전력-포화와-분산형-AI-데이터센터-코로케이션|T3-03]]** (전력 포화에 따른 임대 가치 상승)
- **데이터센터 물리 인프라**: **[[T1-01-데이터센터의-변화|T1-01]]** (액체냉각 레트로핏 및 고밀도 랙 전환)
- **자본비용과 ROI**: **[[T6-01-금리와-데이터센터|T6-01]]** (금리 안정화 시 리츠 밸류에이션 리레이팅)

---

## 📊 관련 분석 글 및 다이제스트
```dataview
TABLE file.mtime AS "수정일", tags AS "태그"
FROM "argus" OR "outputs"
WHERE contains(file.outlinks, this.file.link) OR contains(companies, "Equinix") OR contains(companies, "EQIX")
SORT file.mtime DESC
```
