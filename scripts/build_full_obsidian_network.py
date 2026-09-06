"""
scripts/build_full_obsidian_network.py
Argus Pulse 38개 테제 및 엔티티 허브(Topic, Company), MOC를 일괄 생성하고 상호링크를 구축하는 마이그레이션 스크립트.
"""

import os
import shutil
import unicodedata
from pathlib import Path
import yaml

import sys
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
THESIS_DIR = ROOT_DIR / "thesis"
DOCS_DIR = ROOT_DIR / "docs"
OUTPUT_DIR = ROOT_DIR / "output"

import config

VAULT = config.OBSIDIAN_PATH

# ── 1. 테제별 상세 네트워크 매핑 데이터 ───────────────────────────────────────────
SECTOR_MAP = {
    # 1. AI 컴퓨트 & 차세대 반도체
    "T-02": ("AI 컴퓨트 & 반도체", "1-💾-ai-컴퓨트--차세대-반도체-compute--silicon"),
    "T-06": ("AI 컴퓨트 & 반도체", "1-💾-ai-컴퓨트--차세대-반도체-compute--silicon"),
    "T-07": ("AI 컴퓨트 & 반도체", "1-💾-ai-컴퓨트--차세대-반도체-compute--silicon"),
    "T-10": ("AI 컴퓨트 & 반도체", "1-💾-ai-컴퓨트--차세대-반도체-compute--silicon"),
    "T-11": ("AI 컴퓨트 & 반도체", "1-💾-ai-컴퓨트--차세대-반도체-compute--silicon"),
    "T-14": ("AI 컴퓨트 & 반도체", "1-💾-ai-컴퓨트--차세대-반도체-compute--silicon"),
    "T-15": ("AI 컴퓨트 & 반도체", "1-💾-ai-컴퓨트--차세대-반도체-compute--silicon"),
    "T-16": ("AI 컴퓨트 & 반도체", "1-💾-ai-컴퓨트--차세대-반도체-compute--silicon"),
    "T-24": ("AI 컴퓨트 & 반도체", "1-💾-ai-컴퓨트--차세대-반도체-compute--silicon"),
    "T-28": ("AI 컴퓨트 & 반도체", "1-💾-ai-컴퓨트--차세대-반도체-compute--silicon"),
    "T-29": ("AI 컴퓨트 & 반도체", "1-💾-ai-컴퓨트--차세대-반도체-compute--silicon"),
    "T-33": ("AI 컴퓨트 & 반도체", "1-💾-ai-컴퓨트--차세대-반도체-compute--silicon"),
    "T-35": ("AI 컴퓨트 & 반도체", "1-💾-ai-컴퓨트--차세대-반도체-compute--silicon"),
    "T-36": ("AI 컴퓨트 & 반도체", "1-💾-ai-컴퓨트--차세대-반도체-compute--silicon"),

    # 2. AI 인프라 & 전력·냉각
    "T-01": ("AI 인프라 & 전력·냉각", "2-⚡-ai-데이터센터--전력냉각-인프라-power--infrastructure"),
    "T-05": ("AI 인프라 & 전력·냉각", "2-⚡-ai-데이터센터--전력냉각-인프라-power--infrastructure"),
    "T-12": ("AI 인프라 & 전력·냉각", "2-⚡-ai-데이터센터--전력냉각-인프라-power--infrastructure"),
    "T-13": ("AI 인프라 & 전력·냉각", "2-⚡-ai-데이터센터--전력냉각-인프라-power--infrastructure"),
    "T-22": ("AI 인프라 & 전력·냉각", "2-⚡-ai-데이터센터--전력냉각-인프라-power--infrastructure"),
    "T-23": ("AI 인프라 & 전력·냉각", "2-⚡-ai-데이터센터--전력냉각-인프라-power--infrastructure"),
    "T-26": ("AI 인프라 & 전력·냉각", "2-⚡-ai-데이터센터--전력냉각-인프라-power--infrastructure"),
    "T-32": ("AI 인프라 & 전력·냉각", "2-⚡-ai-데이터센터--전력냉각-인프라-power--infrastructure"),

    # 3. 피지컬 AI & 엣지 디바이스
    "T-03": ("피지컬 AI & 엣지 디바이스", "3-🤖-피지컬-ai-로보틱스--엣지-디바이스-physical-ai--edge"),
    "T-04": ("피지컬 AI & 엣지 디바이스", "3-🤖-피지컬-ai-로보틱스--엣지-디바이스-physical-ai--edge"),
    "T-17": ("피지컬 AI & 엣지 디바이스", "3-🤖-피지컬-ai-로보틱스--엣지-디바이스-physical-ai--edge"),
    "T-18": ("피지컬 AI & 엣지 디바이스", "3-🤖-피지컬-ai-로보틱스--엣지-디바이스-physical-ai--edge"),
    "T-19": ("피지컬 AI & 엣지 디바이스", "3-🤖-피지컬-ai-로보틱스--엣지-디바이스-physical-ai--edge"),
    "T-20": ("피지컬 AI & 엣지 디바이스", "3-🤖-피지컬-ai-로보틱스--엣지-디바이스-physical-ai--edge"),
    "T-21": ("피지컬 AI & 엣지 디바이스", "3-🤖-피지컬-ai-로보틱스--엣지-디바이스-physical-ai--edge"),
    "T-27": ("피지컬 AI & 엣지 디바이스", "3-🤖-피지컬-ai-로보틱스--엣지-디바이스-physical-ai--edge"),
    "T-30": ("피지컬 AI & 엣지 디바이스", "3-🤖-피지컬-ai-로보틱스--엣지-디바이스-physical-ai--edge"),
    "T-34": ("피지컬 AI & 엣지 디바이스", "3-🤖-피지컬-ai-로보틱스--엣지-디바이스-physical-ai--edge"),

    # 4. 매크로 & 빅테크 생태계
    "T-08": ("매크로 & 빅테크 생태계", "4-🏛️-매크로-클라우드-금융--소프트웨어-과점-macro--ecosystem"),
    "T-09": ("매크로 & 빅테크 생태계", "4-🏛️-매크로-클라우드-금융--소프트웨어-과점-macro--ecosystem"),
    "T-25": ("매크로 & 빅테크 생태계", "4-🏛️-매크로-클라우드-금융--소프트웨어-과점-macro--ecosystem"),
    "T-31": ("매크로 & 빅테크 생태계", "4-🏛️-매크로-클라우드-금융--소프트웨어-과점-macro--ecosystem"),
    "T-37": ("매크로 & 빅테크 생태계", "4-🏛️-매크로-클라우드-금융--소프트웨어-과점-macro--ecosystem"),
    "T-38": ("매크로 & 빅테크 생태계", "4-🏛️-매크로-클라우드-금융--소프트웨어-과점-macro--ecosystem"),
}

# 테제별 인과관계 상세 정의 (선행, 동반, 파생 후행)
CAUSAL_MAP = {
    "T-01": {
        "pre": [("T-05", "금리와 데이터센터", "고금리 및 CAPEX ROI 압박")],
        "par": [("T-26", "소버린 AI와 국가 단위 컴퓨트 인프라", "국가별 자체 DC 구축")],
        "der": [("T-12", "데이터센터 액체냉각의 표준화", "고발열 해소"),
                ("T-23", "변압기·초고압 그리드 쇼티지 장기화", "전력망 병목"),
                ("T-13", "SMR과 데이터센터 무탄소 전력 PPA", "무탄소 전력원 확보"),
                ("T-22", "AI 전력망용 대용량 ESS와 LFP 공급망", "피크컷 전력망")],
        "topics": ["Topic-액체냉각", "Topic-전력그리드", "Topic-SMR", "Topic-ESS"],
    },
    "T-02": {
        "pre": [("T-01", "데이터센터의 변화", "연산 병목의 메모리 대역폭 전이"),
                ("T-05", "금리와 데이터센터", "CSP 메모리 예산 비중 68% 도달")],
        "par": [("T-07", "CXL 메모리의 확대", "CXL 메모리 풀링 병행"),
                ("T-36", "중국 반도체의 HBM 생산 가능성", "후발주자 레거시 추격")],
        "der": [("T-10", "첨단 패키징과 CoWoS의 병목", "16단 적층 & CoWoS 병목"),
                ("T-11", "유리기판의 차세대 패키징 침투", "대면적 기판 혁신"),
                ("T-35", "메모리 2028년 피크아웃", "2028 사이클 논쟁")],
        "topics": ["Topic-HBM", "Topic-CoWoS", "Topic-CXL"],
    },
    "T-03": {
        "pre": [],
        "par": [("T-22", "AI 전력망용 대용량 ESS와 LFP 공급망", "단기 실적 방어 및 LFP 공급망"),
                ("T-32", "ESS와 한국 배터리의 미국 수혜", "북미 공급망 수혜")],
        "der": [("T-17", "휴머노이드 로봇과 액추에이터 공급망", "고에너지밀도 로봇 탑재"),
                ("T-30", "피지컬 AI와 로봇의 상용화", "물리 AI 디바이스 전력원")],
        "topics": ["Topic-ESS", "Topic-피지컬AI"],
    },
    "T-04": {
        "pre": [],
        "par": [("T-25", "오픈소스 모델 고도화와 온프레미스 사설 AI", "소형 SLM 경량화")],
        "der": [("T-20", "행동형 AI 에이전트와 모바일 교체 슈퍼사이클", "스마트폰 교체 주기 단축"),
                ("T-21", "AI PC 보급 확대와 Arm 기반 윈도우 생태계", "차세대 AI PC 침투"),
                ("T-27", "AI 스마트 글래스와 경량 AR 광학계", "공간 컴퓨팅 기기 확산")],
        "topics": ["Topic-온디바이스AI", "Topic-ASIC"],
    },
    "T-05": {
        "pre": [("T-38", "10년 금리 5% 재진입 가능성", "매크로 고금리 장기화")],
        "par": [],
        "der": [("T-01", "데이터센터의 변화", "CAPEX ROI 검증 압박"),
                ("T-08", "엔비디아와 네오클라우드", "GPU 리스 부채 비용 급증"),
                ("T-37", "AI 버블 가능성", "수익화 지연 시 버블 붕괴")],
        "topics": ["Topic-전력그리드", "Topic-ASIC"],
    },
    "T-06": {
        "pre": [("T-01", "데이터센터의 변화", "GPU 조달 비용 급증"),
                ("T-05", "금리와 데이터센터", "CAPEX 절감 압박")],
        "par": [("T-08", "엔비디아와 네오클라우드", "엔비디아 락인 vs 자체 칩"),
                ("T-31", "AI 소프트웨어 레이어의 과점화", "소프트웨어 해자 결합")],
        "der": [("T-15", "AI 추론 시장 폭발과 LPU·ASIC 분화", "추론용 특화칩 분화"),
                ("T-24", "빅테크 커스텀 ASIC 증가와 DSP 생태계", "디자인하우스 생태계 호황")],
        "topics": ["Topic-ASIC", "Topic-2nm-GAA"],
    },
    "T-07": {
        "pre": [("T-01", "데이터센터의 변화", "서버 메모리 용량 병목"),
                ("T-02", "메모리 산업의 변화", "HBM 고가격 보완 필요")],
        "par": [("T-02", "메모리 산업의 변화", "HBM vs CXL 보완 관계")],
        "der": [("T-28", "3D DRAM 기술 전환과 400단 V-NAND", "DRAM 풀링 아키텍처")],
        "topics": ["Topic-CXL", "Topic-HBM"],
    },
    "T-08": {
        "pre": [("T-01", "데이터센터의 변화", "GPU 쇼티지 구간 네오클라우드 부상"),
                ("T-05", "금리와 데이터센터", "이자비용 상승 위험")],
        "par": [("T-06", "TPU 증가와 GPU 수요 둔화", "빅테크 자체 칩 전환")],
        "der": [("T-09", "엔비디아와 GPU 금융", "GPU 담보 차입금 확대"),
                ("T-37", "AI 버블 가능성", "네오클라우드 부실 위험")],
        "topics": ["Topic-ASIC", "Topic-액체냉각"],
    },
    "T-09": {
        "pre": [("T-08", "엔비디아와 네오클라우드", "GPU 자산화 및 금융 결합")],
        "par": [],
        "der": [("T-37", "AI 버블 가능성", "GPU 감가상각 및 담보 가치 하락"),
                ("T-05", "금리와 데이터센터", "부채 조달 한계")],
        "topics": ["Topic-ASIC"],
    },
    "T-10": {
        "pre": [("T-01", "데이터센터의 변화", "AI 가속기 칩 패키징 대형화"),
                ("T-02", "메모리 산업의 변화", "HBM 적층 및 인터포저 결합")],
        "par": [("T-14", "실리콘 포토닉스와 CPO의 상용화", "광학 인터커넥트 결합")],
        "der": [("T-11", "유리기판의 차세대 패키징 침투", "기판 휨 한계 극복"),
                ("T-16", "파운드리 2nm 공정과 GAA 격돌", "선단 파운드리-패키징 연계")],
        "topics": ["Topic-CoWoS", "Topic-HBM", "Topic-유리기판"],
    },
    "T-11": {
        "pre": [("T-10", "첨단 패키징과 CoWoS의 병목", "실리콘/유기 기판 대면적화 한계")],
        "par": [],
        "der": [("T-02", "메모리 산업의 변화", "HBM4/5 초고단수 패키징 안정화")],
        "topics": ["Topic-유리기판", "Topic-CoWoS"],
    },
    "T-12": {
        "pre": [("T-01", "데이터센터의 변화", "랙당 100kW+ 발열 폭증")],
        "par": [],
        "der": [("T-05", "금리와 데이터센터", "냉각 CAPEX 효율화로 PUE 1.1 달성")],
        "topics": ["Topic-액체냉각", "Topic-전력그리드"],
    },
    "T-13": {
        "pre": [("T-01", "데이터센터의 변화", "기저부하 무탄소 전력 수요")],
        "par": [("T-23", "변압기·초고압 그리드 쇼티지 장기화", "그리드 접속 지연 대안")],
        "der": [("T-22", "AI 전력망용 대용량 ESS와 LFP 공급망", "원전-ESS 하이브리드 PPA")],
        "topics": ["Topic-SMR", "Topic-전력그리드"],
    },
    "T-14": {
        "pre": [("T-01", "데이터센터의 변화", "데이터센터 내 구리 배선 대역폭 한계"),
                ("T-10", "첨단 패키징과 CoWoS의 병목", "CPO 패키징 통합")],
        "par": [],
        "der": [("T-29", "초고속 AI 네트워킹 UEC vs 인피니밴드", "광 스위칭 네트워크")],
        "topics": ["Topic-실리콘포토닉스", "Topic-초고속네트워킹", "Topic-CoWoS"],
    },
    "T-15": {
        "pre": [("T-06", "TPU 증가와 GPU 수요 둔화", "학습에서 추론으로의 패러다임 이동")],
        "par": [],
        "der": [("T-24", "빅테크 커스텀 ASIC 증가와 DSP 생태계", "추론 전용 ASIC 설계 수요 폭증"),
                ("T-34", "바이오 AI와 신약 개발 가속", "도메인 특화 추론 가속")],
        "topics": ["Topic-ASIC", "Topic-온디바이스AI"],
    },
    "T-16": {
        "pre": [("T-02", "메모리 산업의 변화", "HBM4 베이스 다이 선단 파운드리 요구"),
                ("T-10", "첨단 패키징과 CoWoS의 병목", "파운드리-패키징 턴키 수주")],
        "par": [],
        "der": [("T-24", "빅테크 커스텀 ASIC 증가와 DSP 생태계", "빅테크 2nm 공정 선점 경쟁")],
        "topics": ["Topic-2nm-GAA", "Topic-CoWoS"],
    },
    "T-17": {
        "pre": [("T-19", "피지컬 AI와 공간지능 반도체", "비전·물리 모델 결합"),
                ("T-03", "전고체 배터리의 변화", "로봇용 고출력 배터리")],
        "par": [],
        "der": [("T-30", "피지컬 AI와 로봇의 상용화", "제조·물류 현장 투입 양산")],
        "topics": ["Topic-피지컬AI", "Topic-자율주행"],
    },
    "T-18": {
        "pre": [("T-04", "온디바이스 AI의 변화", "차량 내 실시간 추론 연산"),
                ("T-19", "피지컬 AI와 공간지능 반도체", "VLA 기반 엔드투엔드 주행")],
        "par": [],
        "der": [("T-17", "휴머노이드 로봇과 액추에이터 공급망", "로보틱스 파운데이션 모델 공유")],
        "topics": ["Topic-자율주행", "Topic-피지컬AI"],
    },
    "T-19": {
        "pre": [("T-01", "데이터센터의 변화", "물리 엔진 학습 컴퓨트"),
                ("T-04", "온디바이스 AI의 변화", "엣지 공간 지능 추론")],
        "par": [],
        "der": [("T-17", "휴머노이드 로봇과 액추에이터 공급망", "물리 에이전트 구동"),
                ("T-18", "End-to-End AI 자율주행과 로보택시", "완전자율주행 구현"),
                ("T-27", "AI 스마트 글래스와 경량 AR 광학계", "공간 컴퓨팅 인터페이스")],
        "topics": ["Topic-피지컬AI", "Topic-자율주행", "Topic-온디바이스AI"],
    },
    "T-20": {
        "pre": [("T-04", "온디바이스 AI의 변화", "NPU 탑재 스마트폰 출시")],
        "par": [("T-21", "AI PC 보급 확대와 Arm 기반 윈도우 생태계", "PC 및 모바일 동반 교체")],
        "der": [],
        "topics": ["Topic-온디바이스AI"],
    },
    "T-21": {
        "pre": [("T-04", "온디바이스 AI의 변화", "40+ TOPS NPU 표준화")],
        "par": [("T-20", "행동형 AI 에이전트와 모바일 교체 슈퍼사이클", "디바이스 생태계 연계")],
        "der": [],
        "topics": ["Topic-온디바이스AI", "Topic-ASIC"],
    },
    "T-22": {
        "pre": [("T-01", "데이터센터의 변화", "데이터센터 전력 피크 및 간헐성 문제")],
        "par": [("T-23", "변압기·초고압 그리드 쇼티지 장기화", "그리드 안정화 보완")],
        "der": [("T-32", "ESS와 한국 배터리의 미국 수혜", "북미 LFP/NCM ESS 수혜")],
        "topics": ["Topic-ESS", "Topic-전력그리드"],
    },
    "T-23": {
        "pre": [("T-01", "데이터센터의 변화", "전력 그리드 접속 지연(인터커넥션 큐)")],
        "par": [("T-13", "SMR과 데이터센터 무탄소 전력 PPA", "현장 분산 발전"),
                ("T-22", "AI 전력망용 대용량 ESS와 LFP 공급망", "피크 완화")],
        "der": [],
        "topics": ["Topic-전력그리드"],
    },
    "T-24": {
        "pre": [("T-06", "TPU 증가와 GPU 수요 둔화", "빅테크 자체 ASIC 전환"),
                ("T-15", "AI 추론 시장 폭발과 LPU·ASIC 분화", "추론 ASIC 수요 폭증")],
        "par": [],
        "der": [("T-16", "파운드리 2nm 공정과 GAA 격돌", "디자인하우스 선단 공정 수주")],
        "topics": ["Topic-ASIC", "Topic-2nm-GAA"],
    },
    "T-25": {
        "pre": [("T-04", "온디바이스 AI의 변화", "오픈소스 가중치 모델 경량화")],
        "par": [],
        "der": [("T-26", "소버린 AI와 국가 단위 컴퓨트 인프라", "사설/국가 인프라 구축")],
        "topics": ["Topic-온디바이스AI"],
    },
    "T-26": {
        "pre": [("T-01", "데이터센터의 변화", "글로벌 컴퓨트 인프라 주권 경쟁")],
        "par": [("T-25", "오픈소스 모델 고도화와 온프레미스 사설 AI", "자체 LLM 배포")],
        "der": [],
        "topics": ["Topic-ASIC", "Topic-전력그리드"],
    },
    "T-27": {
        "pre": [("T-04", "온디바이스 AI의 변화", "초저전력 엣지 NPU"),
                ("T-19", "피지컬 AI와 공간지능 반도체", "공간 인식 광학계")],
        "par": [],
        "der": [],
        "topics": ["Topic-온디바이스AI", "Topic-피지컬AI"],
    },
    "T-28": {
        "pre": [("T-02", "메모리 산업의 변화", "1c/1d nm D램 미세화 한계"),
                ("T-07", "CXL 메모리의 확대", "초고용량 메모리 적층 요구")],
        "par": [],
        "der": [],
        "topics": ["Topic-3D-DRAM", "Topic-HBM"],
    },
    "T-29": {
        "pre": [("T-01", "데이터센터의 변화", "클러스터 스케일아웃 네트워크 병목"),
                ("T-14", "실리콘 포토닉스와 CPO의 상용화", "광 인터커넥트 도입")],
        "par": [],
        "der": [],
        "topics": ["Topic-초고속네트워킹", "Topic-실리콘포토닉스"],
    },
    "T-30": {
        "pre": [("T-03", "전고체 배터리의 변화", "차세대 로봇 배터리"),
                ("T-17", "휴머노이드 로봇과 액추에이터 공급망", "액추에이터·하드웨어 공급망")],
        "par": [],
        "der": [],
        "topics": ["Topic-피지컬AI"],
    },
    "T-31": {
        "pre": [("T-06", "TPU 증가와 GPU 수요 둔화", "빅테크 수직 계열화"),
                ("T-08", "엔비디아와 네오클라우드", "클라우드-모델 락인")],
        "par": [],
        "der": [],
        "topics": ["Topic-ASIC"],
    },
    "T-32": {
        "pre": [("T-03", "전고체 배터리의 변화", "중장기 로드맵"),
                ("T-22", "AI 전력망용 대용량 ESS와 LFP 공급망", "북미 ESS 시장 폭발")],
        "par": [],
        "der": [],
        "topics": ["Topic-ESS", "Topic-전력그리드"],
    },
    "T-33": {
        "pre": [("T-01", "데이터센터의 변화", "글로벌 공급망 재편"),
                ("T-02", "메모리 산업의 변화", "HBM 고단화 본딩 및 세정 소재 국산화")],
        "par": [],
        "der": [],
        "topics": ["Topic-HBM", "Topic-CoWoS"],
    },
    "T-34": {
        "pre": [("T-04", "온디바이스 AI의 변화", "바이오 AI 모델 연산"),
                ("T-15", "AI 추론 시장 폭발과 LPU·ASIC 분화", "단백질 구조 추론 가속")],
        "par": [],
        "der": [],
        "topics": ["Topic-ASIC"],
    },
    "T-35": {
        "pre": [("T-02", "메모리 산업의 변화", "HBM4 양산 공급 확대"),
                ("T-06", "TPU 증가와 GPU 수요 둔화", "빅테크 CAPEX 사이클"),
                ("T-07", "CXL 메모리의 확대", "메모리 대체제 출현")],
        "par": [],
        "der": [],
        "topics": ["Topic-HBM", "Topic-CXL"],
    },
    "T-36": {
        "pre": [("T-02", "메모리 산업의 변화", "HBM3E 기술 성숙")],
        "par": [],
        "der": [("T-02", "메모리 산업의 변화", "글로벌 HBM3E 마진 하방 압력")],
        "topics": ["Topic-HBM", "Topic-2nm-GAA"],
    },
    "T-37": {
        "pre": [("T-05", "금리와 데이터센터", "CAPEX ROI 불일치"),
                ("T-08", "엔비디아와 네오클라우드", "GPU 부채 리스크"),
                ("T-09", "엔비디아와 GPU 금융", "금융 레버리지 청산")],
        "par": [],
        "der": [],
        "topics": ["Topic-ASIC", "Topic-전력그리드"],
    },
    "T-38": {
        "pre": [],
        "par": [],
        "der": [("T-05", "금리와 데이터센터", "빅테크 WACC 급등 및 CAPEX 위축"),
                ("T-37", "AI 버블 가능성", "밸류에이션 디레이팅 촉발")],
        "topics": ["Topic-전력그리드"],
    },
}

# ── 2. 토픽 허브 메타데이터 ──────────────────────────────────────────────────────────
TOPICS = {
    "Topic-HBM": {
        "title": "HBM (High Bandwidth Memory & Custom ASIC)",
        "aliases": ["HBM", "고대역폭메모리", "High Bandwidth Memory", "HBM3E", "HBM4", "커스텀HBM"],
        "category": "반도체 하드웨어",
        "desc": "여러 개의 D램 다이를 TSV 기술로 적층한 고대역폭 메모리. HBM4부터 4nm 베이스 다이를 탑재한 커스텀 ASIC으로 진화.",
        "theses": ["T-02", "T-07", "T-10", "T-11", "T-28", "T-33", "T-35", "T-36"],
        "companies": ["SK하이닉스", "삼성전자", "Micron", "NVIDIA", "TSMC", "한미반도체"],
    },
    "Topic-액체냉각": {
        "title": "데이터센터 액체냉각 & DLC (Direct Liquid Cooling)",
        "aliases": ["액체냉각", "DLC", "CDU", "침전냉각", "Direct Liquid Cooling", "Liquid Cooling"],
        "category": "AI 인프라 / 냉각",
        "desc": "랙당 100kW+ 시대를 맞아 공랭식의 한계를 극복하는 직접액체냉각(DLC), CDU, 침전냉각 기술. PUE 1.1 달성의 필수 솔루션.",
        "theses": ["T-01", "T-05", "T-12"],
        "companies": ["Vertiv", "Supermicro", "Schneider", "CoolIT"],
    },
    "Topic-CoWoS": {
        "title": "CoWoS 첨단 패키징 (Chip-on-Wafer-on-Substrate)",
        "aliases": ["CoWoS", "첨단패키징", "2.5D패키징", "인터포저", "Advanced Packaging"],
        "category": "반도체 패키징",
        "desc": "실리콘 인터포저 위에 로직 다이와 HBM을 수평·수직으로 집적하는 TSMC의 독점적 첨단 2.5D 패키징 공정.",
        "theses": ["T-01", "T-02", "T-10", "T-11", "T-14", "T-16", "T-33"],
        "companies": ["TSMC", "ASE", "Amkor", "삼성전자", "SK하이닉스", "한미반도체"],
    },
    "Topic-SMR": {
        "title": "SMR (소형 모듈 원자로) & 무탄소 전력 PPA",
        "aliases": ["SMR", "소형모듈원전", "원자력PPA", "무탄소전력", "Small Modular Reactor"],
        "category": "에너지 / 전력",
        "desc": "AI 데이터센터의 24/7 무탄소 기저부하 전력 공급을 위한 차세대 소형 원전 및 빅테크 전력구매계약(PPA) 생태계.",
        "theses": ["T-01", "T-13", "T-23"],
        "companies": ["NuScale", "Constellation Energy", "Oklo", "두산에너빌리티"],
    },
    "Topic-전력그리드": {
        "title": "전력 그리드 & 변압기·HVDC 인프라",
        "aliases": ["변압기", "초고압그리드", "HVDC", "전력망", "Power Grid"],
        "category": "AI 인프라 / 전력",
        "desc": "데이터센터 전력 인입 지연을 유발하는 초고압 변압기, 전력망 인터커넥션 큐, HVDC 초고압 직류 송전망 쇼티지 생태계.",
        "theses": ["T-01", "T-05", "T-13", "T-22", "T-23", "T-38"],
        "companies": ["HD현대일렉트릭", "Eaton", "효성중공업", "LS일렉트릭", "Schneider"],
    },
    "Topic-ESS": {
        "title": "대용량 ESS & LFP 배터리 공급망",
        "aliases": ["ESS", "에너지저장장치", "BESS", "LFP배터리", "Energy Storage System"],
        "category": "배터리 / 신재생",
        "desc": "데이터센터 피크 전력 완화 및 신재생 전력 간헐성 해소를 위한 52조원 규모 북미 BESS 시장과 LFP 배터리 공급망.",
        "theses": ["T-03", "T-22", "T-32"],
        "companies": ["LG에너지솔루션", "삼성SDI", "Tesla", "Fluence Energy", "CATL"],
    },
    "Topic-CXL": {
        "title": "CXL (Compute Express Link) 메모리 풀링",
        "aliases": ["CXL", "컴퓨트익스프레스링크", "CMM-D", "메모리풀링", "CXL2.0", "CXL3.0"],
        "category": "차세대 메모리",
        "desc": "PCIe 기반으로 CPU·GPU·가속기 간 메모리를 공유하고 풀링(Pooling)하여 데이터센터 메모리 용량 한계를 극복하는 표준 인터커넥트.",
        "theses": ["T-02", "T-07", "T-28", "T-35"],
        "companies": ["삼성전자", "SK하이닉스", "Micron", "Astera Labs", "Montage"],
    },
    "Topic-유리기판": {
        "title": "차세대 패키징 유리기판 (Glass Substrate)",
        "aliases": ["유리기판", "글래스기판", "Glass Substrate", "앱솔릭스"],
        "category": "차세대 패키징 기판",
        "desc": "실리콘 인터포저와 유기 기판의 미세화 및 대면적 휨(Warpage) 한계를 돌파하는 차세대 패키징 기판 기술.",
        "theses": ["T-02", "T-10", "T-11"],
        "companies": ["SKC", "인텔", "삼성전기", "이오테크닉스", "필옵틱스"],
    },
    "Topic-ASIC": {
        "title": "빅테크 커스텀 ASIC & LPU·DSP 생태계",
        "aliases": ["ASIC", "커스텀ASIC", "LPU", "DSP", "디자인하우스", "주문형반도체"],
        "category": "반도체 아키텍처",
        "desc": "엔비디아 GPU 의존도를 낮추고 추론 비용을 절감하기 위한 구글 TPU, 메타 MTIA 등 빅테크 맞춤형 가속기 및 DSP 디자인 생태계.",
        "theses": ["T-04", "T-06", "T-08", "T-15", "T-24", "T-31", "T-34", "T-37"],
        "companies": ["Broadcom", "Marvell", "Groq", "ARM", "가온칩스", "에이직랜드"],
    },
    "Topic-2nm-GAA": {
        "title": "파운드리 2nm 공정 & GAA (Gate-All-Around)",
        "aliases": ["2nm", "GAA", "GateAllAround", "선단파운드리", "2나노"],
        "category": "선단 파운드리",
        "desc": "FinFET 한계를 극복한 3차원 GAA 트랜지스터 구조 기반의 2nm 선단 파운드리 양산 및 빅테크 칩 수주 격돌.",
        "theses": ["T-02", "T-16", "T-24", "T-36"],
        "companies": ["TSMC", "삼성전자", "인텔", "Rapidus", "ASML"],
    },
    "Topic-피지컬AI": {
        "title": "피지컬 AI & 공간지능·휴머노이드 로보틱스",
        "aliases": ["피지컬AI", "Physical AI", "공간지능", "휴머노이드", "VLA", "로보틱스"],
        "category": "로보틱스 / 차세대 AI",
        "desc": "가상 세계를 넘어 물리 세계의 3D 공간을 이해하고 조작하는 파운데이션 모델(VLA) 및 휴머노이드 로봇 생태계.",
        "theses": ["T-03", "T-17", "T-18", "T-19", "T-27", "T-30"],
        "companies": ["Tesla", "Boston Dynamics", "Figure AI", "현대차", "NVIDIA", "두산로보틱스"],
    },
    "Topic-자율주행": {
        "title": "End-to-End AI 자율주행 & 로보택시",
        "aliases": ["자율주행", "FSD", "로보택시", "E2E자율주행", "Autonomous Driving"],
        "category": "모빌리티 / AI",
        "desc": "센서 데이터 입력부터 제어 출력까지 하나의 신경망으로 처리하는 End-to-End 신경망 자율주행 및 상용 로보택시 네트워크.",
        "theses": ["T-04", "T-18", "T-19"],
        "companies": ["Tesla", "Waymo", "Cruise", "현대차", "모빌아이"],
    },
    "Topic-온디바이스AI": {
        "title": "온디바이스 AI & NPU 기반 행동형 에이전트",
        "aliases": ["온디바이스AI", "Edge AI", "NPU", "Apple Intelligence", "Galaxy AI", "행동형에이전트"],
        "category": "엣지 컴퓨팅 / 모바일",
        "desc": "45+ TOPS NPU를 탑재한 스마트폰·PC에서 클라우드 연결 없이 개인화된 태스크를 자율 수행하는 온디바이스 에이전트 생태계.",
        "theses": ["T-04", "T-20", "T-21", "T-25", "T-27"],
        "companies": ["Apple", "삼성전자", "Qualcomm", "MediaTek", "Microsoft", "Google"],
    },
    "Topic-실리콘포토닉스": {
        "title": "실리콘 포토닉스 & CPO (Co-Packaged Optics)",
        "aliases": ["실리콘포토닉스", "CPO", "광인터커넥트", "Optical Interconnect", "Silicon Photonics"],
        "category": "네트워킹 / 광학",
        "desc": "전기 신호 대신 빛(광자)을 사용하여 칩 간 대용량 데이터를 초저지연·초저전력으로 전송하는 광반도체 기술.",
        "theses": ["T-01", "T-14", "T-29"],
        "companies": ["Broadcom", "TSMC", "Marvell", "Coherent", "Cisco"],
    },
    "Topic-3D-DRAM": {
        "title": "3D DRAM & 400단 V-NAND 고단화",
        "aliases": ["3D DRAM", "3DDRAM", "400단낸드", "V-NAND", "3D메모리"],
        "category": "차세대 메모리",
        "desc": "셀을 수직으로 세우는 3D D램 아키텍처와 400단 이상 초고단 V-NAND 적층을 통한 메모리 미세화 한계 극복 기술.",
        "theses": ["T-02", "T-07", "T-28"],
        "companies": ["SK하이닉스", "삼성전자", "Micron", "Tokyo Electron", "Applied Materials"],
    },
    "Topic-초고속네트워킹": {
        "title": "초고속 AI 네트워킹 (UEC vs 인피니밴드)",
        "aliases": ["UEC", "인피니밴드", "Ultra Ethernet", "InfiniBand", "AI네트워킹"],
        "category": "AI 인프라 / 네트워킹",
        "desc": "수만 개 가속기를 묶는 AI 클러스터에서 엔비디아 인피니밴드 독점망과 빅테크 연합의 울트라 이더넷(UEC) 간 표준 경쟁.",
        "theses": ["T-01", "T-14", "T-29"],
        "companies": ["Arista Networks", "NVIDIA", "Cisco", "Broadcom", "Marvell"],
    },
}

# ── 3. 기업 허브 메타데이터 ──────────────────────────────────────────────────────────
COMPANIES = {
    "Company-삼성전자": {
        "title": "삼성전자 (Samsung Electronics | 005930.KS)",
        "aliases": ["삼성전자", "Samsung", "005930"],
        "ticker": "005930.KS",
        "sector": "반도체 / 모바일",
        "desc": "글로벌 1위 메모리 제조사이자 파운드리·패키징 턴키(Turnkey) 역량을 갖춘 종합 반도체(IDM) 기업. CUBE/zHBM 아키텍처로 HBM4 반격 주도.",
        "theses": ["T-02", "T-04", "T-07", "T-10", "T-11", "T-16", "T-20", "T-28", "T-33", "T-35"],
    },
    "Company-NVIDIA": {
        "title": "NVIDIA (엔비디아 | NVDA)",
        "aliases": ["NVIDIA", "엔비디아", "NVDA"],
        "ticker": "NVDA",
        "sector": "AI 반도체 / 컴퓨팅",
        "desc": "CUDA 생태계와 Hopper/Blackwell/Vera Rubin 아키텍처를 앞세워 전 세계 AI 가속기 시장을 80%+ 점유하는 글로벌 AI 대장주.",
        "theses": ["T-01", "T-02", "T-06", "T-08", "T-09", "T-19", "T-26", "T-29", "T-37"],
    },
    "Company-TSMC": {
        "title": "TSMC (TSM)",
        "aliases": ["TSMC", "TSM", "대만적체전로"],
        "ticker": "TSM",
        "sector": "파운드리 / 첨단 패키징",
        "desc": "글로벌 파운드리 60%+ 점유율과 CoWoS 첨단 패키징 생태계를 독점하여 엔비디아, 애플, 빅테크 커스텀 칩을 전량 위탁 생산하는 핵심 인프라.",
        "theses": ["T-01", "T-02", "T-10", "T-11", "T-14", "T-16", "T-24"],
    },
    "Company-HD현대일렉트릭": {
        "title": "HD현대일렉트릭 (267260.KS)",
        "aliases": ["HD현대일렉트릭", "현대일렉트릭", "267260"],
        "ticker": "267260.KS",
        "sector": "전력 기기 / 인프라",
        "desc": "북미 초고압 변압기 및 전력망 쇼티지 슈퍼사이클의 최대 수혜 기업. 2028년까지 생산 캐파 완판 및 높은 OPM 기록.",
        "theses": ["T-01", "T-23"],
    },
    "Company-LG에너지솔루션": {
        "title": "LG에너지솔루션 (373220.KS)",
        "aliases": ["LG에너지솔루션", "LG엔솔", "373220"],
        "ticker": "373220.KS",
        "sector": "2차전지 / ESS",
        "desc": "북미 ESS(에너지저장장치) 시장에서 LFP 및 고용량 배터리 현지 공급망을 선점하여 AI 전력망 인프라 수혜를 극대화하는 배터리 선도사.",
        "theses": ["T-03", "T-22", "T-32"],
    },
    "Company-Vertiv": {
        "title": "Vertiv Holdings (VRT)",
        "aliases": ["Vertiv", "버티브", "VRT"],
        "ticker": "VRT",
        "sector": "데이터센터 전력·냉각",
        "desc": "AI 고밀도 랙에 필수적인 액체냉각(CDU/DLC) 및 무정전 전원장치(UPS) 분야 글로벌 1위 기업.",
        "theses": ["T-01", "T-12"],
    },
    "Company-Broadcom": {
        "title": "Broadcom (AVGO)",
        "aliases": ["Broadcom", "브로드컴", "AVGO"],
        "ticker": "AVGO",
        "sector": "커스텀 ASIC / 네트워킹",
        "desc": "구글 TPU, 메타 MTIA 등 빅테크 커스텀 ASIC 설계 및 CPO/초고속 네트워킹 칩셋 시장의 절대 강자.",
        "theses": ["T-06", "T-14", "T-24", "T-29"],
    },
    "Company-Tesla": {
        "title": "Tesla (테슬라 | TSLA)",
        "aliases": ["Tesla", "테슬라", "TSLA"],
        "ticker": "TSLA",
        "sector": "피지컬 AI / 모빌리티",
        "desc": "FSD(자율주행), Optimus(휴머노이드 로봇), Megapack(대용량 ESS)을 아우르는 피지컬 AI 및 에너지 통합 기업.",
        "theses": ["T-17", "T-18", "T-19", "T-22", "T-30"],
    },
    "Company-Apple": {
        "title": "Apple (애플 | AAPL)",
        "aliases": ["Apple", "애플", "AAPL"],
        "ticker": "AAPL",
        "sector": "온디바이스 AI / 디바이스",
        "desc": "Apple Intelligence와 차세대 Apple Silicon(M/A 시리즈)을 통해 20억 대 활성 기기 기반의 온디바이스 AI 슈퍼사이클을 주도.",
        "theses": ["T-04", "T-20", "T-27"],
    },
    "Company-Qualcomm": {
        "title": "Qualcomm (퀄컴 | QCOM)",
        "aliases": ["Qualcomm", "퀄컴", "QCOM"],
        "ticker": "QCOM",
        "sector": "온디바이스 AI / AP",
        "desc": "Snapdragon X Elite(AI PC) 및 8 Gen 시리즈로 45+ TOPS 엣지 NPU 시장을 선도하는 팹리스 기업.",
        "theses": ["T-04", "T-19", "T-20", "T-21"],
    },
    "Company-Meta": {
        "title": "Meta Platforms (META)",
        "aliases": ["Meta", "메타", "META"],
        "ticker": "META",
        "sector": "AI 소프트웨어 / 오픈소스",
        "desc": "오픈소스 LLM(Llama) 생태계와 Ray-Ban 스마트글래스 및 자체 MTIA 가속기를 통해 AI 생태계를 주도.",
        "theses": ["T-05", "T-25", "T-27", "T-37"],
    },
    "Company-Microsoft": {
        "title": "Microsoft (MSFT)",
        "aliases": ["Microsoft", "마이크로소프트", "MSFT"],
        "ticker": "MSFT",
        "sector": "클라우드 / 엔터프라이즈 AI",
        "desc": "Azure 클라우드와 OpenAI 협력, Copilot 플랫폼을 통해 전 세계 엔터프라이즈 AI 소프트웨어 시장을 과점.",
        "theses": ["T-05", "T-21", "T-31", "T-37"],
    },
    "Company-Alphabet": {
        "title": "Alphabet (구글 | GOOGL)",
        "aliases": ["Alphabet", "구글", "Google", "GOOGL"],
        "ticker": "GOOGL",
        "sector": "AI 가속기 / 클라우드",
        "desc": "자체 TPU v5/v6 아키텍처와 Gemini 모델, Waymo 로보택시를 앞세워 하드웨어부터 서비스까지 풀스택 AI를 구축.",
        "theses": ["T-04", "T-06", "T-18", "T-31", "T-37"],
    },
    "Company-CoreWeave": {
        "title": "CoreWeave (코어위브)",
        "aliases": ["CoreWeave", "코어위브"],
        "ticker": "Private",
        "sector": "GPU 특화 클라우드",
        "desc": "엔비디아 GPU를 담보로 대규모 차입을 일으켜 GPU 클라우드 인프라를 확장하는 네오클라우드의 대표 주자.",
        "theses": ["T-08", "T-09", "T-37"],
    },
}


def get_thesis_filename_map() -> dict[str, str]:
    """T-XX ID를 실제 파일명으로 매핑 (NFC 정규화)"""
    mapping = {}
    for p in THESIS_DIR.glob("T-*.md"):
        norm_name = unicodedata.normalize("NFC", p.name)
        tid = norm_name.split("-")[0] + "-" + norm_name.split("-")[1]
        mapping[tid] = norm_name
    return mapping


def build_topic_files():
    """모든 Topic Hub MD 파일 생성"""
    file_map = get_thesis_filename_map()
    for key, data in TOPICS.items():
        aliases_yaml = "\n".join([f"  - {a}" for a in data["aliases"]])
        theses_links = []
        for tid in data["theses"]:
            fname = file_map.get(tid, f"{tid}.md")
            theses_links.append(f"- [[{fname.replace('.md', '')}|{tid}]]")
        
        theses_str = "\n".join(theses_links)
        companies_links = ", ".join([f"[[Company-{c}|{c}]]" for c in data["companies"]])

        content = f"""---
aliases:
{aliases_yaml}
type: topic
category: {data['category']}
created: 2026-09-06
---

# 💡 {data['title']}

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 개념 개요 및 산업 변곡점
{data['desc']}

---

## 🔗 연관 투자 테제 매핑 (Theses Network)
{theses_str}

---

## 🏢 핵심 플레이어 및 공급망
- **주요 기업**: {companies_links}

---

## 📑 관련 분석 리포트 (Dataview)

```dataview
TABLE file.mtime AS "작성일", title AS "제목", angle AS "관점"
FROM "argus" OR "output"
WHERE contains(file.tags, "{data['aliases'][0]}") OR contains(file.text, "{data['aliases'][0]}")
SORT file.mtime DESC
LIMIT 8
```
"""
        target = THESIS_DIR / f"{key}.md"
        target.write_text(content, encoding="utf-8")
        print(f"  💡 [Topic Hub 생성] {key}.md")


def build_company_files():
    """모든 Company Hub MD 파일 생성"""
    file_map = get_thesis_filename_map()
    for key, data in COMPANIES.items():
        aliases_yaml = "\n".join([f"  - {a}" for a in data["aliases"]])
        theses_links = []
        for tid in data["theses"]:
            fname = file_map.get(tid, f"{tid}.md")
            theses_links.append(f"- [[{fname.replace('.md', '')}|{tid}]]")
        theses_str = "\n".join(theses_links)

        content = f"""---
aliases:
{aliases_yaml}
type: company
ticker: "{data['ticker']}"
sector: {data['sector']}
created: 2026-09-06
---

# 🏢 {data['title']}

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]]

---

## 📌 기업 개요 및 AI 생태계 내 포지션
{data['desc']}

---

## 🔗 연관 투자 가설 (Thesis Mapping)
{theses_str}

---

## 📑 관련 리포트 & 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", tags AS "태그", type AS "유형"
FROM "argus" OR "output"
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "{data['aliases'][0]}")
SORT file.mtime DESC
LIMIT 8
```
"""
        target = THESIS_DIR / f"{key}.md"
        target.write_text(content, encoding="utf-8")
        print(f"  🏢 [Company Hub 생성] {key}.md")


def upgrade_all_theses():
    """38개 전체 테제 마크다운 파일 상호링크 전면 업그레이드"""
    file_map = get_thesis_filename_map()

    for p in sorted(THESIS_DIR.glob("T-*.md")):
        text = p.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue

        parts = text.split("---", 2)
        if len(parts) < 3:
            continue

        meta = yaml.safe_load(parts[1]) or {}
        raw_body = parts[2].lstrip("\r\n")

        tid = meta.get("id")
        title = meta.get("title", "")
        hypo = meta.get("hypothesis", "")

        # 1. Aliases 구성
        aliases = meta.get("aliases") or []
        if tid and tid not in aliases:
            aliases.insert(0, tid)
        full_alias = f"{tid} {title}"
        if full_alias not in aliases:
            aliases.append(full_alias)
        if title and title not in aliases:
            aliases.append(title)
        meta["aliases"] = aliases

        # 2. 섹터 및 MOC 링크
        sector_info = SECTOR_MAP.get(tid, ("AI 인프라 & 반도체", "00-Argus-Master-MOC"))
        sector_name, sector_anchor = sector_info

        # 3. Causal Network 정보
        c_info = CAUSAL_MAP.get(tid, {"pre": [], "par": [], "der": [], "topics": []})

        pre_links = []
        for pid, ptitle, reason in c_info.get("pre", []):
            pfname = file_map.get(pid, f"{pid}.md").replace(".md", "")
            pre_links.append(f"  - [[{pfname}|{pid} {ptitle}]] — {reason}")

        par_links = []
        for pid, ptitle, reason in c_info.get("par", []):
            pfname = file_map.get(pid, f"{pid}.md").replace(".md", "")
            par_links.append(f"  - [[{pfname}|{pid} {ptitle}]] — {reason}")

        der_links = []
        for pid, ptitle, reason in c_info.get("der", []):
            pfname = file_map.get(pid, f"{pid}.md").replace(".md", "")
            der_links.append(f"  - [[{pfname}|{pid} {ptitle}]] — {reason}")

        # Mermaid 관계도
        mermaid_lines = ["graph LR"]
        cur_node = f"T_{tid.replace('-', '_')}[\"★ [[{p.name.replace('.md', '')}|{tid} {title}]]\"]"
        for pid, ptitle, _ in c_info.get("pre", []):
            pnode = f"P_{pid.replace('-', '_')}[\"[[{file_map.get(pid, pid).replace('.md', '')}|{pid} {ptitle}]]\"]"
            mermaid_lines.append(f"    {pnode} --> {cur_node}")
        for pid, ptitle, _ in c_info.get("der", []):
            dnode = f"D_{pid.replace('-', '_')}[\"[[{file_map.get(pid, pid).replace('.md', '')}|{pid} {ptitle}]]\"]"
            mermaid_lines.append(f"    {cur_node} --> {dnode}")
        for pid, ptitle, _ in c_info.get("par", []):
            snode = f"S_{pid.replace('-', '_')}[\"[[{file_map.get(pid, pid).replace('.md', '')}|{pid} {ptitle}]]\"]"
            mermaid_lines.append(f"    {cur_node} <.-> {snode}")

        if len(mermaid_lines) == 1:
            mermaid_lines.append(f"    {cur_node}")
        mermaid_block = "\n".join(mermaid_lines)

        # 4. 연관 기업 & 기술 허브 링크
        comp_links = ", ".join([f"[[Company-{c}|{c}]]" for c in meta.get("related_companies", [])])
        topic_links = ", ".join([f"[[{t}|{t.replace('Topic-', '')}]]" for t in c_info.get("topics", [])])

        # 5. 기존 본문에서 지지 근거, 반박 근거, 관련 블로그, 메모 추출
        sections = {"지지 근거": "", "반박 근거": "", "관련 블로그": "", "메모": ""}
        current_sec = None
        current_sec_lines = []

        for line in raw_body.splitlines():
            if line.startswith("## "):
                sec_title = line.replace("## ", "").strip()
                if current_sec:
                    sections[current_sec] = "\n".join(current_sec_lines).strip()
                current_sec = sec_title
                current_sec_lines = []
            elif current_sec:
                current_sec_lines.append(line)
        if current_sec:
            sections[current_sec] = "\n".join(current_sec_lines).strip()

        # 본문 재생성
        new_body = f"""# {tid} {title}

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]] ➔ [[00-Argus-Master-MOC#{sector_anchor}|{sector_name}]]

---

## 🎯 핵심 가설
{hypo}

---

## 🔗 테제 네트워크 (상호 연관 가설)

```mermaid
{mermaid_block}
```

- 🔼 **선행 가설 (배경 요인 & 상위 인프라)**:
{chr(10).join(pre_links) if pre_links else "  - (독립적 기저 요인)"}
- ➡️ **동반 및 대체·경쟁 가설**:
{chr(10).join(par_links) if par_links else "  - (해당 없음)"}
- 🔽 **파생 및 후행 병목 가설**:
{chr(10).join(der_links) if der_links else "  - (해당 없음)"}

---

## 🏢 연관 기업 & 핵심 기술 허브
- **핵심 기업**: {comp_links if comp_links else "N/A"}
- **핵심 기술/토픽**: {topic_links if topic_links else "N/A"}

---

## 📈 지지 근거
{sections.get("지지 근거", "<!-- 시스템이 자동으로 채워주거나 사용자가 직접 메모 -->")}

---

## 📉 반박 근거
{sections.get("반박 근거", "<!-- 가설에 반하는 뉴스/데이터 -->")}

---

## 📑 관련 산출물 (자동 집계)

### 🤖 Dataview 실시간 역방향 링크
```dataview
TABLE file.mtime AS "작성일", angle AS "관점", tags AS "태그"
FROM "argus" OR "output"
WHERE contains(thesis, "{tid}") OR contains(file.outlinks, this.file.link)
SORT file.mtime DESC
LIMIT 7
```

### 📌 수동 링크 아카이브
{sections.get("관련 블로그", "<!-- [[블로그 파일명]] 형식으로 링크 -->")}

---

## 📝 분석가 메모
{sections.get("메모", "")}
"""

        # YAML 덤프 후 저장
        yaml_str = yaml.dump(meta, allow_unicode=True, sort_keys=False)
        full_content = f"---\n{yaml_str}---\n\n{new_body}"
        p.write_text(full_content, encoding="utf-8")
        print(f"  📝 [Thesis 업그레이드 완료] {tid} — {title}")


def sync_all_to_vault():
    """모든 업그레이드 파일들을 사용자 옵시디언 볼트로 전체 동기화"""
    if not VAULT.exists():
        print(f"  ❌ 옵시디언 볼트 경로 없음: {VAULT}")
        return

    print(f"\n📂 [옵시디언 볼트 전체 동기화 진행 중...]")
    (VAULT / "argus" / "Theses").mkdir(parents=True, exist_ok=True)
    (VAULT / "argus" / "Topics").mkdir(parents=True, exist_ok=True)
    (VAULT / "argus" / "Companies").mkdir(parents=True, exist_ok=True)
    (VAULT / "argus" / "Docs").mkdir(parents=True, exist_ok=True)
    (VAULT / "argus" / "Blog").mkdir(parents=True, exist_ok=True)

    # 1. Master MOC
    shutil.copy2(THESIS_DIR / "00-Argus-Master-MOC.md", VAULT / "argus" / "00-Argus-Master-MOC.md")

    # 2. Docs
    for d in DOCS_DIR.glob("*.md"):
        shutil.copy2(d, VAULT / "argus" / "Docs" / d.name)

    # 3. 38개 Theses
    count_t = 0
    for t in THESIS_DIR.glob("T-*.md"):
        norm_name = unicodedata.normalize("NFC", t.name)
        shutil.copy2(t, VAULT / "argus" / "Theses" / norm_name)
        count_t += 1

    # 4. Topics
    count_top = 0
    for top in THESIS_DIR.glob("Topic-*.md"):
        shutil.copy2(top, VAULT / "argus" / "Topics" / top.name)
        count_top += 1

    # 5. Companies
    count_c = 0
    for c in THESIS_DIR.glob("Company-*.md"):
        shutil.copy2(c, VAULT / "argus" / "Companies" / c.name)
        count_c += 1

    # 6. Blog
    count_b = 0
    blog_dir = OUTPUT_DIR / "blog"
    if blog_dir.exists():
        for b in blog_dir.glob("*.md"):
            shutil.copy2(b, VAULT / "argus" / "Blog" / b.name)
            count_b += 1

    print(f"  ✅ 동기화 완료:")
    print(f"     - Master MOC: 1개")
    print(f"     - Theses: {count_t}개")
    print(f"     - Topics: {count_top}개")
    print(f"     - Companies: {count_c}개")
    print(f"     - Blog: {count_b}개")


if __name__ == "__main__":
    print("🚀 [Argus Pulse] 전체 상호링크 네트워크 구축 시작\n")
    build_topic_files()
    print()
    build_company_files()
    print()
    upgrade_all_theses()
    print()
    sync_all_to_vault()
    print("\n🎉 모든 작업이 성공적으로 완료되었습니다!")
