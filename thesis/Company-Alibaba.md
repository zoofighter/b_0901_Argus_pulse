---
title: "Company: Alibaba"
aliases:
  - Alibaba
  - 알리바바
  - BABA
  - Qwen
  - 통이첸원
type: company
ticker: "BABA"
sector: "클라우드 컴퓨팅 & 프론티어 파운데이션 모델 (Qwen)"
created: 2026-09-07
related_theses:
  - "[[T4-08-중국-AI-모델-급부상과-오픈AI·앤트로픽-과점-위협|T4-08]]"
  - "[[T4-01-오픈소스-모델-고도화와-온프레미스-사설-AI|T4-01]]"
  - "[[T6-06-소버린-AI와-국가-단위-컴퓨트-인프라|T6-06]]"
tags:
  - company
  - alibaba
  - qwen
  - cloud
  - chinese-ai
  - open-source-llm
---

# 🏢 Company Hub: Alibaba (알리바바 그룹 / Qwen, BABA)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]] ➔ [[04-파운데이션모델-엔터프라이즈SW.canvas|💻 Sector 4 캔버스]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
중국 최대의 전자상거래 및 클라우드 서비스 기업.
자체 개발한 **Qwen(통이첸원, 通义千问)** 시리즈(Qwen 2.5, Qwen-Max, Qwen-Coder)를 오픈소스로 전면 개방하며, 코딩·수학·다국어 벤치마크에서 글로벌 최상위권 성적을 기록. 알리바바 클라우드 인프라와 결합하여 아시아-태평양 및 글로벌 엔터프라이즈 AI 시장을 적극 공략하고 있습니다.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- **중국 AI 급부상과 미국 LLM 과점 위협**: **[[T4-08-중국-AI-모델-급부상과-오픈AI·앤트로픽-과점-위협|T4-08]]** (Qwen 오픈소스 생태계 확산 및 초저가 API 공세)
- **오픈소스 모델 고도화와 사설 AI**: **[[T4-01-오픈소스-모델-고도화와-온프레미스-사설-AI|T4-01]]** (글로벌 오픈소스 생태계 내 Llama와의 양강 체제 형성)
- **소버린 AI와 국가 컴퓨트 인프라**: **[[T6-06-소버린-AI와-국가-단위-컴퓨트-인프라|T6-06]]** (중화권 및 동남아 소버린 클라우드 AI 구축 주도)

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "outputs"
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "Alibaba") OR contains(file.text, "알리바바") OR contains(file.text, "Qwen")
SORT file.mtime DESC
LIMIT 8
```
