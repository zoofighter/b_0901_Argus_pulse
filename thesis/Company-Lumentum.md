---
title: "Company: Lumentum"
aliases:
  - Lumentum
  - 루멘텀
  - LITE
type: company
ticker: "LITE"
sector: "광통신 부품 & 레이저 광학계"
created: 2026-09-07
related_theses:
  - "[[T3-04-800G·1.6T-광트랜시버와-AEC·LPO-초고속-인터커넥트-혁신|T3-04]]"
  - "[[T3-01-실리콘-포토닉스와-CPO의-상용화|T3-01]]"
  - "[[T3-07-데이터센터-간-초장거리-인터커넥트-DCI|T3-07]]"
tags:
  - company
  - lumentum
  - optical-transceiver
  - emls
  - cw-laser
  - cpo
---

# 🏢 Company Hub: Lumentum (루멘텀, LITE)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]] ➔ [[03-초고속네트워킹-시스템플랫폼.canvas|🌐 Sector 3 캔버스]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
글로벌 최고 수준의 고속 광통신 광원(EML, CW 레이저) 및 광트랜시버 부품 전문 기업.
AI 데이터센터의 800G 및 1.6T 고속 광모듈에 탑재되는 200G/Lane급 EML 레이저 칩과 실리콘 포토닉스용 고출력 CW(Continuous Wave) 레이저 공급을 독점하고 있습니다.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- **800G·1.6T 광트랜시버와 인터커넥트 혁신**: **[[T3-04-800G·1.6T-광트랜시버와-AEC·LPO-초고속-인터커넥트-혁신|T3-04]]** (1.6T 광모듈용 200G EML 레이저 칩 쇼티지 수혜)
- **실리콘 포토닉스와 CPO의 상용화**: **[[T3-01-실리콘-포토닉스와-CPO의-상용화|T3-01]]** (외장형 광원 ELS / CW Laser 공급)
- **데이터센터 간 초장거리 DCI**: **[[T3-07-데이터센터-간-초장거리-인터커넥트-DCI|T3-07]]** (코히런트 광모듈용 고출력 파장 가변 레이저 공급)

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "outputs"
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "Lumentum") OR contains(file.text, "루멘텀")
SORT file.mtime DESC
LIMIT 8
```
