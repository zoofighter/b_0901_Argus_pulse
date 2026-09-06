"""
scripts/fix_missing_nodes.py — 누락된 기업 허브 노드 일괄 생성 및 린터 오류 자동 치료
"""

import os
from pathlib import Path
import unicodedata

ROOT_DIR = Path(__file__).parent.parent
THESIS_DIR = ROOT_DIR / "thesis"

# 주요 누락 기업 리스트 정의
COMPANY_DEFS = {
    "Micron": ("마이크론 테크놀로지", "MU", "미국 3대 메모리 반도체 기업. HBM3E 8단/12단 엔비디아 납품 및 1γ DRAM 공정 경쟁."),
    "Google": ("구글 / 알파벳", "GOOGL", "TPU v5/v6 기반 자체 AI 가속기 생태계 구축, 제미나이(Gemini) 파운데이션 모델 선도."),
    "Amazon": ("아마존 / AWS", "AMZN", "Trainium / Inferentia 자체 AI 칩 개발, 세계 최대 클라우드 IaaS 점유율."),
    "AMD": ("어드밴스드 마이크로 디바이시스", "AMD", "MI300X/MI325X/MI350X 가속기 및 ROCm 소프트웨어 생태계로 엔비디아 대항."),
    "Intel": ("인텔", "INTC", "Gaudi 3 AI 가속기, 18A 공정 파운드리 재건, x86 및 AI PC 생태계 주도."),
    "Eaton": ("이튼", "ETN", "글로벌 전력 관리 및 배전 솔루션 선두 기업. 데이터센터 배전반 및 무정전 전원장치(UPS)."),
    "현대차": ("현대자동차", "005380.KS", "보스턴 다이내믹스 인수, 로보틱스 및 SDV 자율주행 전환 가속화."),
    "삼성SDI": ("삼성SDI", "006400.KS", "전고체 배터리(ASB) 2027년 양산 선도 및 프리미엄 에너지저장장치(ESS) 공급."),
    "Oracle": ("오라클", "ORCL", "OCI(Oracle Cloud Infrastructure) 대규모 엔비디아 GPU 클러스터 및 데이터베이스 클라우드."),
    "Groq": ("그록", "Private", "LPU(Language Processing Unit) 초고속 추론 전문 ASIC 팹리스 스타트업."),
    "Marvell": ("마벨 테크놀로지", "MRVL", "커스텀 ASIC 설계 및 광학 DSP, 고속 인터커넥트 칩셋 선도."),
    "Cerebras": ("세레브라스", "Private", "웨이퍼 스케일 엔진(WSE-3) 초거대 단일 다이 AI 칩 개발사."),
    "Fluence-Energy": ("플루언스 에너지", "FLNC", "지멘스·AES 합작 글로벌 대용량 ESS 솔루션 및 에너지 관리 소프트웨어."),
    "CATL": ("닝더스다이", "300750.SZ", "세계 1위 배터리 제조사. LFP 배터리 및 대용량 그리드 ESS 주도."),
    "SK온": ("SK온", "Private", "SK이노베이션 배터리 자회사. 고성능 삼원계 NCM 배터리 및 ESS 라인업."),
    "에코프로": ("에코프로", "086520.KQ", "하이니켈 양극재 및 배터리 재활용 생태계(Eco-System) 선도."),
    "엘앤에프": ("엘앤에프", "066970.KQ", "하이니켈 NCMA 양극재 공급사."),
    "서진시스템": ("서진시스템", "178320.KQ", "글로벌 ESS 메탈 프레임 및 케이스 OEM/ODM 1위 제조사."),
    "Dell": ("델 테크놀로지스", "DELL", "엔터프라이즈 AI 서버 및 온프레미스 인프라 솔루션 1위 공급사."),
    "HPE": ("휴렛팩커드 엔터프라이즈", "HPE", "고성능 컴퓨팅(HPC) 크레이(Cray) 슈퍼컴퓨터 및 사설 AI 인프라."),
    "슈퍼마이크로": ("슈퍼마이크로컴퓨터", "SMCI", "서버 랙 스케일 액체냉각 및 엔비디아 GPU 서버 초고속 턴키 공급."),
    "삼성SDS": ("삼성SDS", "018260.KS", "엔터프라이즈 생성형 AI 플랫폼 패브릭스(FabriX) 및 브리티 코파일럿."),
    "Sony": ("소니 그룹", "SONY", "세계 1위 이미지 센서(CIS) 공급사. 공간 컴퓨팅 및 스마트 글래스 광학계."),
    "LG디스플레이": ("LG디스플레이", "034220.KS", "OLEDoS 및 차량용/AR 경량 디스플레이 패널 공급사."),
    "EssilorLuxottica": ("에실로룩소티카", "EL.PA", "메타(Meta) 레이밴 스마트 글래스 공동 개발 및 글로벌 아이웨어 1위."),
}


def create_missing_company_nodes():
    created = 0
    for key, (kr_name, ticker, desc) in COMPANY_DEFS.items():
        fp = THESIS_DIR / f"Company-{key}.md"
        if not fp.exists():
            content = f"""---
id: Company-{key}
name: "{key}"
korean_name: "{kr_name}"
ticker: "{ticker}"
type: company
created: "2026-09-06"
tags:
  - company
  - argus-hub
---

# 🏢 {kr_name} ({key})

> **티커 / 시장**: `{ticker}`  
> **핵심 포지션**: {desc}

---

## 📌 주요 연관 가설 및 사업 영역
- **기업 개요**: {desc}
- **연관 지식 허브**: [[00-Argus-Master-MOC|Argus Master MOC]]

---

## 🔗 연관 문서 (Backlinks)
```dataview
TABLE file.mtime AS "최종 수정일"
FROM ""
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "{key}")
SORT file.mtime DESC
LIMIT 15
```
"""
            fp.write_text(content, encoding="utf-8")
            created += 1
            print(f"  ✨ 생성: {fp.name}")

            # 옵시디언 동기화
            try:
                from obsidian_sync import sync_file
                sync_file(fp, "theses")
            except Exception:
                pass

    print(f"\n총 {created}개 신규 기업 허브 생성 완료.")


if __name__ == "__main__":
    create_missing_company_nodes()
