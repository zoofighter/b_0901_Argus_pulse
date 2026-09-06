---
id: TC-01
title: "자유전자레이저(FEL) 기반 극자외선 노광원 상용화"
sector: "AI 컴퓨트 & 차세대 반도체 (후보)"
sector_candidate: "T1"
stage: "candidate"
incubation_score: 84
first_detected: "2026-09-06"
observation_days: 3
news_velocity_zscore: 3.2
keywords:
  - "자유전자레이저"
  - "FEL"
  - "EUV 광원"
  - "펠리클"
  - "High-NA EUV"
candidate_companies:
  - "ASML"
  - "삼성전자"
  - "포항가속기연구소"
promotion_triggers:
  - "파운드리/연구소 간 1kW급 FEL 가속기 실증 계약 공시"
  - "기존 LPP 광원 대비 소비전력 50% 절감 데이터 발표"
aliases:
  - TC-01
  - TC-01 자유전자레이저(FEL) 기반 극자외선 노광원 상용화
  - 자유전자레이저 EUV 광원
---

# 🧭 TC-01 자유전자레이저(FEL) 기반 극자외선 노광원 상용화

> **신규 테마 인큐베이션 (Stage: Candidate / Score: 84점)**  
> 2nm 이하 초미세 공정에서 기존 주석 플라즈마(LPP) EUV 광원의 출력 한계와 막대한 전력 소모를 극복할 차세대 광원으로 급부상 중인 후보 가설입니다.

---

## 1. 신규 테마 발굴 배경 (Why Now)
- **발굴 계기**: 최근 3일간 41개 기존 테제와 매칭되지 않던 글로벌 반도체 기술 외신에서 `자유전자레이저(FEL)` 및 `출력 1kW 이상 EUV 광원` 관련 기사가 5건 이상 급증(Z-Score 3.2).
- **기술적 병목**: 기존 High-NA EUV는 2나노 이하 패터닝 시 광량 부족으로 스캔 속도가 느려져 웨이퍼 생산 단가(Cost per Wafer)가 급등함.

---

## 2. 기존 정식 테제와의 인과관계 가설 맵

```mermaid
flowchart LR
    P_2nm["[[T1-08-파운드리-2nm-공정과-GAA-격돌|T1-08 2nm 파운드리]]"] -->|미세 패턴 광량 부족| T_Main["★ [[TC-01-자유전자레이저-FEL-노광원|TC-01 FEL 광원 상용화]]"]
    T_Main -->|차세대 EUV 로드맵| D_Mem["[[T1-01-메모리-산업의-변화|T1-01 1c/1d D램 미세화]]"]
```

---

## 3. 정식 테제 승격 체크리스트 (Promotion Checklist)
- [x] **약한 신호 감지**: 3개 이상 외신에서 독립 보도 확인 (2026-09-06 완료)
- [ ] **후속 뉴스 지속성**: 향후 14일간 주간 3건 이상 관련 뉴스 유입 유지
- [ ] **산업 촉매(Catalyst)**: ASML 또는 빅테크의 FEL 파일럿 라인 투자 공시 확인
- [ ] **반증 리스크 점검**: 가속기 설치 부지 및 장비 단가 타당성 확인

---

## 4. 관련 뉴스 및 수집 피드
```dataview
TABLE file.mtime AS "수정일", tags AS "태그"
FROM "argus" OR "outputs"
WHERE contains(topics, "FEL") OR contains(file.outlinks, this.file.link)
SORT file.mtime DESC
```
