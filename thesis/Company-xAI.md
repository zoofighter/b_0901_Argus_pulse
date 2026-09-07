---
id: Company-xAI
name: "xAI"
korean_name: "xAI (엑스에이아이)"
ticker: "Private"
type: company
sector: "프론티어 AI 파운데이션 모델 & 슈퍼컴퓨팅"
created: "2026-09-07"
related_theses:
  - "[[T4-07-xAI-그록과-실시간-데이터-파이어호스-인텔리전스|T4-07]]"
  - "[[T5-05-End-to-End-AI-자율주행과-로보택시|T5-05]]"
  - "[[T5-06-휴머노이드-로봇과-액추에이터-공급망|T5-06]]"
  - "[[T1-08-온사이트-가스터빈과-연료전지-자체발전|T1-08]]"
tags:
  - company
  - xai
  - grok
  - colossus
  - elon-musk
  - frontier-llm
---

# 🏢 Company Hub: xAI (엑스에이아이)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]] ➔ [[04-파운데이션모델-엔터프라이즈SW.canvas|💻 Sector 4 캔버스]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
일론 머스크가 2023년 설립한 프론티어 AI 기업으로, X(구 트위터)의 실시간 데이터와 멤피스 'Colossus(20만 GPU 슈퍼클러스터)'를 기반으로 Grok 3 등 최고 성능의 자율 추론 모델을 개발하고 있습니다. 테슬라(FSD, Optimus), 스페이스X와의 긴밀한 결합을 통해 디지털 및 피지컬 AI 전반을 아우르는 차세대 인텔리전스 허브 역할을 수행합니다.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- **xAI 그록과 실시간 파이어호스**: **[[T4-07-xAI-그록과-실시간-데이터-파이어호스-인텔리전스|T4-07]]** (X 실시간 데이터와 Colossus 슈퍼클러스터 결합)
- **E2E 자율주행과 로보택시**: **[[T5-05-End-to-End-AI-자율주행과-로보택시|T5-05]]** (Tesla FSD VLA 백본 연계)
- **휴머노이드 로봇 생태계**: **[[T5-06-휴머노이드-로봇과-액추에이터-공급망|T5-06]]** (Optimus 인공지능 두뇌 결합)
- **온사이트 가스터빈 자체발전**: **[[T1-08-온사이트-가스터빈과-연료전지-자체발전|T1-08]]** (멤피스 데이터센터 독립 전력 인프라 구축)

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "output" OR ""
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "xAI") OR contains(file.text, "Grok")
SORT file.mtime DESC
LIMIT 8
```
