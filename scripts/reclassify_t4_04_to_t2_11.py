# -*- coding: utf-8 -*-
import os, glob, json

T2_11_CONTENT = """---
confidence: 35
direction: bearish
hypothesis: 추론 시대 진입으로 TPU·커스텀ASIC이 NVIDIA GPU를 대체하며 GPU 수요 증가세가 꺾인다
id: T2-11
keywords:
- TPU
- CUDA
- JAX
- FLOPS
- 추론최적화
- 커스텀ASIC
- 학습vs추론
- CUDAwall
- TPUv6
last_checked: 2026-09-06T21:05
last_ranked: 2026-09-07T19:05
milestone: 구글 TPU 외부 판매 개시 또는 NVIDIA 실적에서 추론용 GPU 비중 공개
momentum: 87.0
news_count: 1
priority: 4
rank: 25
related_companies:
- NVIDIA
- Google
- AMD
- Cerebras
- Groq
- Intel
related_theses:
- T5-05
- T2-07
- T2-08
status: active
time_horizon: 2026~2027
title: TPU 증가와 GPU 수요 둔화
aliases:
- T2-11
- T2-11 TPU 증가와 GPU 수요 둔화
- T4-04
- T4-04 TPU 증가와 GPU 수요 둔화
- T6-08
- T6-08 TPU 증가와 GPU 수요 둔화
- T-06
- T-06 TPU 증가와 GPU 수요 둔화
- TPU 증가와 GPU 수요 둔화
sector: AI 컴퓨트 & 차세대 반도체
sector_id: T2
thesis_nature: contrarian
stack_layer: L1
stack_name: L1 (칩/패키징)
geography:
- US
- TW
related_vs:
- Vs-GPU-vs-TPU-ASIC
old_id: T-06
previous_id: SC-02
---

# T2-11 TPU 증가와 GPU 수요 둔화

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]] ➔ [[00-Argus-Master-MOC#1-💾-ai-컴퓨트--차세대-반도체-compute--silicon|AI 컴퓨트 & 반도체]]

> 🏷️ **교차 분석 메타데이터**:
> - **성격**: `🛡️ 역발상/헷지 (Contrarian)` | **스택**: `L1 (칩/패키징)` | **시계**: `2026~2027`
> - **공급망 권역**: `US`, `TW` | **핵심 대결 구도**: [[Vs-GPU-vs-TPU-ASIC|GPU-vs-TPU-ASIC]]

---

## 🎯 핵심 가설
추론 시대 진입으로 TPU·커스텀ASIC이 NVIDIA GPU를 대체하며 GPU 수요 증가세가 꺾인다

---

## 🔗 테제 네트워크 (상호 연관 가설)

```mermaid
graph LR
    P_T_01["[[T1-01-데이터센터의-변화|T1-01 데이터센터의 변화]]"] --> T_T_06["★ [[T2-11-TPU-증가와-GPU-수요-둔화|T2-11 TPU 증가와 GPU 수요 둔화]]"]
    P_T_05["[[T6-01-금리와-데이터센터|T6-01 금리와 데이터센터]]"] --> T_T_06["★ [[T2-11-TPU-증가와-GPU-수요-둔화|T2-11 TPU 증가와 GPU 수요 둔화]]"]
    T_T_06["★ [[T2-11-TPU-증가와-GPU-수요-둔화|T2-11 TPU 증가와 GPU 수요 둔화]]"] --> D_T_15["[[T2-07-AI-추론-시장-폭발과-LPU-ASIC-분화|T2-07 AI 추론 시장 폭발과 LPU·ASIC 분화]]"]
    T_T_06["★ [[T2-11-TPU-증가와-GPU-수요-둔화|T2-11 TPU 증가와 GPU 수요 둔화]]"] --> D_T_24["[[T2-08-빅테크-커스텀-ASIC-증가와-DSP-생태계|T2-08 빅테크 커스텀 ASIC 증가와 DSP 생태계]]"]
    T_T_06["★ [[T2-11-TPU-증가와-GPU-수요-둔화|T2-11 TPU 증가와 GPU 수요 둔화]]"] <.-> S_T_08["[[T6-09-엔비디아와-네오클라우드|T6-09 엔비디아와 네오클라우드]]"]
    T_T_06["★ [[T2-11-TPU-증가와-GPU-수요-둔화|T2-11 TPU 증가와 GPU 수요 둔화]]"] <.-> S_T_31["[[T4-02-AI-소프트웨어-레이어의-과점화|T4-02 AI 소프트웨어 레이어의 과점화]]"]
```

- 🔼 **선행 가설 (배경 요인 & 상위 인프라)**:
  - [[T1-01-데이터센터의-변화|T1-01 데이터센터의 변화]] — GPU 조달 비용 급증
  - [[T6-01-금리와-데이터센터|T6-01 금리와 데이터센터]] — CAPEX 절감 압박
- ➡️ **동반 및 대체·경쟁 가설**:
  - [[T6-09-엔비디아와-네오클라우드|T6-09 엔비디아와 네오클라우드]] — 엔비디아 락인 vs 자체 칩
  - [[T4-02-AI-소프트웨어-레이어의-과점화|T4-02 AI 소프트웨어 레이어의 과점화]] — 소프트웨어 해자 결합
- 🔽 **파생 및 후행 병목 가설**:
  - [[T2-07-AI-추론-시장-폭발과-LPU-ASIC-분화|T2-07 AI 추론 시장 폭발과 LPU·ASIC 분화]] — 추론용 특화칩 분화
  - [[T2-08-빅테크-커스텀-ASIC-증가와-DSP-생태계|T2-08 빅테크 커스텀 ASIC 증가와 DSP 생태계]] — 디자인하우스 생태계 호황

---

## 🏢 연관 기업 & 핵심 기술 허브
- **핵심 기업**: [[Company-NVIDIA|NVIDIA]], [[Company-Google|Google]], [[Company-AMD|AMD]], [[Company-Cerebras|Cerebras]], [[Company-Groq|Groq]], [[Company-Intel|Intel]]
- **핵심 기술/토픽**: [[Topic-ASIC|ASIC]], [[Topic-2nm-GAA|2nm-GAA]]

---

## 📈 지지 근거


---

## 📉 반박 근거
- 2026-09-05: 서버용 CPU/GPU에 탑재되는 고부가 기판의 수급이 타이트할 정도로 GPU 수요가 여전히 양호하다는 분석이 제시되었습니다.
- 2026-09-04: 증권사 리포트들이 GPU·HBM을 생성형AI 핵심 가속기로 규정하고 서버용 CPU/GPU용 고부가 패키지 기판(FC-BGA) 수급이 타이트할 정도로 수요가 양호하다고 명시해 GPU 수요 둔화 전제와 상충함
- 2026-09-04: 증권사 리포트들이 GPU·HBM을 생성형AI 가속기의 핵심 요소로 재확인하고 서버용 CPU/GPU용 고부가 기판 수요/공급이 타이트할 정도로 수요가 양호하다고 언급
- 2026-09-04: 증권사 리포트가 AI 가속기의 핵심 요소를 GPU·HBM으로 규정하고 서버용 CPU/GPU용 FC-BGA 등 고부가 기판의 수급 타이트 및 수요 양호를 언급하여 GPU 수요가 여전히 견조함을 시사함
- 2026-09-06: 증권사 리포트들이 AI 가속기 핵심을 GPU·HBM으로 규정하고 데이터센터 비용의 대부분이 GPU·CPU에 집중되며 서버용 CPU/GPU 기판 수급이 타이트할 정도로 수요가 양호하다고 언급해 GPU 수요 둔화 가설을 반박함

---

## 📑 관련 산출물 (자동 집계)

### 🤖 Dataview 실시간 역방향 링크
```dataview
TABLE file.mtime AS "작성일", angle AS "관점", tags AS "태그"
FROM "argus" OR "output" OR ""
WHERE contains(thesis, "T2-11") OR contains(thesis, "T4-04") OR contains(file.outlinks, this.file.link)
SORT file.mtime DESC
LIMIT 7
```

### 📌 수동 링크 아카이브


---

## 📝 분석가 메모
"""

with open('thesis/T2-11-TPU-증가와-GPU-수요-둔화.md', 'w', encoding='utf-8') as f:
    f.write(T2_11_CONTENT.strip() + '\n')

old_file = 'thesis/T4-04-TPU-증가와-GPU-수요-둔화.md'
if os.path.exists(old_file):
    os.remove(old_file)

print("T2-11 written successfully.")
