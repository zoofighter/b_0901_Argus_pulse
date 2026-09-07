---
title: "Company: DeepSeek"
aliases:
  - DeepSeek
  - 딥시크
  - 深度求索
type: company
ticker: "Private"
sector: "프론티어 AI 파운데이션 모델 & 알고리즘 혁신"
created: 2026-09-07
related_theses:
  - "[[T4-08-중국-AI-모델-급부상과-오픈AI·앤트로픽-과점-위협|T4-08]]"
  - "[[T4-01-오픈소스-모델-고도화와-온프레미스-사설-AI|T4-01]]"
  - "[[T4-03-추론-시간-연산과-시스템2-추론-모델의-부상|T4-03]]"
  - "[[T6-05-오픈AI·앤트로픽의-5000억달러-매출-갭과-데이터센터-ROI-딜레마|T6-05]]"
tags:
  - company
  - deepseek
  - chinese-ai
  - mla
  - moe
  - reasoning-model
  - open-source-llm
---

# 🏢 Company Hub: DeepSeek (딥시크, 深度求索)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]] ➔ [[04-파운데이션모델-엔터프라이즈SW.canvas|💻 Sector 4 캔버스]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
중국 항저우 기반의 프론티어 AI 리서치 기업(High-Flyer 퀀트 펀드 산하).
독자적인 **MLA(Multi-Head Latent Attention)** 및 **DeepSeekMoE** 아키텍처를 기반으로, 미국 대비 1/10 미만의 컴퓨트 비용으로 GPT-4o 및 o1/o3급 고성능 오픈 가중치 모델(DeepSeek-V3, DeepSeek-R1)을 개발하며 글로벌 AI 시장에 극단적인 가격 파괴를 주도하고 있습니다.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- **중국 AI 급부상과 미국 LLM 과점 위협**: **[[T4-08-중국-AI-모델-급부상과-오픈AI·앤트로픽-과점-위협|T4-08]]** (1/20 가격 파괴와 오픈소스 확산으로 OpenAI/Anthropic 마진 압박)
- **추론 시간 연산과 시스템 2 모델**: **[[T4-03-추론-시간-연산과-시스템2-추론-모델의-부상|T4-03]]** (DeepSeek-R1 추론 모델을 통한 시스템 2 추론 오픈소스화)
- **오픈소스 고도화와 사설 AI**: **[[T4-01-오픈소스-모델-고도화와-온프레미스-사설-AI|T4-01]]** (온프레미스 및 프라이빗 클라우드 시장 장악)
- **$5,000억 매출 갭과 ROI 딜레마**: **[[T6-05-오픈AI·앤트로픽의-5000억달러-매출-갭과-데이터센터-ROI-딜레마|T6-05]]** (토큰 단가 디플레이션으로 인한 인프라 투자 회수 난항 가중)

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "outputs"
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "DeepSeek") OR contains(file.text, "딥시크")
SORT file.mtime DESC
LIMIT 8
```
