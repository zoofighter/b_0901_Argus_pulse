---
title: "Topic: 800V DC & HVDC 전력 변환 아키텍처"
type: hub-topic
sector: "AI 데이터센터 & 전력·냉각 인프라"
related_theses:
  - "[[T2-07-800V-48V-HVDC-전력-아키텍처-혁신|T2-07]]"
  - "[[T2-05-변압기-초고압-그리드-쇼티지-장기화|T2-05]]"
  - "[[T2-01-데이터센터의-변화|T2-01]]"
tags:
  - topic
  - power
  - hvdc
  - 800v
---

# ⚡ Topic Hub: 800V DC & HVDC 전력 변환 아키텍처

> **초고밀도 AI 랙의 전력 손실을 극복하는 차세대 직류 배전 및 초고압 송전망 기술**

---

## 📌 핵심 연관 테제
- **[[T2-07-800V-48V-HVDC-전력-아키텍처-혁신|T2-07 800V·48V HVDC 전력 아키텍처 혁신]]**
- **[[T2-05-변압기-초고압-그리드-쇼티지-장기화|T2-05 변압기·초고압 그리드 쇼티지 장기화]]**
- **[[T2-01-데이터센터의-변화|T2-01 데이터센터의 변화]]**

---

## 🏢 핵심 기업
- [[Company-LS-ELECTRIC|LS ELECTRIC]]
- [[Company-HD현대일렉트릭|HD현대일렉트릭]]
- Vicor, Monolithic Power Systems (MPS), Delta Electronics, Schneider Electric

---

## 📊 관련 콘텐츠 모아보기
```dataview
TABLE file.mtime AS "수정일", tags AS "태그"
FROM "argus" OR "outputs"
WHERE contains(file.outlinks, this.file.link) OR contains(topics, "HVDC") OR contains(topics, "800V")
SORT file.mtime DESC
```
