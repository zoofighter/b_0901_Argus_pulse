"""
scripts/apply_cross_cutting_dimensions.py
38개 전체 테제에 5대 교차 차원 메타데이터를 일괄 적용하고,
4대 대결 허브(Vs-Hubs) 및 확장 Master MOC를 생성하여 옵시디언 볼트로 동기화.
"""

import sys
import shutil
import unicodedata
from pathlib import Path
import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
THESIS_DIR = ROOT_DIR / "thesis"
DOCS_DIR = ROOT_DIR / "docs"

import config
VAULT = config.OBSIDIAN_PATH

# ── 38개 테제 교차 차원 전체 매핑 데이터 ──────────────────────────────────────────
DIMENSIONS_DATA = {
    "T-01": {"sector": "⚡ AI 데이터센터 & 전력·냉각 인프라", "sector_id": "S2", "nature": "consensus", "stack": "L2 (물리인프라)", "stack_id": "L2", "geo": ["US", "KR"], "horizon": "2026~2027", "vs": ["Vs-공랭-vs-액체냉각"]},
    "T-02": {"sector": "💾 AI 컴퓨트 & 차세대 반도체", "sector_id": "S1", "nature": "consensus", "stack": "L1 (칩/패키징)", "stack_id": "L1", "geo": ["KR", "US", "TW"], "horizon": "2026~2027", "vs": ["Vs-TSMC동맹-vs-삼성턴키"]},
    "T-03": {"sector": "🤖 피지컬 AI, 모빌리티 & 로보틱스", "sector_id": "S3", "nature": "consensus", "stack": "L0 (소재/배터리)", "stack_id": "L0", "geo": ["KR", "JP", "US"], "horizon": "2026H2~2028", "vs": []},
    "T-04": {"sector": "🤖 피지컬 AI, 모빌리티 & 로보틱스", "sector_id": "S3", "nature": "consensus", "stack": "L5 (디바이스)", "stack_id": "L5", "geo": ["US", "KR"], "horizon": "2026~2027", "vs": []},
    "T-05": {"sector": "🏛️ 매크로 자본시장, 금리 & 밸류에이션", "sector_id": "S6", "nature": "contrarian", "stack": "L3 (클라우드)", "stack_id": "L3", "geo": ["US"], "horizon": "2026~2027", "vs": []},
    "T-06": {"sector": "💾 AI 컴퓨트 & 차세대 반도체", "sector_id": "S1", "nature": "contrarian", "stack": "L1 (칩/패키징)", "stack_id": "L1", "geo": ["US", "TW"], "horizon": "2026~2027", "vs": ["Vs-GPU-vs-TPU-ASIC"]},
    "T-07": {"sector": "💾 AI 컴퓨트 & 차세대 반도체", "sector_id": "S1", "nature": "consensus", "stack": "L1 (칩/패키징)", "stack_id": "L1", "geo": ["KR", "US"], "horizon": "2026H2~2027", "vs": []},
    "T-08": {"sector": "🏛️ 매크로 자본시장, 금리 & 밸류에이션", "sector_id": "S6", "nature": "consensus", "stack": "L3 (클라우드)", "stack_id": "L3", "geo": ["US"], "horizon": "2026~2027", "vs": ["Vs-GPU-vs-TPU-ASIC"]},
    "T-09": {"sector": "🏛️ 매크로 자본시장, 금리 & 밸류에이션", "sector_id": "S6", "nature": "contrarian", "stack": "L3 (클라우드)", "stack_id": "L3", "geo": ["US"], "horizon": "2026~2027", "vs": []},
    "T-10": {"sector": "💾 AI 컴퓨트 & 차세대 반도체", "sector_id": "S1", "nature": "consensus", "stack": "L1 (칩/패키징)", "stack_id": "L1", "geo": ["TW", "KR", "US"], "horizon": "2026~2027", "vs": ["Vs-TSMC동맹-vs-삼성턴키"]},
    "T-11": {"sector": "💾 AI 컴퓨트 & 차세대 반도체", "sector_id": "S1", "nature": "consensus", "stack": "L0 (소부장/기판)", "stack_id": "L0", "geo": ["KR", "US"], "horizon": "2027~2028", "vs": []},
    "T-12": {"sector": "⚡ AI 데이터센터 & 전력·냉각 인프라", "sector_id": "S2", "nature": "consensus", "stack": "L2 (물리인프라)", "stack_id": "L2", "geo": ["US", "KR"], "horizon": "2026~2027", "vs": ["Vs-공랭-vs-액체냉각"]},
    "T-13": {"sector": "⚡ AI 데이터센터 & 전력·냉각 인프라", "sector_id": "S2", "nature": "consensus", "stack": "L2 (물리인프라)", "stack_id": "L2", "geo": ["US", "KR"], "horizon": "2027~2028", "vs": []},
    "T-14": {"sector": "💾 AI 컴퓨트 & 차세대 반도체", "sector_id": "S1", "nature": "consensus", "stack": "L3 (네트워킹)", "stack_id": "L3", "geo": ["US", "TW"], "horizon": "2027~2028", "vs": ["Vs-인피니밴드-vs-울트라이더넷"]},
    "T-15": {"sector": "💾 AI 컴퓨트 & 차세대 반도체", "sector_id": "S1", "nature": "consensus", "stack": "L1 (칩/패키징)", "stack_id": "L1", "geo": ["US", "KR"], "horizon": "2026~2027", "vs": ["Vs-GPU-vs-TPU-ASIC"]},
    "T-16": {"sector": "💾 AI 컴퓨트 & 차세대 반도체", "sector_id": "S1", "nature": "consensus", "stack": "L1 (칩/패키징)", "stack_id": "L1", "geo": ["TW", "KR", "US"], "horizon": "2026H2~2027", "vs": ["Vs-TSMC동맹-vs-삼성턴키"]},
    "T-17": {"sector": "🤖 피지컬 AI, 모빌리티 & 로보틱스", "sector_id": "S3", "nature": "consensus", "stack": "L5 (디바이스)", "stack_id": "L5", "geo": ["US", "KR"], "horizon": "2027~2029", "vs": []},
    "T-18": {"sector": "🤖 피지컬 AI, 모빌리티 & 로보틱스", "sector_id": "S3", "nature": "consensus", "stack": "L5 (디바이스)", "stack_id": "L5", "geo": ["US", "KR"], "horizon": "2026~2027", "vs": []},
    "T-19": {"sector": "🤖 피지컬 AI, 모빌리티 & 로보틱스", "sector_id": "S3", "nature": "consensus", "stack": "L1 (칩/패키징)", "stack_id": "L1", "geo": ["US", "JP"], "horizon": "2026~2028", "vs": []},
    "T-20": {"sector": "🤖 피지컬 AI, 모빌리티 & 로보틱스", "sector_id": "S3", "nature": "consensus", "stack": "L5 (디바이스)", "stack_id": "L5", "geo": ["US", "KR"], "horizon": "2026~2027", "vs": []},
    "T-21": {"sector": "🤖 피지컬 AI, 모빌리티 & 로보틱스", "sector_id": "S3", "nature": "consensus", "stack": "L5 (디바이스)", "stack_id": "L5", "geo": ["US"], "horizon": "2026~2027", "vs": []},
    "T-22": {"sector": "⚡ AI 데이터센터 & 전력·냉각 인프라", "sector_id": "S2", "nature": "consensus", "stack": "L2 (물리인프라)", "stack_id": "L2", "geo": ["KR", "US", "CN"], "horizon": "2026~2027", "vs": []},
    "T-23": {"sector": "⚡ AI 데이터센터 & 전력·냉각 인프라", "sector_id": "S2", "nature": "consensus", "stack": "L2 (물리인프라)", "stack_id": "L2", "geo": ["KR", "US", "EU"], "horizon": "2026~2028", "vs": []},
    "T-24": {"sector": "💾 AI 컴퓨트 & 차세대 반도체", "sector_id": "S1", "nature": "consensus", "stack": "L1 (칩/패키징)", "stack_id": "L1", "geo": ["US", "KR", "TW"], "horizon": "2026~2027", "vs": ["Vs-GPU-vs-TPU-ASIC"]},
    "T-25": {"sector": "💻 AI 엔터프라이즈 SW & 버티컬 에이전트", "sector_id": "S4", "nature": "consensus", "stack": "L4 (모델/SW)", "stack_id": "L4", "geo": ["US"], "horizon": "2026~2027", "vs": []},
    "T-26": {"sector": "🌐 지정학, 소버린 AI & 공급망 안보", "sector_id": "S5", "nature": "consensus", "stack": "L3 (클라우드)", "stack_id": "L3", "geo": ["Global", "KR", "US"], "horizon": "2026~2028", "vs": []},
    "T-27": {"sector": "🤖 피지컬 AI, 모빌리티 & 로보틱스", "sector_id": "S3", "nature": "consensus", "stack": "L5 (디바이스)", "stack_id": "L5", "geo": ["US", "KR"], "horizon": "2026~2027", "vs": []},
    "T-28": {"sector": "💾 AI 컴퓨트 & 차세대 반도체", "sector_id": "S1", "nature": "consensus", "stack": "L1 (칩/패키징)", "stack_id": "L1", "geo": ["KR", "US"], "horizon": "2027~2029", "vs": []},
    "T-29": {"sector": "💾 AI 컴퓨트 & 차세대 반도체", "sector_id": "S1", "nature": "consensus", "stack": "L3 (네트워킹)", "stack_id": "L3", "geo": ["US"], "horizon": "2026~2027", "vs": ["Vs-인피니밴드-vs-울트라이더넷"]},
    "T-30": {"sector": "🤖 피지컬 AI, 모빌리티 & 로보틱스", "sector_id": "S3", "nature": "consensus", "stack": "L5 (디바이스)", "stack_id": "L5", "geo": ["KR", "US"], "horizon": "2026~2028", "vs": []},
    "T-31": {"sector": "💻 AI 엔터프라이즈 SW & 버티컬 에이전트", "sector_id": "S4", "nature": "consensus", "stack": "L4 (모델/SW)", "stack_id": "L4", "geo": ["US"], "horizon": "2026~2027", "vs": []},
    "T-32": {"sector": "⚡ AI 데이터센터 & 전력·냉각 인프라", "sector_id": "S2", "nature": "consensus", "stack": "L0 (소재/배터리)", "stack_id": "L0", "geo": ["KR", "US"], "horizon": "2026~2027", "vs": []},
    "T-33": {"sector": "💾 AI 컴퓨트 & 차세대 반도체", "sector_id": "S1", "nature": "consensus", "stack": "L0 (소부장)", "stack_id": "L0", "geo": ["KR"], "horizon": "2026~2027", "vs": []},
    "T-34": {"sector": "💻 AI 엔터프라이즈 SW & 버티컬 에이전트", "sector_id": "S4", "nature": "consensus", "stack": "L4 (모델/SW)", "stack_id": "L4", "geo": ["US", "KR"], "horizon": "2026~2028", "vs": []},
    "T-35": {"sector": "💾 AI 컴퓨트 & 차세대 반도체", "sector_id": "S1", "nature": "contrarian", "stack": "L1 (칩/패키징)", "stack_id": "L1", "geo": ["KR", "US"], "horizon": "2027H2~2028", "vs": []},
    "T-36": {"sector": "🌐 지정학, 소버린 AI & 공급망 안보", "sector_id": "S5", "nature": "contrarian", "stack": "L1 (칩/패키징)", "stack_id": "L1", "geo": ["CN", "KR"], "horizon": "2026~2027", "vs": []},
    "T-37": {"sector": "🏛️ 매크로 자본시장, 금리 & 밸류에이션", "sector_id": "S6", "nature": "contrarian", "stack": "L3 (클라우드)", "stack_id": "L3", "geo": ["US"], "horizon": "2026~2027", "vs": []},
    "T-38": {"sector": "🏛️ 매크로 자본시장, 금리 & 밸류에이션", "sector_id": "S6", "nature": "contrarian", "stack": "L6 (매크로)", "stack_id": "L6", "geo": ["US"], "horizon": "2026~2027", "vs": []},
}

# ── 4대 대결 허브(Vs-Hubs) 데이터 ────────────────────────────────────────────────
VS_HUBS = {
    "Vs-GPU-vs-TPU-ASIC": {
        "title": "범용 GPU (NVIDIA) vs 커스텀 ASIC (빅테크 자체 칩)",
        "aliases": ["GPU vs ASIC", "GPU vs TPU", "엔비디아 vs 빅테크 자체칩"],
        "desc": "엔비디아 CUDA 생태계 중심의 범용 GPU 아키텍처와 구글 TPU, 메타 MTIA, AWS Trainium/Inferentia 등 TCO 절감 및 추론 최적화를 위한 빅테크 커스텀 가속기 간의 제로섬 수주전.",
        "theses": ["T-06", "T-08", "T-15", "T-24"],
        "companies": ["NVIDIA", "Broadcom", "Alphabet", "Marvell", "CoreWeave"],
        "key_conflict": "유연성과 소프트웨어 해자(CUDA) vs 전력 대역폭 효율과 단가(TCO)의 격돌",
    },
    "Vs-TSMC동맹-vs-삼성턴키": {
        "title": "TSMC 동맹 (SK하이닉스-TSMC) vs 삼성전자 턴키 (원팀)",
        "aliases": ["TSMC 연합 vs 삼성 턴키", "SK-TSMC vs 삼성", "분리형 vs 수직계열화"],
        "desc": "SK하이닉스(메모리)-TSMC(선단 로직 & CoWoS)-엔비디아로 이어지는 분리형 삼각편대와, 메모리+파운드리+어드밴스드 패키징을 일괄 제공하는 삼성전자의 CUBE 턴키 모델 간의 서플라이체인 표준 경쟁.",
        "theses": ["T-02", "T-10", "T-16"],
        "companies": ["SK하이닉스", "TSMC", "삼성전자", "NVIDIA", "한미반도체"],
        "key_conflict": "검증된 CoWoS 생태계와 락인 vs 일괄 공급에 따른 리드타임 단축 및 단가 우위",
    },
    "Vs-공랭-vs-액체냉각": {
        "title": "레거시 공랭식 (Air Cooling) vs 직접액체냉각 (DLC & CDU)",
        "aliases": ["공랭 vs 액랭", "Air vs Liquid Cooling", "데이터센터 냉각 표준"],
        "desc": "랙당 40kW 이하 전통적 팬 공랭식 냉각과 블랙웰 GB200(랙당 120kW+) 시대를 맞아 PUE 1.1을 달성하기 위한 CDU 및 DLC(Direct Liquid Cooling) 직접 액체냉각 간의 인프라 전환 격돌.",
        "theses": ["T-01", "T-12"],
        "companies": ["Vertiv", "Supermicro", "Schneider", "CoolIT"],
        "key_conflict": "기존 레거시 설비의 감가상각 유지 vs 고밀도 연산 칩셋의 물리적 발열 임계 돌파",
    },
    "Vs-인피니밴드-vs-울트라이더넷": {
        "title": "인피니밴드 (NVIDIA 독점) vs 울트라 이더넷 (UEC 연합)",
        "aliases": ["InfiniBand vs UEC", "인피니밴드 vs 이더넷", "초고속 AI 네트워킹"],
        "desc": "초저지연과 무손실 패킷 전송을 무기로 엔비디아가 장악한 인피니밴드 독점망과, 브로드컴·아리스타·시스코·메타 중심의 개방형 표준 울트라 이더넷(UEC) 간의 데이터센터 스케일아웃 네트워크 주도권 경쟁.",
        "theses": ["T-14", "T-29"],
        "companies": ["NVIDIA", "Arista Networks", "Broadcom", "Cisco", "Marvell"],
        "key_conflict": "독점 폐쇄망의 최고 성능 vs 개방형 표준망의 확장성 및 원가 절감",
    },
}


def apply_dimensions_to_all_theses():
    """38개 테제 프론트매터에 5대 교차 차원 메타데이터 일괄 적용"""
    for p in sorted(THESIS_DIR.glob("T-*.md")):
        text = p.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue

        parts = text.split("---", 2)
        if len(parts) < 3:
            continue

        meta = yaml.safe_load(parts[1]) or {}
        body = parts[2].lstrip("\r\n")
        tid = meta.get("id")

        if tid in DIMENSIONS_DATA:
            d = DIMENSIONS_DATA[tid]
            meta["sector"] = d["sector"]
            meta["sector_id"] = d["sector_id"]
            meta["thesis_nature"] = d["nature"]
            meta["stack_layer"] = d["stack_id"]
            meta["stack_name"] = d["stack"]
            meta["geography"] = d["geo"]
            meta["time_horizon"] = d["horizon"]
            meta["related_vs"] = d["vs"]

            # 뱃지 스트립 생성 (본문 상단에 삽입)
            nature_badge = "🚀 주류 성장 (Consensus)" if d["nature"] == "consensus" else "🛡️ 역발상/헷지 (Contrarian)"
            geo_badges = ", ".join([f"`{g}`" for g in d["geo"]])
            vs_links = ", ".join([f"[[{v}|{v.replace('Vs-', '')}]]" for v in d["vs"]]) if d["vs"] else "해당 없음"

            badge_block = f"""> 🏷️ **교차 분석 메타데이터**:
> - **성격**: `{nature_badge}` | **스택**: `{d['stack']}` | **시계**: `{d['horizon']}`
> - **공급망 권역**: {geo_badges} | **핵심 대결 구도**: {vs_links}
"""

            # 본문 내 기존 상위 인덱스 바로 아래에 뱃지 블록 업데이트
            if "> 🧭 **상위 인덱스**:" in body:
                body_parts = body.split("---", 1)
                header_part = body_parts[0]
                rest_part = body_parts[1] if len(body_parts) > 1 else ""

                # 기존 뱃지 블록 제거 후 재구성
                new_header = header_part.split("> 🏷️ **교차 분석")[0].strip()
                body = f"{new_header}\n\n{badge_block}\n---{rest_part}"

        yaml_str = yaml.dump(meta, allow_unicode=True, sort_keys=False)
        p.write_text(f"---\n{yaml_str}---\n\n{body}", encoding="utf-8")
        print(f"  🏷️ [교차 차원 메타데이터 적용] {tid} ({meta.get('thesis_nature')}, {meta.get('stack_layer')})")


def build_vs_hubs():
    """4대 대결 허브(Vs-Hubs) MD 파일 생성"""
    for key, data in VS_HUBS.items():
        aliases_yaml = "\n".join([f"  - {a}" for a in data["aliases"]])
        theses_links = []
        for tid in data["theses"]:
            fname = f"{tid}.md"
            for p in THESIS_DIR.glob(f"{tid}-*.md"):
                fname = p.name
                break
            theses_links.append(f"- [[{fname.replace('.md', '')}|{tid}]]")
        theses_str = "\n".join(theses_links)
        comp_links = ", ".join([f"[[Company-{c}|{c}]]" for c in data["companies"]])

        content = f"""---
aliases:
{aliases_yaml}
type: vs_hub
category: 제로섬 대결 & 트레이드오프
created: 2026-09-06
---

# ⚔️ {data['title']}

> 🧭 **상위 인덱스**: [[00-Argus-Master-MOC|Master MOC]] ➔ [[00-Argus-Master-MOC#⚔️-핵심-기술--진영-대결-구도-versus-hubs|대결 허브]]

---

## 📌 대결 구도 개요 및 핵심 쟁점
{data['desc']}

> ⚡ **핵심 충돌 지점**:  
> **{data['key_conflict']}**

---

## 🔗 관련 투자 테제군 (Theses Network)
{theses_str}

---

## 🏢 대결 진영별 핵심 기업 (Players)
- **주요 플레이어**: {comp_links}

---

## 📑 관련 분석 리포트 및 블로그 (Dataview)

```dataview
TABLE file.mtime AS "작성일", title AS "제목", tags AS "태그"
FROM "argus" OR "output"
WHERE contains(file.text, "{data['aliases'][0]}") OR contains(file.outlinks, this.file.link)
SORT file.mtime DESC
LIMIT 8
```
"""
        target = THESIS_DIR / f"{key}.md"
        target.write_text(content, encoding="utf-8")
        print(f"  ⚔️ [Vs Hub 생성] {key}.md")


def update_master_moc():
    """00-Argus-Master-MOC.md를 6대 섹터 및 다차원 대시보드를 포함하도록 전면 고도화"""
    content = """---
title: "Argus Pulse 투자 테제 Master MOC"
type: moc
created: 2026-09-06
updated: 2026-09-06
tags:
  - moc
  - argus-pulse
  - investment-thesis
  - multi-dimensional-dashboard
---

# 🧭 Argus Pulse 투자 테제 Master MOC (Map of Content)

> **Argus Nexus 중앙 사령탑**  
> AI 및 첨단 기술 산업의 구조적 변화를 추적하는 38개 투자 가설(Theses)의 상호 인과관계 맵과 **6대 섹터 & 5대 교차 차원(다차원 대시보드)** 사령탑입니다.

---

## 🗺️ 전체 가설 생태계 가치사슬 구조도 (Macro Value Chain)

```mermaid
flowchart TB
    subgraph Macro["🏛️ 매크로 자본시장 & 밸류에이션 (S6)"]
        T05["[[T-05-금리와-데이터센터|T-05 금리와 DC ROI]]"]
        T08["[[T-08-엔비디아와-네오클라우드|T-08 네오클라우드]]"]
        T09["[[T-09-엔비디아와-GPU-금융|T-09 GPU 금융]]"]
        T37["[[T-37-AI-버블-가능성|T-37 AI 버블 붕괴 리스크]]"]
        T38["[[T-38-10년금리-5%-재진입-가능성|T-38 10년 금리 5%]]"]
    end

    subgraph PowerInfra["⚡ AI 인프라 & 전력·냉각 (S2)"]
        T01["[[T-01-데이터센터의-변화|T-01 데이터센터 병목]]"]
        T12["[[T-12-데이터센터-액체냉각의-표준화|T-12 액체냉각 표준화]]"]
        T13["[[T-13-SMR과-데이터센터-무탄소-전력-PPA|T-13 SMR·무탄소 PPA]]"]
        T22["[[T-22-AI-전력망용-대용량-ESS와-LFP-공급망|T-22 대용량 ESS/LFP]]"]
        T23["[[T-23-변압기·초고압-그리드-쇼티지-장기화|T-23 변압기·그리드]]"]
        T32["[[T-32-ESS와-한국배터리의-미국수혜|T-32 K-배터리 미국수혜]]"]
    end

    subgraph ComputeMemory["💾 AI 컴퓨트 & 차세대 반도체 (S1)"]
        T02["[[T-02-메모리-산업의-변화|T-02 HBM4 ASIC화]]"]
        T06["[[T-06-TPU-증가와-GPU-수요-둔화|T-06 TPU vs GPU]]"]
        T07["[[T-07-CXL-메모리의-확대|T-07 CXL 메모리 풀링]]"]
        T10["[[T-10-첨단-패키징과-CoWoS의-병목|T-10 CoWoS 패키징]]"]
        T11["[[T-11-유리기판의-차세대-패키징-침투|T-11 유리기판 인터포저]]"]
        T14["[[T-14-실리콘-포토닉스와-CPO의-상용화|T-14 CPO 광반도체]]"]
        T15["[[T-15-AI-추론-시장-폭발과-LPU-ASIC-분화|T-15 추론 LPU·ASIC]]"]
        T16["[[T-16-파운드리-2nm-공정과-GAA-격돌|T-16 파운드리 2nm GAA]]"]
        T24["[[T-24-빅테크-커스텀-ASIC-증가와-DSP-생태계|T-24 빅테크 ASIC/DSP]]"]
        T28["[[T-28-3D-DRAM-기술-전환과-400단-V-NAND|T-28 3D DRAM & V-NAND]]"]
        T29["[[T-29-초고속-AI-네트워킹-UEC-vs-인피니밴드|T-29 UEC vs 인피니밴드]]"]
        T33["[[T-33-반도체-소부장의-내재화|T-33 반도체 소부장]]"]
        T35["[[T-35-메모리-2028년-피크아웃|T-35 2028 메모리 피크아웃]]"]
    end

    subgraph SoftwareAgents["💻 AI 엔터프라이즈 SW & 에이전트 (S4)"]
        T25["[[T-25-오픈소스-모델-고도화와-온프레미스-사설-AI|T-25 사설 AI / 온프레미스]]"]
        T31["[[T-31-AI-소프트웨어-레이어의-과점화|T-31 AI SW 레이어 과점]]"]
        T34["[[T-34-바이오AI와-신약개발-가속|T-34 바이오 AI 신약]]"]
    end

    subgraph Geopolitics["🌐 지정학, 소버린 AI & 공급망 안보 (S5)"]
        T26["[[T-26-소버린-AI와-국가-단위-컴퓨트-인프라|T-26 소버린 AI]]"]
        T36["[[T-36-중국반도체의-HBM-생산가능성|T-36 중국 HBM 추격]]"]
    end

    subgraph EdgePhysical["🤖 피지컬 AI, 모빌리티 & 로보틱스 (S3)"]
        T03["[[T-03-전고체-배터리의-변화|T-03 전고체 배터리]]"]
        T04["[[T-04-온디바이스-AI의-변화|T-04 온디바이스 NPU]]"]
        T17["[[T-17-휴머노이드-로봇과-액추에이터-공급망|T-17 휴머노이드 로봇]]"]
        T18["[[T-18-End-to-End-AI-자율주행과-로보택시|T-18 E2E 자율주행]]"]
        T19["[[T-19-피지컬-AI와-공간지능-반도체|T-19 피지컬 AI 공간지능]]"]
        T20["[[T-20-행동형-AI-에이전트와-모바일-교체-슈퍼사이클|T-20 모바일 교체 사이클]]"]
        T21["[[T-21-AI-PC-보급-확대와-Arm-기반-윈도우-생태계|T-21 AI PC & Arm]]"]
        T27["[[T-27-AI-스마트-글래스와-경량-AR-광학계|T-27 AI 스마트 글래스]]"]
        T30["[[T-30-피지컬AI와-로봇의-상용화|T-30 로봇 상용화]]"]
    end

    Macro --> PowerInfra
    PowerInfra --> ComputeMemory
    ComputeMemory --> SoftwareAgents
    ComputeMemory --> EdgePhysical
    Geopolitics -. 규제/통제 .-> ComputeMemory
    Geopolitics -. 인프라투자 .-> PowerInfra
```

---

## 🔀 다차원 교차 분석 대시보드 (Multi-Dimensional Dashboards)

### 🛡️ 1. 컨센서스 vs 역발상/헷지 뷰 (Consensus vs Contrarian)
> 시장 과열 국면에서 리스크를 헷지하고 포트폴리오를 방어할 수 있는 **역발상(Contrarian) 가설 7종** 전용 모니터링 테이블입니다.

```dataview
TABLE hypothesis AS "핵심 가설", sector AS "섹터", confidence AS "신뢰도", momentum AS "모멘텀"
FROM "argus/Theses"
WHERE thesis_nature = "contrarian"
SORT momentum DESC
```

---

### 🧱 2. 6계층 밸류체인 수직 스택 뷰 (Value Chain Stack L0~L5)
> 원자재(L0) ➔ 칩(L1) ➔ 전력/인프라(L2) ➔ 클라우드(L3) ➔ 소프트웨어(L4) ➔ 디바이스(L5) 순으로 정렬된 수직 파이프라인 뷰입니다.

```dataview
TABLE stack_name AS "스택 레이어", title AS "가설 제목", related_companies AS "핵심 기업"
FROM "argus/Theses"
SORT stack_layer ASC, rank ASC
```

---

### 🗺️ 3. 한국(KR) 핵심 수혜 및 공급망 뷰 (Korea Alpha View)
```dataview
TABLE title AS "가설 제목", hypothesis AS "핵심 가설", momentum AS "모멘텀", rank AS "순위"
FROM "argus/Theses"
WHERE contains(geography, "KR")
SORT momentum DESC
LIMIT 10
```

---

## ⚔️ 핵심 기술 & 진영 대결 구도 (Versus Hubs)

- **[[Vs-GPU-vs-TPU-ASIC|⚔️ 범용 GPU (NVIDIA) vs 커스텀 ASIC (빅테크 자체 칩)]]**: `T-06`, `T-08`, `T-15`, `T-24`
- **[[Vs-TSMC동맹-vs-삼성턴키|⚔️ TSMC 동맹 (SK-TSMC) vs 삼성전자 턴키 (원팀)]]**: `T-02`, `T-10`, `T-16`
- **[[Vs-공랭-vs-액체냉각|⚔️ 레거시 공랭식 vs 직접액체냉각 (DLC & CDU)]]**: `T-01`, `T-12`
- **[[Vs-인피니밴드-vs-울트라이더넷|⚔️ 인피니밴드 (NVIDIA) vs 울트라 이더넷 (UEC 연합)]]**: `T-14`, `T-29`

---

## 📂 6대 섹터별 테제 인덱스

### 1. 💾 AI 컴퓨트 & 차세대 반도체 (Sector 1)
| ID | 가설 제목 | 스택 | 성격 | 핵심 기업 | 주요 연관 테제 |
|:---|:---|:---:|:---:|:---|:---|
| **[[T-02-메모리-산업의-변화\|T-02]]** | 메모리 산업의 변화 | `L1` | `🚀 주류` | `[[Company-SK하이닉스\|SK하이닉스]]`, `[[Company-삼성전자\|삼성전자]]` | `[[T-07-CXL-메모리의-확대\|T-07]]`, `[[T-10-첨단-패키징과-CoWoS의-병목\|T-10]]`, `[[T-35-메모리-2028년-피크아웃\|T-35]]` |
| **[[T-06-TPU-증가와-GPU-수요-둔화\|T-06]]** | TPU 증가와 GPU 수요 둔화 | `L1` | `🛡️ 헷지` | `[[Company-Alphabet\|Alphabet]]`, `[[Company-Broadcom\|Broadcom]]` | `[[T-08-엔비디아와-네오클라우드\|T-08]]`, `[[T-15-AI-추론-시장-폭발과-LPU-ASIC-분화\|T-15]]`, `[[T-24-빅테크-커스텀-ASIC-증가와-DSP-생태계\|T-24]]` |
| **[[T-07-CXL-메모리의-확대\|T-07]]** | CXL 메모리의 확대 | `L1` | `🚀 주류` | `[[Company-삼성전자\|삼성전자]]`, `[[Company-SK하이닉스\|SK하이닉스]]` | `[[T-02-메모리-산업의-변화\|T-02]]`, `[[T-28-3D-DRAM-기술-전환과-400단-V-NAND\|T-28]]` |
| **[[T-10-첨단-패키징과-CoWoS의-병목\|T-10]]** | 첨단 패키징과 CoWoS의 병목 | `L1` | `🚀 주류` | `[[Company-TSMC\|TSMC]]`, `[[Company-SK하이닉스\|SK하이닉스]]` | `[[T-01-데이터센터의-변화\|T-01]]`, `[[T-02-메모리-산업의-변화\|T-02]]`, `[[T-11-유리기판의-차세대-패키징-침투\|T-11]]` |
| **[[T-11-유리기판의-차세대-패키징-침투\|T-11]]** | 유리기판의 차세대 패키징 침투 | `L0` | `🚀 주류` | `[[Company-SKC\|SKC]]`, `[[Company-인텔\|인텔]]` | `[[T-10-첨단-패키징과-CoWoS의-병목\|T-10]]`, `[[T-02-메모리-산업의-변화\|T-02]]` |
| **[[T-14-실리콘-포토닉스와-CPO의-상용화\|T-14]]** | 실리콘 포토닉스와 CPO의 상용화 | `L3` | `🚀 주류` | `[[Company-Broadcom\|Broadcom]]`, `[[Company-TSMC\|TSMC]]` | `[[T-01-데이터센터의-변화\|T-01]]`, `[[T-29-초고속-AI-네트워킹-UEC-vs-인피니밴드\|T-29]]` |
| **[[T-15-AI-추론-시장-폭발과-LPU-ASIC-분화\|T-15]]** | AI 추론 시장 폭발과 LPU·ASIC | `L1` | `🚀 주류` | `[[Company-Groq\|Groq]]`, `[[Company-Qualcomm\|Qualcomm]]` | `[[T-06-TPU-증가와-GPU-수요-둔화\|T-06]]`, `[[T-24-빅테크-커스텀-ASIC-증가와-DSP-생태계\|T-24]]` |
| **[[T-16-파운드리-2nm-공정과-GAA-격돌\|T-16]]** | 파운드리 2nm 공정과 GAA 격돌 | `L1` | `🚀 주류` | `[[Company-TSMC\|TSMC]]`, `[[Company-삼성전자\|삼성전자]]` | `[[T-02-메모리-산업의-변화\|T-02]]`, `[[T-10-첨단-패키징과-CoWoS의-병목\|T-10]]` |
| **[[T-24-빅테크-커스텀-ASIC-증가와-DSP-생태계\|T-24]]** | 빅테크 커스텀 ASIC 증가와 DSP | `L1` | `🚀 주류` | `[[Company-Broadcom\|Broadcom]]`, `[[Company-TSMC\|TSMC]]` | `[[T-06-TPU-증가와-GPU-수요-둔화\|T-06]]`, `[[T-15-AI-추론-시장-폭발과-LPU-ASIC-분화\|T-15]]` |
| **[[T-28-3D-DRAM-기술-전환과-400단-V-NAND\|T-28]]** | 3D DRAM 기술 전환과 400단 V-NAND | `L1` | `🚀 주류` | `[[Company-SK하이닉스\|SK하이닉스]]`, `[[Company-삼성전자\|삼성전자]]` | `[[T-02-메모리-산업의-변화\|T-02]]`, `[[T-07-CXL-메모리의-확대\|T-07]]` |
| **[[T-29-초고속-AI-네트워킹-UEC-vs-인피니밴드\|T-29]]** | 초고속 AI 네트워킹 UEC vs 인피니밴드 | `L3` | `🚀 주류` | `[[Company-Arista\|Arista]]`, `[[Company-NVIDIA\|NVIDIA]]` | `[[T-01-데이터센터의-변화\|T-01]]`, `[[T-14-실리콘-포토닉스와-CPO의-상용화\|T-14]]` |
| **[[T-33-반도체-소부장의-내재화\|T-33]]** | 반도체 소부장의 내재화 | `L0` | `🚀 주류` | `[[Company-한미반도체\|한미반도체]]`, `[[Company-동진쎄미켐\|동진쎄미켐]]` | `[[T-01-데이터센터의-변화\|T-01]]`, `[[T-02-메모리-산업의-변화\|T-02]]` |
| **[[T-35-메모리-2028년-피크아웃\|T-35]]** | 메모리 2028년 피크아웃 논쟁 | `L1` | `🛡️ 헷지` | `[[Company-SK하이닉스\|SK하이닉스]]`, `[[Company-삼성전자\|삼성전자]]` | `[[T-02-메모리-산업의-변화\|T-02]]`, `[[T-06-TPU-증가와-GPU-수요-둔화\|T-06]]` |

### 2. ⚡ AI 데이터센터 & 전력·냉각 인프라 (Sector 2)
| ID | 가설 제목 | 스택 | 성격 | 핵심 기업 | 주요 연관 테제 |
|:---|:---|:---:|:---:|:---|:---|
| **[[T-01-데이터센터의-변화\|T-01]]** | 데이터센터의 변화 (전력·냉각 병목) | `L2` | `🚀 주류` | `[[Company-Vertiv\|Vertiv]]`, `[[Company-HD현대일렉트릭\|HD현대일렉트릭]]` | `[[T-05-금리와-데이터센터\|T-05]]`, `[[T-12-데이터센터-액체냉각의-표준화\|T-12]]`, `[[T-23-변압기·초고압-그리드-쇼티지-장기화\|T-23]]` |
| **[[T-12-데이터센터-액체냉각의-표준화\|T-12]]** | 데이터센터 액체냉각의 표준화 | `L2` | `🚀 주류` | `[[Company-Vertiv\|Vertiv]]`, `[[Company-Supermicro\|Supermicro]]` | `[[T-01-데이터센터의-변화\|T-01]]`, `[[T-05-금리와-데이터센터\|T-05]]` |
| **[[T-13-SMR과-데이터센터-무탄소-전력-PPA\|T-13]]** | SMR과 데이터센터 무탄소 전력 PPA | `L2` | `🚀 주류` | `[[Company-NuScale\|NuScale]]`, `[[Company-Constellation\|Constellation]]` | `[[T-01-데이터센터의-변화\|T-01]]`, `[[T-23-변압기·초고압-그리드-쇼티지-장기화\|T-23]]` |
| **[[T-22-AI-전력망용-대용량-ESS와-LFP-공급망\|T-22]]** | AI 전력망용 대용량 ESS와 LFP | `L2` | `🚀 주류` | `[[Company-LG에너지솔루션\|LG에너지솔루션]]`, `[[Company-Tesla\|Tesla]]` | `[[T-01-데이터센터의-변화\|T-01]]`, `[[T-23-변압기·초고압-그리드-쇼티지-장기화\|T-23]]`, `[[T-32-ESS와-한국배터리의-미국수혜\|T-32]]` |
| **[[T-23-변압기·초고압-그리드-쇼티지-장기화\|T-23]]** | 변압기·초고압 그리드 쇼티지 장기화 | `L2` | `🚀 주류` | `[[Company-HD현대일렉트릭\|HD현대일렉트릭]]`, `[[Company-Eaton\|Eaton]]` | `[[T-01-데이터센터의-변화\|T-01]]`, `[[T-13-SMR과-데이터센터-무탄소-전력-PPA\|T-13]]`, `[[T-22-AI-전력망용-대용량-ESS와-LFP-공급망\|T-22]]` |
| **[[T-32-ESS와-한국배터리의-미국수혜\|T-32]]** | ESS와 한국 배터리의 미국 수혜 | `L0` | `🚀 주류` | `[[Company-LG에너지솔루션\|LG에너지솔루션]]`, `[[Company-삼성SDI\|삼성SDI]]` | `[[T-03-전고체-배터리의-변화\|T-03]]`, `[[T-22-AI-전력망용-대용량-ESS와-LFP-공급망\|T-22]]` |

### 3. 🤖 피지컬 AI, 모빌리티 & 로보틱스 (Sector 3)
| ID | 가설 제목 | 스택 | 성격 | 핵심 기업 | 주요 연관 테제 |
|:---|:---|:---:|:---:|:---|:---|
| **[[T-03-전고체-배터리의-변화\|T-03]]** | 전고체 배터리의 변화 | `L0` | `🚀 주류` | `[[Company-삼성SDI\|삼성SDI]]`, `[[Company-현대차\|현대차]]` | `[[T-17-휴머노이드-로봇과-액추에이터-공급망\|T-17]]`, `[[T-32-ESS와-한국배터리의-미국수혜\|T-32]]` |
| **[[T-04-온디바이스-AI의-변화\|T-04]]** | 온디바이스 AI의 변화 | `L5` | `🚀 주류` | `[[Company-Apple\|Apple]]`, `[[Company-Qualcomm\|Qualcomm]]` | `[[T-20-행동형-AI-에이전트와-모바일-교체-슈퍼사이클\|T-20]]`, `[[T-21-AI-PC-보급-확대와-Arm-기반-윈도우-생태계\|T-21]]` |
| **[[T-17-휴머노이드-로봇과-액추에이터-공급망\|T-17]]** | 휴머노이드 로봇과 액추에이터 | `L5` | `🚀 주류` | `[[Company-Tesla\|Tesla]]`, `[[Company-BostonDynamics\|Boston Dynamics]]` | `[[T-19-피지컬-AI와-공간지능-반도체\|T-19]]`, `[[T-30-피지컬AI와-로봇의-상용화\|T-30]]` |
| **[[T-18-End-to-End-AI-자율주행과-로보택시\|T-18]]** | End-to-End AI 자율주행과 로보택시 | `L5` | `🚀 주류` | `[[Company-Tesla\|Tesla]]`, `[[Company-Alphabet\|Waymo]]` | `[[T-04-온디바이스-AI의-변화\|T-04]]`, `[[T-19-피지컬-AI와-공간지능-반도체\|T-19]]` |
| **[[T-19-피지컬-AI와-공간지능-반도체\|T-19]]** | 피지컬 AI와 공간지능 반도체 | `L1` | `🚀 주류` | `[[Company-NVIDIA\|NVIDIA]]`, `[[Company-Qualcomm\|Qualcomm]]` | `[[T-17-휴머노이드-로봇과-액추에이터-공급망\|T-17]]`, `[[T-18-End-to-End-AI-자율주행과-로보택시\|T-18]]` |
| **[[T-20-행동형-AI-에이전트와-모바일-교체-슈퍼사이클\|T-20]]** | 행동형 AI 에이전트와 모바일 교체 | `L5` | `🚀 주류` | `[[Company-Apple\|Apple]]`, `[[Company-삼성전자\|삼성전자]]` | `[[T-04-온디바이스-AI의-변화\|T-04]]`, `[[T-21-AI-PC-보급-확대와-Arm-기반-윈도우-생태계\|T-21]]` |
| **[[T-21-AI-PC-보급-확대와-Arm-기반-윈도우-생태계\|T-21]]** | AI PC 보급 확대와 Arm 기반 윈도우 | `L5` | `🚀 주류` | `[[Company-Qualcomm\|Qualcomm]]`, `[[Company-Microsoft\|Microsoft]]` | `[[T-04-온디바이스-AI의-변화\|T-04]]`, `[[T-20-행동형-AI-에이전트와-모바일-교체-슈퍼사이클\|T-20]]` |
| **[[T-27-AI-스마트-글래스와-경량-AR-광학계\|T-27]]** | AI 스마트 글래스와 경량 AR 광학계 | `L5` | `🚀 주류` | `[[Company-Meta\|Meta]]`, `[[Company-Apple\|Apple]]` | `[[T-04-온디바이스-AI의-변화\|T-04]]`, `[[T-19-피지컬-AI와-공간지능-반도체\|T-19]]` |
| **[[T-30-피지컬AI와-로봇의-상용화\|T-30]]** | 피지컬 AI와 로봇의 상용화 | `L5` | `🚀 주류` | `[[Company-현대차\|현대차]]`, `[[Company-두산로보틱스\|두산로보틱스]]` | `[[T-03-전고체-배터리의-변화\|T-03]]`, `[[T-17-휴머노이드-로봇과-액추에이터-공급망\|T-17]]` |

### 4. 💻 AI 엔터프라이즈 SW & 버티컬 에이전트 (Sector 4)
| ID | 가설 제목 | 스택 | 성격 | 핵심 기업 | 주요 연관 테제 |
|:---|:---|:---:|:---:|:---|:---|
| **[[T-25-오픈소스-모델-고도화와-온프레미스-사설-AI\|T-25]]** | 오픈소스 모델 고도화와 온프레미스 | `L4` | `🚀 주류` | `[[Company-Meta\|Meta]]`, `[[Company-Dell\|Dell]]` | `[[T-04-온디바이스-AI의-변화\|T-04]]`, `[[T-26-소버린-AI와-국가-단위-컴퓨트-인프라\|T-26]]` |
| **[[T-31-AI-소프트웨어-레이어의-과점화\|T-31]]** | AI 소프트웨어 레이어의 과점화 | `L4` | `🚀 주류` | `[[Company-Microsoft\|Microsoft]]`, `[[Company-Alphabet\|Alphabet]]` | `[[T-06-TPU-증가와-GPU-수요-둔화\|T-06]]`, `[[T-08-엔비디아와-네오클라우드\|T-08]]` |
| **[[T-34-바이오AI와-신약개발-가속\|T-34]]** | 바이오 AI와 신약 개발 가속 | `L4` | `🚀 주류` | `[[Company-Recursion\|Recursion]]`, `[[Company-Schrodinger\|Schrodinger]]` | `[[T-04-온디바이스-AI의-변화\|T-04]]`, `[[T-15-AI-추론-시장-폭발과-LPU-ASIC-분화\|T-15]]` |

### 5. 🌐 지정학, 소버린 AI & 공급망 안보 (Sector 5)
| ID | 가설 제목 | 스택 | 성격 | 핵심 기업 | 주요 연관 테제 |
|:---|:---|:---:|:---:|:---|:---|
| **[[T-26-소버린-AI와-국가-단위-컴퓨트-인프라\|T-26]]** | 소버린 AI와 국가 단위 컴퓨트 | `L3` | `🚀 주류` | `[[Company-NVIDIA\|NVIDIA]]`, `[[Company-네이버\|네이버]]` | `[[T-01-데이터센터의-변화\|T-01]]`, `[[T-25-오픈소스-모델-고도화와-온프레미스-사설-AI\|T-25]]` |
| **[[T-36-중국반도체의-HBM-생산가능성\|T-36]]** | 중국 반도체의 HBM 생산 가능성 | `L1` | `🛡️ 헷지` | `[[Company-CXMT\|CXMT]]`, `[[Company-SMIC\|SMIC]]` | `[[T-02-메모리-산업의-변화\|T-02]]`, `[[T-15-AI-추론-시장-폭발과-LPU-ASIC-분화\|T-15]]` |

### 6. 🏛️ 매크로 자본시장, 금리 & 밸류에이션 (Sector 6)
| ID | 가설 제목 | 스택 | 성격 | 핵심 기업 | 주요 연관 테제 |
|:---|:---|:---:|:---:|:---|:---|
| **[[T-05-금리와-데이터센터\|T-05]]** | 금리와 데이터센터 (CAPEX ROI) | `L3` | `🛡️ 헷지` | `[[Company-Microsoft\|Microsoft]]`, `[[Company-Amazon\|Amazon]]` | `[[T-01-데이터센터의-변화\|T-01]]`, `[[T-08-엔비디아와-네오클라우드\|T-08]]`, `[[T-37-AI-버블-가능성\|T-37]]` |
| **[[T-08-엔비디아와-네오클라우드\|T-08]]** | 엔비디아와 네오클라우드 | `L3` | `🚀 주류` | `[[Company-CoreWeave\|CoreWeave]]`, `[[Company-NVIDIA\|NVIDIA]]` | `[[T-01-데이터센터의-변화\|T-01]]`, `[[T-05-금리와-데이터센터\|T-05]]`, `[[T-09-엔비디아와-GPU-금융\|T-09]]` |
| **[[T-09-엔비디아와-GPU-금융\|T-09]]** | 엔비디아와 GPU 금융 | `L3` | `🛡️ 헷지` | `[[Company-Blackstone\|Blackstone]]`, `[[Company-CoreWeave\|CoreWeave]]` | `[[T-08-엔비디아와-네오클라우드\|T-08]]`, `[[T-37-AI-버블-가능성\|T-37]]` |
| **[[T-37-AI-버블-가능성\|T-37]]** | AI 버블 가능성 (CAPEX ROI 불일치) | `L3` | `🛡️ 헷지` | `[[Company-NVIDIA\|NVIDIA]]`, `[[Company-BigTech\|빅테크]]` | `[[T-05-금리와-데이터센터\|T-05]]`, `[[T-08-엔비디아와-네오클라우드\|T-08]]`, `[[T-09-엔비디아와-GPU-금융\|T-09]]` |
| **[[T-38-10년금리-5%-재진입-가능성\|T-38]]** | 10년 금리 5% 재진입 가능성 | `L6` | `🛡️ 헷지` | `[[Company-US_Treasury\|미국채]]`, `[[Company-Fed\|연준]]` | `[[T-05-금리와-데이터센터\|T-05]]`, `[[T-37-AI-버블-가능성\|T-37]]` |
"""
    target = THESIS_DIR / "00-Argus-Master-MOC.md"
    target.write_text(content, encoding="utf-8")
    print("  🧭 [Master MOC 업데이트 완료] 6대 섹터 & 다차원 대시보드 내장")


def sync_all_to_vault():
    """모든 업그레이드 파일들을 사용자 옵시디언 볼트로 전체 동기화"""
    if not VAULT.exists():
        print(f"  ❌ 옵시디언 볼트 경로 없음: {VAULT}")
        return

    print(f"\n📂 [옵시디언 볼트 전체 동기화 진행 중...]")
    (VAULT / "argus" / "Theses").mkdir(parents=True, exist_ok=True)
    (VAULT / "argus" / "Vs").mkdir(parents=True, exist_ok=True)
    (VAULT / "argus" / "Docs").mkdir(parents=True, exist_ok=True)

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

    # 4. Vs Hubs
    count_vs = 0
    for v in THESIS_DIR.glob("Vs-*.md"):
        shutil.copy2(v, VAULT / "argus" / "Vs" / v.name)
        count_vs += 1

    print(f"  ✅ 동기화 완료: Theses {count_t}개, Vs Hubs {count_vs}개, Master MOC 1개")


if __name__ == "__main__":
    print("🚀 [Argus Pulse] 교차 차원 메타데이터 일괄 적용 및 Vs Hubs 생성 시작\n")
    build_vs_hubs()
    print()
    apply_dimensions_to_all_theses()
    print()
    update_master_moc()
    print()
    sync_all_to_vault()
    print("\n🎉 모든 교차 차원 적용 및 동기화가 성공적으로 완료되었습니다!")
