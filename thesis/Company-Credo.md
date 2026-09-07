---
title: "Company: Credo"
aliases:
  - Credo
  - Credo Technology
  - 크레도
  - CRDO
type: company
ticker: "CRDO"
sector: "초고속 인터커넥트 & 액티브 전기 케이블 (AEC)"
created: 2026-09-07
related_theses:
  - "[[T3-04-800G·1.6T-광트랜시버와-AEC·LPO-초고속-인터커넥트-혁신|T3-04]]"
  - "[[T3-09-PCIe-Gen6·Gen7-전환과-초고속-신호-리타이머-병목|T3-09]]"
tags:
  - company
  - credo
  - crdo
  - aec
  - serdes
  - active-electrical-cable
  - dsp
---

# 🏢 Company Hub: Credo (크레도 테크놀로지, CRDO)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]] ➔ [[03-초고속네트워킹-시스템플랫폼.canvas|🌐 Sector 3 캔버스]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
고속 SerDes 및 **AEC(Active Electrical Cable, 액티브 전기 케이블)** 시장 1위 기업.
AI 데이터센터 랙 내부(ToR 스위치 - 서버 간)에서 고가 광케이블 대비 전력 소모와 비용을 대폭 절감하고, 일반 패시브 구리선의 물리적 거리 한계를 극복하는 고성능 AEC 및 DSP 칩셋을 마이크로소프트, 아마존 등에 공급하고 있습니다.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- **800G·1.6T 광트랜시버와 인터커넥트 혁신**: **[[T3-04-800G·1.6T-광트랜시버와-AEC·LPO-초고속-인터커넥트-혁신|T3-04]]** (랙 내부 800G AEC 케이블 수요 폭증 수혜)
- **PCIe Gen6/7 전환과 리타이머 병목**: **[[T3-09-PCIe-Gen6·Gen7-전환과-초고속-신호-리타이머-병목|T3-09]]** (초고속 SerDes 기반 신호 복원 칩 공급)

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "outputs"
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "Credo") OR contains(file.text, "크레도")
SORT file.mtime DESC
LIMIT 8
```
