---
title: "Company: Fabrinet"
aliases:
  - Fabrinet
  - 패브리넷
  - FN
type: company
ticker: "FN"
sector: "첨단 광학 제조 파운드리 & 광트랜시버 패키징"
created: 2026-09-07
related_theses:
  - "[[T3-04-800G·1.6T-광트랜시버와-AEC·LPO-초고속-인터커넥트-혁신|T3-04]]"
  - "[[T3-01-실리콘-포토닉스와-CPO의-상용화|T3-01]]"
tags:
  - company
  - fabrinet
  - fn
  - optical-packaging
  - transceiver-foundry
  - nvidia-supplier
---

# 🏢 Company Hub: Fabrinet (패브리넷, FN)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]] ➔ [[03-초고속네트워킹-시스템플랫폼.canvas|🌐 Sector 3 캔버스]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
글로벌 1위 첨단 정밀 광학 및 전자제품 외주 제조(EMS/파운드리) 기업.
엔비디아의 인피니밴드 및 이더넷용 **800G/1.6T 광트랜시버 제조를 독점 위탁 생산**하고 있으며, Cisco, Lumentum 등의 고난도 광패키징을 전담하고 있습니다.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- **800G·1.6T 광트랜시버와 인터커넥트 혁신**: **[[T3-04-800G·1.6T-광트랜시버와-AEC·LPO-초고속-인터커넥트-혁신|T3-04]]** (엔비디아 광트랜시버 독점 양산 파트너)
- **실리콘 포토닉스와 CPO의 상용화**: **[[T3-01-실리콘-포토닉스와-CPO의-상용화|T3-01]]** (광엔진 패키징 조립)

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "outputs"
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "Fabrinet") OR contains(file.text, "패브리넷")
SORT file.mtime DESC
LIMIT 8
```
