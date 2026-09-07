---
title: "Company: OpenAI"
aliases:
  - OpenAI
  - 오픈AI
type: company
ticker: "Private"
sector: "프론티어 AI 파운데이션 모델 & AI 플랫폼"
created: 2026-09-06
related_theses:
  - "[[T6-05-오픈AI·앤트로픽의-5000억달러-매출-갭과-데이터센터-ROI-딜레마|T6-05]]"
  - "[[T4-02-AI-소프트웨어-레이어의-과점화|T4-02]]"
  - "[[T6-03-AI-버블-가능성|T6-03]]"
tags:
  - company
  - openai
  - frontier-llm
  - ai-software
---

# 🏢 Company Hub: OpenAI (오픈AI)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
생성형 AI 슈퍼사이클을 촉발한 글로벌 1위 프론티어 파운데이션 모델(ChatGPT, GPT-4/5, o1/o3 등) 개발사이자 AI 플랫폼 리더.
마이크로소프트와의 전략적 제휴를 기반으로 Azure 인프라를 최대 규모로 소비하며, B2B 기업용 워크플로우 및 B2C 유료 구독 시장을 주도하고 있습니다.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- **$5,000억 매출 갭과 ROI 딜레마**: **[[T6-05-오픈AI·앤트로픽의-5000억달러-매출-갭과-데이터센터-ROI-딜레마|T6-05]]** (AI 데이터센터 인프라 소화를 위한 매출 허들 검증)
- **AI 소프트웨어 과점화**: **[[T4-02-AI-소프트웨어-레이어의-과점화|T4-02]]** (기업용 LLM API 과점을 통한 레거시 SaaS 시장 잠식)
- **AI 인프라 버블 및 CapEx 과잉 리스크**: **[[T6-03-AI-버블-가능성|T6-03]]** (수익화 지연 시 빅테크 인프라 투자 조정)

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "outputs"
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "OpenAI") OR contains(file.text, "오픈AI")
SORT file.mtime DESC
LIMIT 8
```
