"""
scripts/migrate_theses_to_t1_format.py
38개 테제 파일명을 T1-01 ~ T6-02 (대분류 T1~T6 갯수순, 소분류 01~13) 체계로 일괄 전환하고,
내부 메타데이터, 상호링크, Topic/Company/Vs/MOC 허브 및 파이썬 동기화 엔진을 전면 갱신.
"""

import os
import sys
import shutil
from pathlib import Path
import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
THESIS_DIR = ROOT_DIR / "thesis"
DOCS_DIR = ROOT_DIR / "docs"

import config
VAULT = config.OBSIDIAN_PATH

# ── 38개 테제 매핑 정의: (구 섹터코드 SC/DC/RB/SW/GE/MC ➔ 신규 T1~T6 체계) ───
# Sector 1: Silicon & Compute (반도체) - 13개 -> T1
# Sector 2: Robotics & Physical AI (로봇·디바이스) - 9개 -> T2
# Sector 3: Data Center & Power (인프라·전력) - 6개 -> T3
# Sector 4: Macro & Capital Markets (매크로·자본시장) - 5개 -> T4
# Sector 5: Software & Enterprise Agents (SW·에이전트) - 3개 -> T5
# Sector 6: Geopolitics & Sovereign (지정학·소버린) - 2개 -> T6

MAPPING = [
    # 💾 T1 (반도체 / Silicon & Compute) - 13개
    {"old_sector_id": "SC-01", "old_t_id": "T-02", "new_id": "T1-01", "slug": "메모리-산업의-변화", "title": "메모리 산업의 변화", "sector": "AI 컴퓨트 & 차세대 반도체", "sector_id": "T1", "nature": "consensus", "stack_name": "L1 (칩/패키징)", "stack_layer": "L1", "geo": ["KR", "US", "TW"], "horizon": "2026~2027", "vs": ["Vs-TSMC동맹-vs-삼성턴키"]},
    {"old_sector_id": "SC-02", "old_t_id": "T-06", "new_id": "T1-02", "slug": "TPU-증가와-GPU-수요-둔화", "title": "TPU 증가와 GPU 수요 둔화", "sector": "AI 컴퓨트 & 차세대 반도체", "sector_id": "T1", "nature": "contrarian", "stack_name": "L1 (칩/패키징)", "stack_layer": "L1", "geo": ["US", "TW"], "horizon": "2026~2027", "vs": ["Vs-GPU-vs-TPU-ASIC"]},
    {"old_sector_id": "SC-03", "old_t_id": "T-07", "new_id": "T1-03", "slug": "CXL-메모리의-확대", "title": "CXL 메모리의 확대", "sector": "AI 컴퓨트 & 차세대 반도체", "sector_id": "T1", "nature": "consensus", "stack_name": "L1 (칩/패키징)", "stack_layer": "L1", "geo": ["KR", "US"], "horizon": "2026H2~2027", "vs": []},
    {"old_sector_id": "SC-04", "old_t_id": "T-10", "new_id": "T1-04", "slug": "첨단-패키징과-CoWoS의-병목", "title": "첨단 패키징과 CoWoS의 병목", "sector": "AI 컴퓨트 & 차세대 반도체", "sector_id": "T1", "nature": "consensus", "stack_name": "L1 (칩/패키징)", "stack_layer": "L1", "geo": ["TW", "KR", "US"], "horizon": "2026~2027", "vs": ["Vs-TSMC동맹-vs-삼성턴키"]},
    {"old_sector_id": "SC-05", "old_t_id": "T-11", "new_id": "T1-05", "slug": "유리기판의-차세대-패키징-침투", "title": "유리기판의 차세대 패키징 침투", "sector": "AI 컴퓨트 & 차세대 반도체", "sector_id": "T1", "nature": "consensus", "stack_name": "L0 (소부장/기판)", "stack_layer": "L0", "geo": ["KR", "US"], "horizon": "2027~2028", "vs": []},
    {"old_sector_id": "SC-06", "old_t_id": "T-14", "new_id": "T1-06", "slug": "실리콘-포토닉스와-CPO의-상용화", "title": "실리콘 포토닉스와 CPO의 상용화", "sector": "AI 컴퓨트 & 차세대 반도체", "sector_id": "T1", "nature": "consensus", "stack_name": "L3 (네트워킹)", "stack_layer": "L3", "geo": ["US", "TW"], "horizon": "2027~2028", "vs": ["Vs-인피니밴드-vs-울트라이더넷"]},
    {"old_sector_id": "SC-07", "old_t_id": "T-15", "new_id": "T1-07", "slug": "AI-추론-시장-폭발과-LPU-ASIC-분화", "title": "AI 추론 시장 폭발과 LPU·ASIC 분화", "sector": "AI 컴퓨트 & 차세대 반도체", "sector_id": "T1", "nature": "consensus", "stack_name": "L1 (칩/패키징)", "stack_layer": "L1", "geo": ["US", "KR"], "horizon": "2026~2027", "vs": ["Vs-GPU-vs-TPU-ASIC"]},
    {"old_sector_id": "SC-08", "old_t_id": "T-16", "new_id": "T1-08", "slug": "파운드리-2nm-공정과-GAA-격돌", "title": "파운드리 2nm 공정과 GAA 격돌", "sector": "AI 컴퓨트 & 차세대 반도체", "sector_id": "T1", "nature": "consensus", "stack_name": "L1 (칩/패키징)", "stack_layer": "L1", "geo": ["TW", "KR", "US"], "horizon": "2026H2~2027", "vs": ["Vs-TSMC동맹-vs-삼성턴키"]},
    {"old_sector_id": "SC-09", "old_t_id": "T-24", "new_id": "T1-09", "slug": "빅테크-커스텀-ASIC-증가와-DSP-생태계", "title": "빅테크 커스텀 ASIC 증가와 DSP 생태계", "sector": "AI 컴퓨트 & 차세대 반도체", "sector_id": "T1", "nature": "consensus", "stack_name": "L1 (칩/패키징)", "stack_layer": "L1", "geo": ["US", "KR", "TW"], "horizon": "2026~2027", "vs": ["Vs-GPU-vs-TPU-ASIC"]},
    {"old_sector_id": "SC-10", "old_t_id": "T-28", "new_id": "T1-10", "slug": "3D-DRAM-기술-전환과-400단-V-NAND", "title": "3D DRAM 기술 전환과 400단 V-NAND", "sector": "AI 컴퓨트 & 차세대 반도체", "sector_id": "T1", "nature": "consensus", "stack_name": "L1 (칩/패키징)", "stack_layer": "L1", "geo": ["KR", "US"], "horizon": "2027~2029", "vs": []},
    {"old_sector_id": "SC-11", "old_t_id": "T-29", "new_id": "T1-11", "slug": "초고속-AI-네트워킹-UEC-vs-인피니밴드", "title": "초고속 AI 네트워킹 UEC vs 인피니밴드", "sector": "AI 컴퓨트 & 차세대 반도체", "sector_id": "T1", "nature": "consensus", "stack_name": "L3 (네트워킹)", "stack_layer": "L3", "geo": ["US"], "horizon": "2026~2027", "vs": ["Vs-인피니밴드-vs-울트라이더넷"]},
    {"old_sector_id": "SC-12", "old_t_id": "T-33", "new_id": "T1-12", "slug": "반도체-소부장의-내재화", "title": "반도체 소부장의 내재화", "sector": "AI 컴퓨트 & 차세대 반도체", "sector_id": "T1", "nature": "consensus", "stack_name": "L0 (소부장)", "stack_layer": "L0", "geo": ["KR"], "horizon": "2026~2027", "vs": []},
    {"old_sector_id": "SC-13", "old_t_id": "T-35", "new_id": "T1-13", "slug": "메모리-2028년-피크아웃", "title": "메모리 2028년 피크아웃", "sector": "AI 컴퓨트 & 차세대 반도체", "sector_id": "T1", "nature": "contrarian", "stack_name": "L1 (칩/패키징)", "stack_layer": "L1", "geo": ["KR", "US"], "horizon": "2027H2~2028", "vs": []},

    # 🤖 T2 (로보틱스·디바이스 / Robotics & Physical AI) - 9개
    {"old_sector_id": "RB-01", "old_t_id": "T-03", "new_id": "T2-01", "slug": "전고체-배터리의-변화", "title": "전고체 배터리의 변화", "sector": "피지컬 AI, 모빌리티 & 로보틱스", "sector_id": "T2", "nature": "consensus", "stack_name": "L0 (소재/배터리)", "stack_layer": "L0", "geo": ["KR", "JP", "US"], "horizon": "2026H2~2028", "vs": []},
    {"old_sector_id": "RB-02", "old_t_id": "T-04", "new_id": "T2-02", "slug": "온디바이스-AI의-변화", "title": "온디바이스 AI의 변화", "sector": "피지컬 AI, 모빌리티 & 로보틱스", "sector_id": "T2", "nature": "consensus", "stack_name": "L5 (디바이스)", "stack_layer": "L5", "geo": ["US", "KR"], "horizon": "2026~2027", "vs": []},
    {"old_sector_id": "RB-03", "old_t_id": "T-17", "new_id": "T2-03", "slug": "휴머노이드-로봇과-액추에이터-공급망", "title": "휴머노이드 로봇과 액추에이터 공급망", "sector": "피지컬 AI, 모빌리티 & 로보틱스", "sector_id": "T2", "nature": "consensus", "stack_name": "L5 (디바이스)", "stack_layer": "L5", "geo": ["US", "KR"], "horizon": "2027~2029", "vs": []},
    {"old_sector_id": "RB-04", "old_t_id": "T-18", "new_id": "T2-04", "slug": "End-to-End-AI-자율주행과-로보택시", "title": "End-to-End AI 자율주행과 로보택시", "sector": "피지컬 AI, 모빌리티 & 로보틱스", "sector_id": "T2", "nature": "consensus", "stack_name": "L5 (디바이스)", "stack_layer": "L5", "geo": ["US", "KR"], "horizon": "2026~2027", "vs": []},
    {"old_sector_id": "RB-05", "old_t_id": "T-19", "new_id": "T2-05", "slug": "피지컬-AI와-공간지능-반도체", "title": "피지컬 AI와 공간지능 반도체", "sector": "피지컬 AI, 모빌리티 & 로보틱스", "sector_id": "T2", "nature": "consensus", "stack_name": "L1 (칩/패키징)", "stack_layer": "L1", "geo": ["US", "JP"], "horizon": "2026~2028", "vs": []},
    {"old_sector_id": "RB-06", "old_t_id": "T-20", "new_id": "T2-06", "slug": "행동형-AI-에이전트와-모바일-교체-슈퍼사이클", "title": "행동형 AI 에이전트와 모바일 교체 슈퍼사이클", "sector": "피지컬 AI, 모빌리티 & 로보틱스", "sector_id": "T2", "nature": "consensus", "stack_name": "L5 (디바이스)", "stack_layer": "L5", "geo": ["US", "KR"], "horizon": "2026~2027", "vs": []},
    {"old_sector_id": "RB-07", "old_t_id": "T-21", "new_id": "T2-07", "slug": "AI-PC-보급-확대와-Arm-기반-윈도우-생태계", "title": "AI PC 보급 확대와 Arm 기반 윈도우 생태계", "sector": "피지컬 AI, 모빌리티 & 로보틱스", "sector_id": "T2", "nature": "consensus", "stack_name": "L5 (디바이스)", "stack_layer": "L5", "geo": ["US"], "horizon": "2026~2027", "vs": []},
    {"old_sector_id": "RB-08", "old_t_id": "T-27", "new_id": "T2-08", "slug": "AI-스마트-글래스와-경량-AR-광학계", "title": "AI 스마트 글래스와 경량 AR 광학계", "sector": "피지컬 AI, 모빌리티 & 로보틱스", "sector_id": "T2", "nature": "consensus", "stack_name": "L5 (디바이스)", "stack_layer": "L5", "geo": ["US", "KR"], "horizon": "2026~2027", "vs": []},
    {"old_sector_id": "RB-09", "old_t_id": "T-30", "new_id": "T2-09", "slug": "피지컬AI와-로봇의-상용화", "title": "피지컬 AI와 로봇의 상용화", "sector": "피지컬 AI, 모빌리티 & 로보틱스", "sector_id": "T2", "nature": "consensus", "stack_name": "L5 (디바이스)", "stack_layer": "L5", "geo": ["KR", "US"], "horizon": "2026~2028", "vs": []},

    # ⚡ T3 (인프라·전력 / Data Center & Power) - 6개
    {"old_sector_id": "DC-01", "old_t_id": "T-01", "new_id": "T3-01", "slug": "데이터센터의-변화", "title": "데이터센터의 변화", "sector": "AI 데이터센터 & 전력·냉각 인프라", "sector_id": "T3", "nature": "consensus", "stack_name": "L2 (물리인프라)", "stack_layer": "L2", "geo": ["US", "KR"], "horizon": "2026~2027", "vs": ["Vs-공랭-vs-액체냉각"]},
    {"old_sector_id": "DC-02", "old_t_id": "T-12", "new_id": "T3-02", "slug": "데이터센터-액체냉각의-표준화", "title": "데이터센터 액체냉각의 표준화", "sector": "AI 데이터센터 & 전력·냉각 인프라", "sector_id": "T3", "nature": "consensus", "stack_name": "L2 (물리인프라)", "stack_layer": "L2", "geo": ["US", "KR"], "horizon": "2026~2027", "vs": ["Vs-공랭-vs-액체냉각"]},
    {"old_sector_id": "DC-03", "old_t_id": "T-13", "new_id": "T3-03", "slug": "SMR과-데이터센터-무탄소-전력-PPA", "title": "SMR과 데이터센터 무탄소 전력 PPA", "sector": "AI 데이터센터 & 전력·냉각 인프라", "sector_id": "T3", "nature": "consensus", "stack_name": "L2 (물리인프라)", "stack_layer": "L2", "geo": ["US", "KR"], "horizon": "2027~2028", "vs": []},
    {"old_sector_id": "DC-04", "old_t_id": "T-22", "new_id": "T3-04", "slug": "AI-전력망용-대용량-ESS와-LFP-공급망", "title": "AI 전력망용 대용량 ESS와 LFP 공급망", "sector": "AI 데이터센터 & 전력·냉각 인프라", "sector_id": "T3", "nature": "consensus", "stack_name": "L2 (물리인프라)", "stack_layer": "L2", "geo": ["KR", "US", "CN"], "horizon": "2026~2027", "vs": []},
    {"old_sector_id": "DC-05", "old_t_id": "T-23", "new_id": "T3-05", "slug": "변압기-초고압-그리드-쇼티지-장기화", "title": "변압기·초고압 그리드 쇼티지 장기화", "sector": "AI 데이터센터 & 전력·냉각 인프라", "sector_id": "T3", "nature": "consensus", "stack_name": "L2 (물리인프라)", "stack_layer": "L2", "geo": ["KR", "US", "EU"], "horizon": "2026~2028", "vs": []},
    {"old_sector_id": "DC-06", "old_t_id": "T-32", "new_id": "T3-06", "slug": "ESS와-한국배터리의-미국수혜", "title": "ESS와 한국 배터리의 미국 수혜", "sector": "AI 데이터센터 & 전력·냉각 인프라", "sector_id": "T3", "nature": "consensus", "stack_name": "L0 (소재/배터리)", "stack_layer": "L0", "geo": ["KR", "US"], "horizon": "2026~2027", "vs": []},

    # 🏛️ T4 (매크로·자본시장 / Macro & Capital Markets) - 5개
    {"old_sector_id": "MC-01", "old_t_id": "T-05", "new_id": "T4-01", "slug": "금리와-데이터센터", "title": "금리와 데이터센터", "sector": "매크로 자본시장, 금리 & 밸류에이션", "sector_id": "T4", "nature": "contrarian", "stack_name": "L3 (클라우드)", "stack_layer": "L3", "geo": ["US"], "horizon": "2026~2027", "vs": []},
    {"old_sector_id": "MC-02", "old_t_id": "T-08", "new_id": "T4-02", "slug": "엔비디아와-네오클라우드", "title": "엔비디아와 네오클라우드", "sector": "매크로 자본시장, 금리 & 밸류에이션", "sector_id": "T4", "nature": "consensus", "stack_name": "L3 (클라우드)", "stack_layer": "L3", "geo": ["US"], "horizon": "2026~2027", "vs": ["Vs-GPU-vs-TPU-ASIC"]},
    {"old_sector_id": "MC-03", "old_t_id": "T-09", "new_id": "T4-03", "slug": "엔비디아와-GPU-금융", "title": "엔비디아와 GPU 금융", "sector": "매크로 자본시장, 금리 & 밸류에이션", "sector_id": "T4", "nature": "contrarian", "stack_name": "L3 (클라우드)", "stack_layer": "L3", "geo": ["US"], "horizon": "2026~2027", "vs": []},
    {"old_sector_id": "MC-04", "old_t_id": "T-37", "new_id": "T4-04", "slug": "AI-버블-가능성", "title": "AI 버블 가능성", "sector": "매크로 자본시장, 금리 & 밸류에이션", "sector_id": "T4", "nature": "contrarian", "stack_name": "L3 (클라우드)", "stack_layer": "L3", "geo": ["US"], "horizon": "2026~2027", "vs": []},
    {"old_sector_id": "MC-05", "old_t_id": "T-38", "new_id": "T4-05", "slug": "10년금리-5%-재진입-가능성", "title": "10년 금리 5% 재진입 가능성", "sector": "매크로 자본시장, 금리 & 밸류에이션", "sector_id": "T4", "nature": "contrarian", "stack_name": "L6 (매크로)", "stack_layer": "L6", "geo": ["US"], "horizon": "2026~2027", "vs": []},

    # 💻 T5 (SW·에이전트 / Software & Enterprise Agents) - 3개
    {"old_sector_id": "SW-01", "old_t_id": "T-25", "new_id": "T5-01", "slug": "오픈소스-모델-고도화와-온프레미스-사설-AI", "title": "오픈소스 모델 고도화와 온프레미스 사설 AI", "sector": "AI 엔터프라이즈 SW & 버티컬 에이전트", "sector_id": "T5", "nature": "consensus", "stack_name": "L4 (모델/SW)", "stack_layer": "L4", "geo": ["US"], "horizon": "2026~2027", "vs": []},
    {"old_sector_id": "SW-02", "old_t_id": "T-31", "new_id": "T5-02", "slug": "AI-소프트웨어-레이어의-과점화", "title": "AI 소프트웨어 레이어의 과점화", "sector": "AI 엔터프라이즈 SW & 버티컬 에이전트", "sector_id": "T5", "nature": "consensus", "stack_name": "L4 (모델/SW)", "stack_layer": "L4", "geo": ["US"], "horizon": "2026~2027", "vs": []},
    {"old_sector_id": "SW-03", "old_t_id": "T-34", "new_id": "T5-03", "slug": "바이오AI와-신약개발-가속", "title": "바이오 AI와 신약 개발 가속", "sector": "AI 엔터프라이즈 SW & 버티컬 에이전트", "sector_id": "T5", "nature": "consensus", "stack_name": "L4 (모델/SW)", "stack_layer": "L4", "geo": ["US", "KR"], "horizon": "2026~2028", "vs": []},

    # 🌐 T6 (지정학·소버린 / Geopolitics & Sovereign) - 2개
    {"old_sector_id": "GE-01", "old_t_id": "T-26", "new_id": "T6-01", "slug": "소버린-AI와-국가-단위-컴퓨트-인프라", "title": "소버린 AI와 국가 단위 컴퓨트 인프라", "sector": "지정학, 소버린 AI & 공급망 안보", "sector_id": "T6", "nature": "consensus", "stack_name": "L3 (클라우드)", "stack_layer": "L3", "geo": ["Global", "KR", "US"], "horizon": "2026~2028", "vs": []},
    {"old_sector_id": "GE-02", "old_t_id": "T-36", "new_id": "T6-02", "slug": "중국반도체의-HBM-생산가능성", "title": "중국 반도체의 HBM 생산 가능성", "sector": "지정학, 소버린 AI & 공급망 안보", "sector_id": "T6", "nature": "contrarian", "stack_name": "L1 (칩/패키징)", "stack_layer": "L1", "geo": ["CN", "KR"], "horizon": "2026~2027", "vs": []},
]

SECTOR_TO_NEW = {m["old_sector_id"]: m["new_id"] for m in MAPPING}
T_TO_NEW = {m["old_t_id"]: m["new_id"] for m in MAPPING}
OLD_FILE_TO_NEW_FILE = {}
for m in MAPPING:
    OLD_FILE_TO_NEW_FILE[f"{m['old_sector_id']}-{m['slug']}"] = f"{m['new_id']}-{m['slug']}"
    OLD_FILE_TO_NEW_FILE[f"{m['old_t_id']}-{m['slug']}"] = f"{m['new_id']}-{m['slug']}"


def update_obsidian_sync_script():
    """obsidian_sync.py 파일의 필터링 로직 최신화"""
    sync_script = ROOT_DIR / "obsidian_sync.py"
    if sync_script.exists():
        text = sync_script.read_text(encoding="utf-8")
        target = 'for t_file in sorted([f for f in config.THESIS_DIR.glob("*.md") if f.name.startswith(("SC-", "DC-", "RB-", "SW-", "GE-", "MC-", "T-"))]):'
        replacement = 'for t_file in sorted([f for f in config.THESIS_DIR.glob("*.md") if not f.name.startswith(("00-", "Topic-", "Company-", "Vs-"))]):'
        if target in text:
            text = text.replace(target, replacement)
            sync_script.write_text(text, encoding="utf-8")
            print("  🔧 [obsidian_sync.py] 필터링 조건 전면 개방 완료")


def migrate_theses():
    """thesis 디렉터리 내의 38개 파일을 T1-01 ~ T6-02 로 변환"""
    print("\n📂 [1/3] 38개 테제 파일 변환 및 메타데이터 갱신 시작...")

    for m in MAPPING:
        old_sector_id = m["old_sector_id"]
        new_id = m["new_id"]
        slug = m["slug"]
        title = m["title"]
        old_t_id = m["old_t_id"]

        # 기존 파일 찾기
        old_file = THESIS_DIR / f"{old_sector_id}-{slug}.md"
        if not old_file.exists():
            old_file = THESIS_DIR / f"{old_t_id}-{slug}.md"
        
        if not old_file.exists():
            # 이미 변환되었거나 없는 경우 검색
            matches = list(THESIS_DIR.glob(f"*{slug}.md"))
            if matches:
                old_file = matches[0]
            else:
                print(f"  ⚠️ 파일을 찾을 수 없음: {old_sector_id}-{slug}.md")
                continue

        raw_text = old_file.read_text(encoding="utf-8")
        if not raw_text.startswith("---"):
            continue
        parts = raw_text.split("---", 2)
        if len(parts) < 3:
            continue

        meta = yaml.safe_load(parts[1]) or {}
        body = parts[2].lstrip("\r\n")

        # 메타데이터 갱신
        meta["id"] = new_id
        meta["old_id"] = old_t_id
        meta["previous_id"] = old_sector_id
        meta["title"] = title
        meta["sector"] = m["sector"]
        meta["sector_id"] = m["sector_id"]
        meta["thesis_nature"] = m["nature"]
        meta["stack_layer"] = m["stack_layer"]
        meta["stack_name"] = m["stack_name"]
        meta["geography"] = m["geo"]
        meta["time_horizon"] = m["horizon"]
        meta["related_vs"] = m["vs"]

        # Aliases 구성: 신규 ID, 신규 풀네임, 이전 섹터ID, 구 T-ID, 한글제목 모두 등록
        aliases = meta.get("aliases", [])
        for a in [new_id, f"{new_id} {title}", old_sector_id, f"{old_sector_id} {title}", old_t_id, f"{old_t_id} {title}", title]:
            if a not in aliases:
                aliases.append(a)
        meta["aliases"] = aliases

        # related_theses 갱신
        new_rel = []
        for r in meta.get("related_theses", []):
            if r in SECTOR_TO_NEW:
                new_rel.append(SECTOR_TO_NEW[r])
            elif r in T_TO_NEW:
                new_rel.append(T_TO_NEW[r])
            else:
                new_rel.append(r)
        meta["related_theses"] = new_rel

        # 본문 내 링크 및 텍스트 치환
        updated_body = body
        # 1. 파일 링크 치환
        for old_pattern, new_pattern in OLD_FILE_TO_NEW_FILE.items():
            updated_body = updated_body.replace(f"[[{old_pattern}", f"[[{new_pattern}")
        # 2. SC-XX / DC-XX / RB-XX / SW-XX / GE-XX / MC-XX 치환
        for old_sec, n_id in SECTOR_TO_NEW.items():
            updated_body = updated_body.replace(f"# {old_sec} ", f"# {n_id} ")
            updated_body = updated_body.replace(f"|{old_sec} ", f"|{n_id} ")
            updated_body = updated_body.replace(f"|{old_sec}|", f"|{n_id}|")
            updated_body = updated_body.replace(f"|{old_sec}]]", f"|{n_id}]]")
            updated_body = updated_body.replace(f'"{old_sec}"', f'"{n_id}"')
            updated_body = updated_body.replace(f"'{old_sec}'", f"'{n_id}'")
            updated_body = updated_body.replace(f"{old_sec} ", f"{n_id} ")
        
        # Dataview 쿼리 업데이트
        updated_body = updated_body.replace(
            f'contains(thesis, "{old_sector_id}")',
            f'contains(thesis, "{new_id}") OR contains(thesis, "{old_sector_id}") OR contains(thesis, "{old_t_id}")'
        )

        # 새 파일 작성 및 구 파일 삭제
        new_file = THESIS_DIR / f"{new_id}-{slug}.md"
        yaml_str = yaml.dump(meta, allow_unicode=True, sort_keys=False)
        new_file.write_text(f"---\n{yaml_str}---\n\n{updated_body}", encoding="utf-8")
        
        if old_file != new_file and old_file.exists():
            old_file.unlink()

        print(f"  ✅ [전환 완료] {old_sector_id} ({old_t_id}) ➔ {new_id} ({new_file.name})")


def update_all_hubs_and_moc():
    """모든 Topic, Company, Vs Hubs 및 Master MOC 링크 일괄 갱신"""
    print("\n🔄 [2/3] Master MOC 및 모든 Hubs 문서 링크 최신화...")

    for md_file in THESIS_DIR.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        modified = False

        # 1. 파일 링크 치환
        for old_pattern, new_pattern in OLD_FILE_TO_NEW_FILE.items():
            if old_pattern in content:
                content = content.replace(f"[[{old_pattern}", f"[[{new_pattern}")
                modified = True

        # 2. 섹터 ID 치환
        for old_sec, n_id in SECTOR_TO_NEW.items():
            if old_sec in content:
                content = content.replace(f"|{old_sec}]]", f"|{n_id}]]")
                content = content.replace(f"|{old_sec} ", f"|{n_id} ")
                content = content.replace(f"[[{old_sec}|", f"[[{n_id}|")
                content = content.replace(f'"{old_sec}"', f'"{n_id}"')
                content = content.replace(f"'{old_sec}'", f"'{n_id}'")
                content = content.replace(f"# {old_sec} ", f"# {n_id} ")
                modified = True

        if modified:
            md_file.write_text(content, encoding="utf-8")
            print(f"  📝 [허브 최신화] {md_file.name}")


def sync_and_clean_vault():
    """옵시디언 볼트 동기화 및 구 파일 정리"""
    print("\n📂 [3/3] 옵시디언 볼트 동기화 및 기존 구 파일 정리...")
    vault_theses = VAULT / "argus" / "Theses"
    if vault_theses.exists():
        for old_pattern in ["SC-*.md", "DC-*.md", "RB-*.md", "SW-*.md", "GE-*.md", "MC-*.md", "T-*.md"]:
            for old_f in vault_theses.glob(old_pattern):
                old_f.unlink()

    from obsidian_sync import sync_all_outputs
    sync_all_outputs()
    print("  🎉 옵시디언 볼트 완전 동기화 완료!")


if __name__ == "__main__":
    print("🚀 [Argus Pulse] T1-01 ~ T6-02 번호체계 마이그레이션 시작\n")
    update_obsidian_sync_script()
    migrate_theses()
    update_all_hubs_and_moc()
    sync_and_clean_vault()
    print("\n✨ 모든 테제가 갯수 순서(T1~T6)의 T1-01 ~ T6-02 번호체계로 성공적으로 전환되었습니다!")
