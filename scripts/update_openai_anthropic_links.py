# -*- coding: utf-8 -*-
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
THESIS_DIR = ROOT_DIR / "thesis"

# 1. Update Company-OpenAI.md
openai_content = """---
title: "Company: OpenAI"
aliases:
  - OpenAI
  - 오픈AI
type: company
ticker: "Private"
sector: "프론티어 AI 파운데이션 모델 & AI 플랫폼"
created: 2026-09-06
related_theses:
  - "[[T4-03-추론-시간-연산과-시스템2-추론-모델의-부상|T4-03]]"
  - "[[T4-04-자율형-에이전트와-컴퓨터-제어-엔터프라이즈-침투|T4-04]]"
  - "[[T4-05-프론티어-LLM-멀티모달-네이티브화와-실시간-옴니-인텔리전스|T4-05]]"
  - "[[T4-02-AI-소프트웨어-레이어의-과점화|T4-02]]"
  - "[[T6-05-오픈AI·앤트로픽의-5000억달러-매출-갭과-데이터센터-ROI-딜레마|T6-05]]"
  - "[[T6-03-AI-버블-가능성|T6-03]]"
tags:
  - company
  - openai
  - frontier-llm
  - test-time-compute
  - autonomous-agents
  - omni-multimodal
---

# 🏢 Company Hub: OpenAI (오픈AI)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]] ➔ [[04-파운데이션모델-엔터프라이즈SW.canvas|💻 Sector 4 캔버스]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
생성형 AI 슈퍼사이클을 촉발한 글로벌 1위 프론티어 파운데이션 모델(ChatGPT, GPT-4o, o1/o3 추론 모델, Operator 자율 에이전트 등) 개발사이자 AI 플랫폼 리더.
마이크로소프트와의 전략적 제휴를 기반으로 Azure 인프라를 최대 규모로 소비하며, B2B 기업용 워크플로우 및 B2C 유료 구독 시장을 주도하고 있습니다.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- **추론 시간 연산과 시스템 2 모델**: **[[T4-03-추론-시간-연산과-시스템2-추론-모델의-부상|T4-03]]** (o1/o3 강화학습 추론 스케일링을 통한 문제해결 혁신)
- **자율형 에이전트 & Operator**: **[[T4-04-자율형-에이전트와-컴퓨터-제어-엔터프라이즈-침투|T4-04]]** (웹/스크린 조작 자율 에이전트를 통한 엔터프라이즈 업무 자동화)
- **멀티모달 네이티브 옴니 인텔리전스**: **[[T4-05-프론티어-LLM-멀티모달-네이티브화와-실시간-옴니-인텔리전스|T4-05]]** (GPT-4o 실시간 음성/비전 인터페이스 혁신)
- **AI 소프트웨어 과점화**: **[[T4-02-AI-소프트웨어-레이어의-과점화|T4-02]]** (기업용 LLM API 과점을 통한 레거시 SaaS 시장 잠식)
- **$5,000억 매출 갭과 ROI 딜레마**: **[[T6-05-오픈AI·앤트로픽의-5000억달러-매출-갭과-데이터센터-ROI-딜레마|T6-05]]** (AI 데이터센터 인프라 소화를 위한 매출 허들 검증)
- **AI 인프라 버블 리스크**: **[[T6-03-AI-버블-가능성|T6-03]]** (수익화 지연 시 빅테크 인프라 투자 조정)

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "outputs"
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "OpenAI") OR contains(file.text, "오픈AI")
SORT file.mtime DESC
LIMIT 8
```
"""
(THESIS_DIR / "Company-OpenAI.md").write_text(openai_content.strip() + "\n", encoding="utf-8")
print("Updated Company-OpenAI.md")

# 2. Update Company-Anthropic.md
anthropic_content = """---
title: "Company: Anthropic"
aliases:
  - Anthropic
  - 앤트로픽
type: company
ticker: "Private"
sector: "프론티어 AI 파운데이션 모델 & AI 안전성"
created: 2026-09-06
related_theses:
  - "[[T4-04-자율형-에이전트와-컴퓨터-제어-엔터프라이즈-침투|T4-04]]"
  - "[[T4-03-추론-시간-연산과-시스템2-추론-모델의-부상|T4-03]]"
  - "[[T4-05-프론티어-LLM-멀티모달-네이티브화와-실시간-옴니-인텔리전스|T4-05]]"
  - "[[T4-02-AI-소프트웨어-레이어의-과점화|T4-02]]"
  - "[[T6-05-오픈AI·앤트로픽의-5000억달러-매출-갭과-데이터센터-ROI-딜레마|T6-05]]"
  - "[[T6-03-AI-버블-가능성|T6-03]]"
tags:
  - company
  - anthropic
  - claude
  - computer-use
  - frontier-llm
  - ai-safety
---

# 🏢 Company Hub: Anthropic (앤트로픽)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]] ➔ [[04-파운데이션모델-엔터프라이즈SW.canvas|💻 Sector 4 캔버스]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
'헌법적 AI(Constitutional AI)'와 안전성(Safety)을 핵심으로 Claude 3.5 Sonnet / Opus 및 업계 최초의 'Computer Use API'를 출시한 프론티어 AI 랩.
아마존(AWS Bedrock) 및 구글(GCP)의 대규모 지분 투자를 유치하며 코딩, 엔터프라이즈 자율 에이전트, 복합 데이터 분석 영역에서 가장 강력한 개발자 지지도를 확보하고 있습니다.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- **자율형 에이전트 & Computer Use**: **[[T4-04-자율형-에이전트와-컴퓨터-제어-엔터프라이즈-침투|T4-04]]** (Claude 3.5 Computer Use API를 통한 GUI 직접 제어 및 RPA 대체)
- **추론 시간 연산과 시스템 2 모델**: **[[T4-03-추론-시간-연산과-시스템2-추론-모델의-부상|T4-03]]** (확장 사고 및 다단계 코딩/추론 가속)
- **멀티모달 네이티브 옴니 인텔리전스**: **[[T4-05-프론티어-LLM-멀티모달-네이티브화와-실시간-옴니-인텔리전스|T4-05]]** (시각·문서 분석 및 멀티모달 오케스트레이션)
- **AI 소프트웨어 과점화**: **[[T4-02-AI-소프트웨어-레이어의-과점화|T4-02]]** (Claude 기반 엔터프라이즈 코딩/워크플로우 자동화)
- **$5,000억 매출 갭과 ROI 딜레마**: **[[T6-05-오픈AI·앤트로픽의-5000억달러-매출-갭과-데이터센터-ROI-딜레마|T6-05]]** (AI 인프라 CapEx 정당화를 위한 기업용 매출 검증)
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
"""
(THESIS_DIR / "Company-Anthropic.md").write_text(anthropic_content.strip() + "\n", encoding="utf-8")
print("Updated Company-Anthropic.md")

# 3. Update T2-07 downstream link
t2_07_path = THESIS_DIR / "T2-07-AI-추론-시장-폭발과-LPU-ASIC-분화.md"
if t2_07_path.exists():
    t = t2_07_path.read_text(encoding="utf-8")
    t = t.replace("T4-03-바이오AI와-신약개발-가속", "T4-03-추론-시간-연산과-시스템2-추론-모델의-부상")
    t = t.replace("T4-03 바이오 AI와 신약 개발 가속", "T4-03 추론 시간 연산과 시스템 2 추론 모델의 부상")
    t = t.replace("도메인 특화 추론 가속", "테스트 타임 연산 및 CoT 추론 가속")
    t2_07_path.write_text(t, encoding="utf-8")
    print("Updated T2-07 link.")

print("All company and thesis links updated.")
