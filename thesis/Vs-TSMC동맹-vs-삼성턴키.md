---
aliases:
  - TSMC 연합 vs 삼성 턴키
  - SK-TSMC vs 삼성
  - 분리형 vs 수직계열화
type: vs_hub
category: 제로섬 대결 & 트레이드오프
created: 2026-09-06
---

# ⚔️ TSMC 동맹 (SK하이닉스-TSMC) vs 삼성전자 턴키 (원팀)

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]] ➔ [[00-Argus-Master-MOC#⚔️-핵심-기술--진영-대결-구도-versus-hubs|대결 허브]]

---

## 📌 대결 구도 개요 및 핵심 쟁점
SK하이닉스(메모리)-TSMC(선단 로직 & CoWoS)-엔비디아로 이어지는 분리형 삼각편대와, 메모리+파운드리+어드밴스드 패키징을 일괄 제공하는 삼성전자의 CUBE 턴키 모델 간의 서플라이체인 표준 경쟁.

> ⚡ **핵심 충돌 지점**:  
> **검증된 CoWoS 생태계와 락인 vs 일괄 공급에 따른 리드타임 단축 및 단가 우위**

---

## 🔗 관련 투자 테제군 (Theses Network)
- [[T-02-메모리-산업의-변화|T-02]]
- [[T-10-첨단-패키징과-CoWoS의-병목|T-10]]
- [[T-16-파운드리-2nm-공정과-GAA-격돌|T-16]]

---

## 🏢 대결 진영별 핵심 기업 (Players)
- **주요 플레이어**: [[Company-SK하이닉스|SK하이닉스]], [[Company-TSMC|TSMC]], [[Company-삼성전자|삼성전자]], [[Company-NVIDIA|NVIDIA]], [[Company-한미반도체|한미반도체]]

---

## 📑 관련 분석 리포트 및 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", title AS "제목", tags AS "태그"
FROM "argus" OR "output"
WHERE contains(file.text, "TSMC 연합 vs 삼성 턴키") OR contains(file.outlinks, this.file.link)
SORT file.mtime DESC
LIMIT 8
```
