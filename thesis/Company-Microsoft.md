---
aliases:
  - Microsoft
  - 마이크로소프트
  - MSFT
type: company
ticker: "MSFT"
sector: 클라우드 / 엔터프라이즈 AI
created: 2026-09-06
---

# 🏢 Microsoft (MSFT)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
Azure 클라우드와 OpenAI 협력, Copilot 플랫폼을 통해 전 세계 엔터프라이즈 AI 소프트웨어 시장을 과점.

---

## 🔗 연관 투자 가설 (Thesis Mapping)
- [[T-05-금리와-데이터센터|T-05]]
- [[T-21-AI-PC-보급-확대와-Arm-기반-윈도우-생태계|T-21]]
- [[T-31-AI-소프트웨어-레이어의-과점화|T-31]]
- [[T-37-AI-버블-가능성|T-37]]

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "output"
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "Microsoft")
SORT file.mtime DESC
LIMIT 8
```
