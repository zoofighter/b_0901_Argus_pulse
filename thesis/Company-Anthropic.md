---
title: "Company: Anthropic"
aliases:
  - Anthropic
  - 앤트로픽
type: company
ticker: "Private"
sector: "프론티어 AI 파운데이션 모델 & AI 안전성"
created: 2026-09-06
related_theses:
  - "[[T6-05-오픈AI·앤트로픽의-5000억달러-매출-갭과-데이터센터-ROI-딜레마|T6-05]]"
  - "[[T4-02-AI-소프트웨어-레이어의-과점화|T4-02]]"
  - "[[T6-03-AI-버블-가능성|T6-03]]"
tags:
  - company
  - anthropic
  - claude
  - frontier-llm
  - ai-safety
---

# 🏢 Company Hub: Anthropic (앤트로픽)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
'헌법적 AI(Constitutional AI)'와 안전성(Safety)을 핵심으로 Claude 시리즈(Claude 3.5 Sonnet / Opus)를 개발하는 프론티어 AI 랩.
아마존(AWS Bedrock) 및 구글(GCP)의 대규모 지분 투자를 유치하며 코딩, 엔터프라이즈 에이전트, 데이터 분석 영역에서 강력한 시장 점유율을 확장하고 있습니다.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- **$5,000억 매출 갭과 ROI 딜레마**: **[[T6-05-오픈AI·앤트로픽의-5000억달러-매출-갭과-데이터센터-ROI-딜레마|T6-05]]** (AI 인프라 CapEx 정당화를 위한 기업용 매출 검증)
- **AI 소프트웨어 과점화**: **[[T4-02-AI-소프트웨어-레이어의-과점화|T4-02]]** (Claude 기반 엔터프라이즈 코딩/워크플로우 자동화)
- **AI 인프라 버블 및 과잉 리스크**: **[[T6-03-AI-버블-가능성|T6-03]]** (추론 비용 및 GPU 감가상각 부담)

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "outputs"
WHERE contains(file.outlinks, this.file.link) OR contains(keywords, "Anthropic") OR contains(file.text, "앤트로픽")
SORT file.mtime DESC
LIMIT 8
```
