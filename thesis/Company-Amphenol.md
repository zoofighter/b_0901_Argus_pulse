---
title: "Company: Amphenol"
aliases:
  - Amphenol
  - 암페놀
  - APH
type: company
ticker: "APH"
sector: "고속 커넥터 & 구리선 인터커넥트 백플레인"
created: 2026-09-07
related_theses:
  - "[[T3-10-NVLink-Switch-랙스케일-패브릭과-대규모-구리-백플레인|T3-10]]"
  - "[[T3-04-800G·1.6T-광트랜시버와-AEC·LPO-초고속-인터커넥트-혁신|T3-04]]"
tags:
  - company
  - amphenol
  - aph
  - copper-backplane
  - connectors
  - nvlink-switch
  - nvlink72
---

# 🏢 Company Hub: Amphenol (암페놀, APH)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]] ➔ [[03-초고속네트워킹-시스템플랫폼.canvas|🌐 Sector 3 캔버스]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
글로벌 1위 고속 커넥터 및 케이블링 시스템 전문 기업.
엔비디아 **GB200 NVL72 랙스케일 시스템**의 핵심 부품인 **NVLink 구리선 카트리지 백플레인(OverPass 케이블 및 5,000+ 가닥 커넥터)**을 독점 공급하며, AI 서버 랙 내부 고속 구리 통신의 핵심 수혜자로 자리잡았습니다.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- **NVLink 랙스케일 패브릭과 대규모 구리 백플레인**: **[[T3-10-NVLink-Switch-랙스케일-패브릭과-대규모-구리-백플레인|T3-10]]** (GB200 NVL72 랙당 수천 달러 규모 커넥터 및 구리 케이블링 독점)
- **800G·1.6T 광트랜시버와 인터커넥트 혁신**: **[[T3-04-800G·1.6T-광트랜시버와-AEC·LPO-초고속-인터커넥트-혁신|T3-04]]** (고속 케이블 어셈블리 공급)

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "outputs"
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "Amphenol") OR contains(file.text, "암페놀")
SORT file.mtime DESC
LIMIT 8
```
