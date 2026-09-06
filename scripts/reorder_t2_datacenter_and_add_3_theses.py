"""
scripts/reorder_t2_datacenter_and_add_3_theses.py
T2를 AI 데이터센터 & 전력 인프라로 전환(신규 테제 3개 추가하여 총 9개 구축),
T3을 피지컬 AI & 로보틱스로 전환(9개 구축),
전체 41개 테제 메타데이터, MOC, Hubs 및 옵시디언 볼트 동기화.
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

# ── 1. 전체 41개 테제 정의 매핑 ──────────────────────────────────────────────
# T1 (13개): 반도체
# T2 (9개): AI 데이터센터 & 전력 인프라 (기존 6개 + 신규 3개)
# T3 (9개): 피지컬 AI & 로보틱스 (기존 T2 9개)
# T4 (5개): 매크로 & 자본시장
# T5 (3개): SW & 에이전트
# T6 (2개): 지정학 & 소버린

NEW_THESES_DATA = [
    # ── T2 신규 추가 3개 ──
    {
        "id": "T2-07",
        "slug": "800V-48V-HVDC-전력-아키텍처-혁신",
        "title": "800V·48V HVDC 전력 아키텍처 혁신",
        "sector": "AI 데이터센터 & 전력·냉각 인프라",
        "sector_id": "T2",
        "hypothesis": "GW급 AI 데이터센터의 I²R 전력 손실을 줄이기 위해 기존 480V AC 배전에서 800V DC 직류 및 48V 랙 내부 파워 모듈(HVDC)로의 전환이 가속화된다.",
        "thesis_nature": "consensus",
        "stack_name": "L2 (물리인프라/전력)",
        "stack_layer": "L2",
        "geography": ["US", "TW", "KR"],
        "time_horizon": "2026~2028",
        "confidence": 75,
        "priority": 4,
        "status": "active",
        "keywords": ["800V", "48V", "HVDC", "초고압직류", "전력변환", "Vicor", "MPS", "전력모듈", "랙파워"],
        "related_companies": ["Vicor", "Monolithic Power Systems", "Delta Electronics", "LS ELECTRIC", "Schneider Electric"],
        "related_theses": ["T2-01", "T2-02", "T2-05", "T1-01"],
        "related_vs": ["Vs-공랭-vs-액체냉각"],
        "aliases": ["T2-07", "T2-07 800V·48V HVDC 전력 아키텍처 혁신", "800V·48V HVDC 전력 아키텍처 혁신", "HVDC 전력 아키텍처"],
        "body": """## 핵심 논리 및 배경
1. **랙당 전력 밀도 폭증**: 차세대 엔비디아 루빈(Rubin) 및 블랙웰 울트라 서버 랙당 전력이 120kW~250kW로 급증함에 따라 기존 480V AC 전력선으로는 구리 두께와 발열(I²R 손실) 한계 봉착.
2. **800V DC ➔ 48V 파워 모듈화**: 전력 손실을 30% 이상 줄이기 위해 데이터센터 메인 버스바를 800V 직류로 공급하고 랙 내부에서 고효율 파워 모듈(Vicor/MPS)로 48V/1V 직변환.
3. **HVDC 송전망 직결**: 대규모 데이터센터 캠퍼스와 원전/신재생 발전소 간 초고압 직류 송전망(HVDC) 연계가 전력망 안정성의 필수재로 부상.

## 밸류체인 및 인과관계 맵
```mermaid
flowchart LR
    P_Grid["[[T2-05-변압기-초고압-그리드-쇼티지-장기화|T2-05 초고압 그리드]]"] --> T_Main["★ [[T2-07-800V-48V-HVDC-전력-아키텍처-혁신|T2-07 800V·48V HVDC 혁신]]"]
    T_Main --> D_DC["[[T2-01-데이터센터의-변화|T2-01 데이터센터 병목 해소]]"]
    T_Main --> D_Cool["[[T2-02-데이터센터-액체냉각의-표준화|T2-02 액체냉각 결합]]"]
```

## 핵심 수혜 기업 및 공급망
- **전력 변환 칩/모듈**: Vicor, Monolithic Power Systems (MPS), Delta Electronics
- **초고압 직류 송전(HVDC)**: LS ELECTRIC, HD현대일렉트릭, Siemens Energy, Schneider Electric

## 관련 최근 분석 리포트 & 블로그
```dataview
TABLE file.mtime AS "수정일", tags AS "태그"
FROM "argus" OR "outputs" OR "blog"
WHERE contains(thesis, "T2-07") OR contains(file.outlinks, this.file.link)
SORT file.mtime DESC
LIMIT 5
```
"""
    },
    {
        "id": "T2-08",
        "slug": "전력-포화와-분산형-AI-데이터센터-코로케이션",
        "title": "전력 포화와 분산형 AI 데이터센터 코로케이션",
        "sector": "AI 데이터센터 & 전력·냉각 인프라",
        "sector_id": "T2",
        "hypothesis": "기존 테크 허브의 전력 인입 지연으로 인해 전력 여유가 있는 외곽 지역으로 분산되는 캠퍼스형 AI 데이터센터 및 코로케이션 렌트비가 급등한다.",
        "thesis_nature": "consensus",
        "stack_name": "L2 (물리인프라)",
        "stack_layer": "L2",
        "geography": ["US", "EU", "KR"],
        "time_horizon": "2026~2028",
        "confidence": 80,
        "priority": 4,
        "status": "active",
        "keywords": ["코로케이션", "데이터센터부지", "전력포화", "Equinix", "Digital Realty", "Applied Digital", "분산컴퓨팅"],
        "related_companies": ["Equinix", "Digital Realty", "Applied Digital", "CoreWeave", "Microsoft"],
        "related_theses": ["T2-01", "T4-01", "T4-02", "T6-01"],
        "related_vs": [],
        "aliases": ["T2-08", "T2-08 전력 포화와 분산형 AI 데이터센터 코로케이션", "분산형 AI 데이터센터 코로케이션", "코로케이션 데이터센터"],
        "body": """## 핵심 논리 및 배경
1. **수도권 및 북미 주요 거점 전력 셧다운**: 버지니아 라우든 카운티, 실리콘밸리 등 메이저 데이터센터 허브의 전력망 대기열(Interconnection Queue)이 5~7년으로 연장.
2. **지리적 분산과 하이퍼스케일 코로케이션**: 저렴하고 즉시 조달 가능한 전력(원전, 수력, 지열)이 있는 외곽 지역으로 AI 학습 클러스터를 이전하고, 추론은 엣지 코로케이션에 분산.
3. **데이터센터 임대료(Cap Rate) 상승**: 신규 공급 제한으로 기보유 코로케이션 사업자(Equinix, Digital Realty)의 계약 갱신 단가(P)와 장기 임대 가치 폭등.

## 밸류체인 및 인과관계 맵
```mermaid
flowchart LR
    P_Cap["[[T4-01-금리와-데이터센터|T4-01 DC 금리 및 ROI]]"] --> T_Main["★ [[T2-08-전력-포화와-분산형-AI-데이터센터-코로케이션|T2-08 분산형 코로케이션]]"]
    T_Main --> D_DC["[[T2-01-데이터센터의-변화|T2-01 데이터센터 공급망]]"]
    T_Main --> D_Neo["[[T4-02-엔비디아와-네오클라우드|T4-02 네오클라우드 인프라]]"]
```

## 핵심 수혜 기업 및 공급망
- **글로벌 코로케이션 리츠**: Equinix (EQIX), Digital Realty (DLR)
- **AI 특화 인프라 호스팅**: Applied Digital (APLD), CoreWeave, Crusoe Energy

## 관련 최근 분석 리포트 & 블로그
```dataview
TABLE file.mtime AS "수정일", tags AS "태그"
FROM "argus" OR "outputs" OR "blog"
WHERE contains(thesis, "T2-08") OR contains(file.outlinks, this.file.link)
SORT file.mtime DESC
LIMIT 5
```
"""
    },
    {
        "id": "T2-09",
        "slug": "온사이트-가스터빈과-연료전지-자체발전",
        "title": "온사이트 가스터빈과 연료전지 자체발전",
        "sector": "AI 데이터센터 & 전력·냉각 인프라",
        "sector_id": "T2",
        "hypothesis": "전력망 연결 지연을 우회하기 위해 데이터센터 부지 내에 직접 가스터빈 및 수소/천연가스 연료전지를 설치하는 'Behind-the-Meter 자체 기저발전'이 필수가 된다.",
        "thesis_nature": "consensus",
        "stack_name": "L2 (물리인프라/에너지)",
        "stack_layer": "L2",
        "geography": ["US", "KR"],
        "time_horizon": "2026~2028",
        "confidence": 72,
        "priority": 4,
        "status": "active",
        "keywords": ["온사이트발전", "가스터빈", "연료전지", "블룸에너지", "GE Vernova", "Behind-the-Meter", "자체발전"],
        "related_companies": ["GE Vernova", "Bloom Energy", "Constellation Energy", "두산퓨얼셀", "SK이터닉스"],
        "related_theses": ["T2-01", "T2-03", "T2-05", "T4-01"],
        "related_vs": [],
        "aliases": ["T2-09", "T2-09 온사이트 가스터빈과 연료전지 자체발전", "온사이트 가스터빈 연료전지", "데이터센터 자체발전"],
        "body": """## 핵심 논리 및 배경
1. **그리드 의존 탈피(Behind-the-Meter)**: 공공 유틸리티 전력망 인입에 수년이 걸리자, 데이터센터 사업자가 부지 내에 직접 천연가스 터빈 또는 고체산화물 연료전지(SOFC)를 구축하여 자가 발전 시작.
2. **연료전지(SOFC)의 고효율 무소음 장점**: 블룸에너지를 필두로 데이터센터 전용 전력원 공급 계약 급증, 탄소 배출 규제 대응용 수소 혼소 터빈 도입.
3. **SMR 가동 전(2026~2029) 브릿지 전력원**: 4세대 원전 SMR이 본격 상용화되기 전까지 가스터빈과 연료전지가 데이터센터 기저부하의 핵심 가교 역할 수행.

## 밸류체인 및 인과관계 맵
```mermaid
flowchart LR
    P_SMR["[[T2-03-SMR과-데이터센터-무탄소-전력-PPA|T2-03 SMR 전력]]"] <.- 브릿지 -.-> T_Main["★ [[T2-09-온사이트-가스터빈과-연료전지-자체발전|T2-09 온사이트 자체발전]]"]
    T_Main --> D_DC["[[T2-01-데이터센터의-변화|T2-01 데이터센터 전력 자립]]"]
```

## 핵심 수혜 기업 및 공급망
- **가스터빈 / 복합화력**: GE Vernova (GEV), Siemens Energy, 두산에너빌리티
- **데이터센터 SOFC 연료전지**: Bloom Energy (BE), 두산퓨얼셀, SK이터닉스

## 관련 최근 분석 리포트 & 블로그
```dataview
TABLE file.mtime AS "수정일", tags AS "태그"
FROM "argus" OR "outputs" OR "blog"
WHERE contains(thesis, "T2-09") OR contains(file.outlinks, this.file.link)
SORT file.mtime DESC
LIMIT 5
```
"""
    }
]

# ── 2. 기존 ID ➔ 신규 ID 전체 매핑 테이블 구성 ──────────────────────────────
# 변환 규칙:
# - 기존 T2-01~09 (로보틱스) -> 신규 T3-01~09
# - 기존 T3-01~06 (데이터센터) -> 신규 T2-01~06
# - 신규 T2-07~09 (데이터센터 신규 3개)
# - T1, T4, T5, T6은 그대로 유지

ID_TRANSFORM_MAP = {
    # Data Center (T3 -> T2)
    "T3-01": "T2-01", "DC-01": "T2-01", "T-01": "T2-01",
    "T3-02": "T2-02", "DC-02": "T2-02", "T-12": "T2-02",
    "T3-03": "T2-03", "DC-03": "T2-03", "T-13": "T2-03",
    "T3-04": "T2-04", "DC-04": "T2-04", "T-22": "T2-04",
    "T3-05": "T2-05", "DC-05": "T2-05", "T-23": "T2-05",
    "T3-06": "T2-06", "DC-06": "T2-06", "T-32": "T2-06",

    # Robotics (T2 -> T3)
    "T2-01": "T3-01", "RB-01": "T3-01", "T-03": "T3-01",
    "T2-02": "T3-02", "RB-02": "T3-02", "T-04": "T3-02",
    "T2-03": "T3-03", "RB-03": "T3-03", "T-17": "T3-03",
    "T2-04": "T3-04", "RB-04": "T3-04", "T-18": "T3-04",
    "T2-05": "T3-05", "RB-05": "T3-05", "T-19": "T3-05",
    "T2-06": "T3-06", "RB-06": "T3-06", "T-20": "T3-06",
    "T2-07": "T3-07", "RB-07": "T3-07", "T-21": "T3-07",
    "T2-08": "T3-08", "RB-08": "T3-08", "T-27": "T3-08",
    "T2-09": "T3-09", "RB-09": "T3-09", "T-30": "T3-09",
}

# 파일 슬러그 매핑
DC_SLUGS = [
    ("T3-01", "T2-01", "데이터센터의-변화", "데이터센터의 변화", "T2"),
    ("T3-02", "T2-02", "데이터센터-액체냉각의-표준화", "데이터센터 액체냉각의 표준화", "T2"),
    ("T3-03", "T2-03", "SMR과-데이터센터-무탄소-전력-PPA", "SMR과 데이터센터 무탄소 전력 PPA", "T2"),
    ("T3-04", "T2-04", "AI-전력망용-대용량-ESS와-LFP-공급망", "AI 전력망용 대용량 ESS와 LFP 공급망", "T2"),
    ("T3-05", "T2-05", "변압기-초고압-그리드-쇼티지-장기화", "변압기·초고압 그리드 쇼티지 장기화", "T2"),
    ("T3-06", "T2-06", "ESS와-한국배터리의-미국수혜", "ESS와 한국 배터리의 미국 수혜", "T2"),
]

RB_SLUGS = [
    ("T2-01", "T3-01", "전고체-배터리의-변화", "전고체 배터리의 변화", "T3"),
    ("T2-02", "T3-02", "온디바이스-AI의-변화", "온디바이스 AI의 변화", "T3"),
    ("T2-03", "T3-03", "휴머노이드-로봇과-액추에이터-공급망", "휴머노이드 로봇과 액추에이터 공급망", "T3"),
    ("T2-04", "T3-04", "End-to-End-AI-자율주행과-로보택시", "End-to-End AI 자율주행과 로보택시", "T3"),
    ("T2-05", "T3-05", "피지컬-AI와-공간지능-반도체", "피지컬 AI와 공간지능 반도체", "T3"),
    ("T2-06", "T3-06", "행동형-AI-에이전트와-모바일-교체-슈퍼사이클", "행동형 AI 에이전트와 모바일 교체 슈퍼사이클", "T3"),
    ("T2-07", "T3-07", "AI-PC-보급-확대와-Arm-기반-윈도우-생태계", "AI PC 보급 확대와 Arm 기반 윈도우 생태계", "T3"),
    ("T2-08", "T3-08", "AI-스마트-글래스와-경량-AR-광학계", "AI 스마트 글래스와 경량 AR 광학계", "T3"),
    ("T2-09", "T3-09", "피지컬AI와-로봇의-상용화", "피지컬 AI와 로봇의 상용화", "T3"),
]


def execute_migration():
    print("🚀 [Argus Nexus] T2(AI 데이터센터, 9개) & T3(로보틱스, 9개) 리팩토링 및 3개 신규 테제 생성 시작\n")

    # 1. 임시 이름으로 기존 파일들 rename하여 충돌 방지
    for old_id, new_id, slug, title, sector_id in DC_SLUGS:
        f = THESIS_DIR / f"{old_id}-{slug}.md"
        if f.exists():
            f.rename(THESIS_DIR / f"TEMP_DC_{new_id}-{slug}.md")

    for old_id, new_id, slug, title, sector_id in RB_SLUGS:
        f = THESIS_DIR / f"{old_id}-{slug}.md"
        if f.exists():
            f.rename(THESIS_DIR / f"TEMP_RB_{new_id}-{slug}.md")

    # 2. DC 파일들을 T2-XX로 정식 저장 및 프론트매터 갱신
    for old_id, new_id, slug, title, sector_id in DC_SLUGS:
        temp_f = THESIS_DIR / f"TEMP_DC_{new_id}-{slug}.md"
        raw_text = temp_f.read_text(encoding="utf-8")
        parts = raw_text.split("---", 2)
        meta = yaml.safe_load(parts[1]) or {}
        body = parts[2].lstrip("\r\n")

        meta["id"] = new_id
        meta["sector_id"] = sector_id
        aliases = meta.get("aliases", [])
        for a in [new_id, f"{new_id} {title}", old_id, f"{old_id} {title}"]:
            if a not in aliases:
                aliases.append(a)
        meta["aliases"] = aliases

        new_f = THESIS_DIR / f"{new_id}-{slug}.md"
        yaml_str = yaml.dump(meta, allow_unicode=True, sort_keys=False)
        new_f.write_text(f"---\n{yaml_str}---\n\n{body}", encoding="utf-8")
        temp_f.unlink()
        print(f"  ✅ [DC ➔ T2 전환] {old_id} ➔ {new_id} ({new_f.name})")

    # 3. RB 파일들을 T3-XX로 정식 저장 및 프론트매터 갱신
    for old_id, new_id, slug, title, sector_id in RB_SLUGS:
        temp_f = THESIS_DIR / f"TEMP_RB_{new_id}-{slug}.md"
        raw_text = temp_f.read_text(encoding="utf-8")
        parts = raw_text.split("---", 2)
        meta = yaml.safe_load(parts[1]) or {}
        body = parts[2].lstrip("\r\n")

        meta["id"] = new_id
        meta["sector_id"] = sector_id
        aliases = meta.get("aliases", [])
        for a in [new_id, f"{new_id} {title}", old_id, f"{old_id} {title}"]:
            if a not in aliases:
                aliases.append(a)
        meta["aliases"] = aliases

        new_f = THESIS_DIR / f"{new_id}-{slug}.md"
        yaml_str = yaml.dump(meta, allow_unicode=True, sort_keys=False)
        new_f.write_text(f"---\n{yaml_str}---\n\n{body}", encoding="utf-8")
        temp_f.unlink()
        print(f"  ✅ [RB ➔ T3 전환] {old_id} ➔ {new_id} ({new_f.name})")

    # 4. 신규 T2-07, T2-08, T2-09 파일 생성
    print("\n✨ [신규 AI 데이터센터 테제 3선 생성]...")
    for t_data in NEW_THESES_DATA:
        body = t_data.pop("body")
        slug = t_data.pop("slug")
        tid = t_data["id"]
        filepath = THESIS_DIR / f"{tid}-{slug}.md"
        yaml_str = yaml.dump(t_data, allow_unicode=True, sort_keys=False)
        filepath.write_text(f"---\n{yaml_str}---\n\n# {tid} {t_data['title']}\n\n{body}", encoding="utf-8")
        print(f"  🌟 [신규 테제 생성] {tid} ({filepath.name})")

    # 5. 모든 테제 및 허브, MOC 내 링크 일괄 치환
    print("\n🔄 [전체 테제, 허브, MOC 링크 상호 최신화 중...]")
    # 파일명 교체 사전
    FILE_REPLACE = {}
    for old_id, new_id, slug, *_ in DC_SLUGS:
        FILE_REPLACE[f"{old_id}-{slug}"] = f"{new_id}-{slug}"
    for old_id, new_id, slug, *_ in RB_SLUGS:
        FILE_REPLACE[f"{old_id}-{slug}"] = f"{new_id}-{slug}"

    for md_file in THESIS_DIR.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        modified = False

        # 파일명 링크 치환
        for old_fname, new_fname in FILE_REPLACE.items():
            if old_fname in content:
                content = content.replace(f"[[{old_fname}", f"[[{new_fname}")
                modified = True

        # ID 치환
        for old_id, new_id, slug, title, *_ in DC_SLUGS + RB_SLUGS:
            if f"# {old_id} " in content:
                content = content.replace(f"# {old_id} ", f"# {new_id} ")
                modified = True
            if f"|{old_id}]]" in content:
                content = content.replace(f"|{old_id}]]", f"|{new_id}]]")
                modified = True
            if f"|{old_id} " in content:
                content = content.replace(f"|{old_id} ", f"|{new_id} ")
                modified = True
            if f"[[{old_id}|" in content:
                content = content.replace(f"[[{old_id}|", f"[[{new_id}|")
                modified = True

        if modified:
            md_file.write_text(content, encoding="utf-8")
            print(f"  📝 [내용 최신화] {md_file.name}")


def update_master_moc():
    """00-Argus-Master-MOC.md 를 41개 테제 체계로 완벽하게 갱신"""
    moc_path = THESIS_DIR / "00-Argus-Master-MOC.md"
    moc_content = """---
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
> AI 및 첨단 기술 산업의 구조적 변화를 추적하는 **총 41개 투자 가설(Theses)**의 상호 인과관계 맵과 **6대 섹터 & 5대 교차 차원(다차원 대시보드)** 사령탑입니다.

---

## 🗺️ 전체 가설 생태계 가치사슬 구조도 (Macro Value Chain)

```mermaid
flowchart TB
    subgraph Macro["🏛️ 매크로 자본시장 & 밸류에이션 (T4)"]
        T4_01["[[T4-01-금리와-데이터센터|T4-01 금리와 DC ROI]]"]
        T4_02["[[T4-02-엔비디아와-네오클라우드|T4-02 네오클라우드]]"]
        T4_03["[[T4-03-엔비디아와-GPU-금융|T4-03 GPU 금융]]"]
        T4_04["[[T4-04-AI-버블-가능성|T4-04 AI 버블 붕괴 리스크]]"]
        T4_05["[[T4-05-10년금리-5%-재진입-가능성|T4-05 10년 금리 5%]]"]
    end

    subgraph PowerInfra["⚡ AI 데이터센터 & 전력·냉각 인프라 (T2)"]
        T2_01["[[T2-01-데이터센터의-변화|T2-01 데이터센터 병목]]"]
        T2_02["[[T2-02-데이터센터-액체냉각의-표준화|T2-02 액체냉각 표준화]]"]
        T2_03["[[T2-03-SMR과-데이터센터-무탄소-전력-PPA|T2-03 SMR·무탄소 PPA]]"]
        T2_04["[[T2-04-AI-전력망용-대용량-ESS와-LFP-공급망|T2-04 대용량 ESS/LFP]]"]
        T2_05["[[T2-05-변압기-초고압-그리드-쇼티지-장기화|T2-05 변압기·그리드]]"]
        T2_06["[[T2-06-ESS와-한국배터리의-미국수혜|T2-06 K-배터리 미국수혜]]"]
        T2_07["[[T2-07-800V-48V-HVDC-전력-아키텍처-혁신|T2-07 800V/HVDC 혁신]]"]
        T2_08["[[T2-08-전력-포화와-분산형-AI-데이터센터-코로케이션|T2-08 분산형 코로케이션]]"]
        T2_09["[[T2-09-온사이트-가스터빈과-연료전지-자체발전|T2-09 온사이트 자체발전]]"]
    end

    subgraph ComputeMemory["💾 AI 컴퓨트 & 차세대 반도체 (T1)"]
        T1_01["[[T1-01-메모리-산업의-변화|T1-01 HBM4 ASIC화]]"]
        T1_02["[[T1-02-TPU-증가와-GPU-수요-둔화|T1-02 TPU vs GPU]]"]
        T1_03["[[T1-03-CXL-메모리의-확대|T1-03 CXL 메모리 풀링]]"]
        T1_04["[[T1-04-첨단-패키징과-CoWoS의-병목|T1-04 CoWoS 패키징]]"]
        T1_05["[[T1-05-유리기판의-차세대-패키징-침투|T1-05 유리기판 인터포저]]"]
        T1_06["[[T1-06-실리콘-포토닉스와-CPO의-상용화|T1-06 CPO 광반도체]]"]
        T1_07["[[T1-07-AI-추론-시장-폭발과-LPU-ASIC-분화|T1-07 추론 LPU·ASIC]]"]
        T1_08["[[T1-08-파운드리-2nm-공정과-GAA-격돌|T1-08 파운드리 2nm GAA]]"]
        T1_09["[[T1-09-빅테크-커스텀-ASIC-증가와-DSP-생태계|T1-09 빅테크 ASIC/DSP]]"]
        T1_10["[[T1-10-3D-DRAM-기술-전환과-400단-V-NAND|T1-10 3D DRAM & V-NAND]]"]
        T1_11["[[T1-11-초고속-AI-네트워킹-UEC-vs-인피니밴드|T1-11 UEC vs 인피니밴드]]"]
        T1_12["[[T1-12-반도체-소부장의-내재화|T1-12 반도체 소부장]]"]
        T1_13["[[T1-13-메모리-2028년-피크아웃|T1-13 2028 메모리 피크아웃]]"]
    end

    subgraph SoftwareAgents["💻 AI 엔터프라이즈 SW & 에이전트 (T5)"]
        T5_01["[[T5-01-오픈소스-모델-고도화와-온프레미스-사설-AI|T5-01 사설 AI / 온프레미스]]"]
        T5_02["[[T5-02-AI-소프트웨어-레이어의-과점화|T5-02 AI SW 레이어 과점]]"]
        T5_03["[[T5-03-바이오AI와-신약개발-가속|T5-03 바이오 AI 신약]]"]
    end

    subgraph Geopolitics["🌐 지정학, 소버린 AI & 공급망 안보 (T6)"]
        T6_01["[[T6-01-소버린-AI와-국가-단위-컴퓨트-인프라|T6-01 소버린 AI]]"]
        T6_02["[[T6-02-중국반도체의-HBM-생산가능성|T6-02 중국 HBM 추격]]"]
    end

    subgraph EdgePhysical["🤖 피지컬 AI, 모빌리티 & 로보틱스 (T3)"]
        T3_01["[[T3-01-전고체-배터리의-변화|T3-01 전고체 배터리]]"]
        T3_02["[[T3-02-온디바이스-AI의-변화|T3-02 온디바이스 NPU]]"]
        T3_03["[[T3-03-휴머노이드-로봇과-액추에이터-공급망|T3-03 휴머노이드 로봇]]"]
        T3_04["[[T3-04-End-to-End-AI-자율주행과-로보택시|T3-04 E2E 자율주행]]"]
        T3_05["[[T3-05-피지컬-AI와-공간지능-반도체|T3-05 피지컬 AI 공간지능]]"]
        T3_06["[[T3-06-행동형-AI-에이전트와-모바일-교체-슈퍼사이클|T3-06 모바일 교체 사이클]]"]
        T3_07["[[T3-07-AI-PC-보급-확대와-Arm-기반-윈도우-생태계|T3-07 AI PC & Arm]]"]
        T3_08["[[T3-08-AI-스마트-글래스와-경량-AR-광학계|T3-08 AI 스마트 글래스]]"]
        T3_09["[[T3-09-피지컬AI와-로봇의-상용화|T3-09 로봇 상용화]]"]
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
```dataview
TABLE hypothesis AS "핵심 가설", sector AS "섹터", confidence AS "신뢰도", momentum AS "모멘텀"
FROM "argus/Theses" OR "Theses" OR "thesis"
WHERE thesis_nature = "contrarian"
SORT momentum DESC
```

---

### 🧱 2. 6계층 밸류체인 수직 스택 뷰 (Value Chain Stack L0~L5)
```dataview
TABLE stack_name AS "스택 레이어", title AS "가설 제목", related_companies AS "핵심 기업"
FROM "argus/Theses" OR "Theses" OR "thesis"
SORT stack_layer ASC, rank ASC
```

---

### 🗺️ 3. 한국(KR) 핵심 수혜 및 공급망 뷰 (Korea Alpha View)
```dataview
TABLE title AS "가설 제목", hypothesis AS "핵심 가설", momentum AS "모멘텀", rank AS "순위"
FROM "argus/Theses" OR "Theses" OR "thesis"
WHERE contains(geography, "KR")
SORT momentum DESC
LIMIT 12
```

---

## ⚔️ 핵심 기술 & 진영 대결 구도 (Versus Hubs)

- **[[Vs-GPU-vs-TPU-ASIC|⚔️ 범용 GPU (NVIDIA) vs 커스텀 ASIC (빅테크 자체 칩)]]**: `T1-02`, `T4-02`, `T1-07`, `T1-09`
- **[[Vs-TSMC동맹-vs-삼성턴키|⚔️ TSMC 동맹 (SK-TSMC) vs 삼성전자 턴키 (원팀)]]**: `T1-01`, `T1-04`, `T1-08`
- **[[Vs-공랭-vs-액체냉각|⚔️ 레거시 공랭식 vs 직접액체냉각 (DLC & CDU)]]**: `T2-01`, `T2-02`, `T2-07`
- **[[Vs-인피니밴드-vs-울트라이더넷|⚔️ 인피니밴드 (NVIDIA) vs 울트라 이더넷 (UEC 연합)]]**: `T1-06`, `T1-11`

---

## 📂 6대 섹터별 테제 인덱스 (총 41개)

### 1. 💾 AI 컴퓨트 & 차세대 반도체 (T1, 13개)
| ID | 가설 제목 | 스택 | 성격 | 핵심 기업 | 주요 연관 테제 |
|:---|:---|:---:|:---:|:---|:---|
| **[[T1-01-메모리-산업의-변화|T1-01]]** | 메모리 산업의 변화 | `L1` | `🚀 주류` | `[[Company-SK하이닉스\|SK하이닉스]]`, `[[Company-삼성전자\|삼성전자]]` | `[[T1-03-CXL-메모리의-확대|T1-03]]`, `[[T1-04-첨단-패키징과-CoWoS의-병목|T1-04]]`, `[[T1-13-메모리-2028년-피크아웃|T1-13]]` |
| **[[T1-02-TPU-증가와-GPU-수요-둔화|T1-02]]** | TPU 증가와 GPU 수요 둔화 | `L1` | `🛡️ 헷지` | `[[Company-Alphabet\|Alphabet]]`, `[[Company-Broadcom\|Broadcom]]` | `[[T4-02-엔비디아와-네오클라우드|T4-02]]`, `[[T1-07-AI-추론-시장-폭발과-LPU-ASIC-분화|T1-07]]`, `[[T1-09-빅테크-커스텀-ASIC-증가와-DSP-생태계|T1-09]]` |
| **[[T1-03-CXL-메모리의-확대|T1-03]]** | CXL 메모리의 확대 | `L1` | `🚀 주류` | `[[Company-삼성전자\|삼성전자]]`, `[[Company-SK하이닉스\|SK하이닉스]]` | `[[T1-01-메모리-산업의-변화|T1-01]]`, `[[T1-10-3D-DRAM-기술-전환과-400단-V-NAND|T1-10]]` |
| **[[T1-04-첨단-패키징과-CoWoS의-병목|T1-04]]** | 첨단 패키징과 CoWoS의 병목 | `L1` | `🚀 주류` | `[[Company-TSMC\|TSMC]]`, `[[Company-SK하이닉스\|SK하이닉스]]` | `[[T2-01-데이터센터의-변화|T2-01]]`, `[[T1-01-메모리-산업의-변화|T1-01]]`, `[[T1-05-유리기판의-차세대-패키징-침투|T1-05]]` |
| **[[T1-05-유리기판의-차세대-패키징-침투|T1-05]]** | 유리기판의 차세대 패키징 침투 | `L0` | `🚀 주류` | `[[Company-SKC\|SKC]]`, `[[Company-인텔\|인텔]]` | `[[T1-04-첨단-패키징과-CoWoS의-병목|T1-04]]`, `[[T1-01-메모리-산업의-변화|T1-01]]` |
| **[[T1-06-실리콘-포토닉스와-CPO의-상용화|T1-06]]** | 실리콘 포토닉스와 CPO의 상용화 | `L3` | `🚀 주류` | `[[Company-Broadcom\|Broadcom]]`, `[[Company-TSMC\|TSMC]]` | `[[T2-01-데이터센터의-변화|T2-01]]`, `[[T1-11-초고속-AI-네트워킹-UEC-vs-인피니밴드|T1-11]]` |
| **[[T1-07-AI-추론-시장-폭발과-LPU-ASIC-분화|T1-07]]** | AI 추론 시장 폭발과 LPU·ASIC | `L1` | `🚀 주류` | `[[Company-Groq\|Groq]]`, `[[Company-Qualcomm\|Qualcomm]]` | `[[T1-02-TPU-증가와-GPU-수요-둔화|T1-02]]`, `[[T1-09-빅테크-커스텀-ASIC-증가와-DSP-생태계|T1-09]]` |
| **[[T1-08-파운드리-2nm-공정과-GAA-격돌|T1-08]]** | 파운드리 2nm 공정과 GAA 격돌 | `L1` | `🚀 주류` | `[[Company-TSMC\|TSMC]]`, `[[Company-삼성전자\|삼성전자]]` | `[[T1-01-메모리-산업의-변화|T1-01]]`, `[[T1-04-첨단-패키징과-CoWoS의-병목|T1-04]]` |
| **[[T1-09-빅테크-커스텀-ASIC-증가와-DSP-생태계|T1-09]]** | 빅테크 커스텀 ASIC 증가와 DSP | `L1` | `🚀 주류` | `[[Company-Broadcom\|Broadcom]]`, `[[Company-TSMC\|TSMC]]` | `[[T1-02-TPU-증가와-GPU-수요-둔화|T1-02]]`, `[[T1-07-AI-추론-시장-폭발과-LPU-ASIC-분화|T1-07]]` |
| **[[T1-10-3D-DRAM-기술-전환과-400단-V-NAND|T1-10]]** | 3D DRAM 기술 전환과 400단 V-NAND | `L1` | `🚀 주류` | `[[Company-SK하이닉스\|SK하이닉스]]`, `[[Company-삼성전자\|삼성전자]]` | `[[T1-01-메모리-산업의-변화|T1-01]]`, `[[T1-03-CXL-메모리의-확대|T1-03]]` |
| **[[T1-11-초고속-AI-네트워킹-UEC-vs-인피니밴드|T1-11]]** | 초고속 AI 네트워킹 UEC vs 인피니밴드 | `L3` | `🚀 주류` | `[[Company-Arista\|Arista]]`, `[[Company-NVIDIA\|NVIDIA]]` | `[[T2-01-데이터센터의-변화|T2-01]]`, `[[T1-06-실리콘-포토닉스와-CPO의-상용화|T1-06]]` |
| **[[T1-12-반도체-소부장의-내재화|T1-12]]** | 반도체 소부장의 내재화 | `L0` | `🚀 주류` | `[[Company-한미반도체\|한미반도체]]`, `[[Company-동진쎄미켐\|동진쎄미켐]]` | `[[T2-01-데이터센터의-변화|T2-01]]`, `[[T1-01-메모리-산업의-변화|T1-01]]` |
| **[[T1-13-메모리-2028년-피크아웃|T1-13]]** | 메모리 2028년 피크아웃 논쟁 | `L1` | `🛡️ 헷지` | `[[Company-SK하이닉스\|SK하이닉스]]`, `[[Company-삼성전자\|삼성전자]]` | `[[T1-01-메모리-산업의-변화|T1-01]]`, `[[T1-02-TPU-증가와-GPU-수요-둔화|T1-02]]` |

### 2. ⚡ AI 데이터센터 & 전력·냉각 인프라 (T2, 9개)
| ID | 가설 제목 | 스택 | 성격 | 핵심 기업 | 주요 연관 테제 |
|:---|:---|:---:|:---:|:---|:---|
| **[[T2-01-데이터센터의-변화|T2-01]]** | 데이터센터의 변화 (전력·냉각 병목) | `L2` | `🚀 주류` | `[[Company-Vertiv\|Vertiv]]`, `[[Company-HD현대일렉트릭\|HD현대일렉트릭]]` | `[[T4-01-금리와-데이터센터|T4-01]]`, `[[T2-02-데이터센터-액체냉각의-표준화|T2-02]]`, `[[T2-05-변압기-초고압-그리드-쇼티지-장기화|T2-05]]` |
| **[[T2-02-데이터센터-액체냉각의-표준화|T2-02]]** | 데이터센터 액체냉각의 표준화 | `L2` | `🚀 주류` | `[[Company-Vertiv\|Vertiv]]`, `[[Company-Supermicro\|Supermicro]]` | `[[T2-01-데이터센터의-변화|T2-01]]`, `[[T4-01-금리와-데이터센터|T4-01]]` |
| **[[T2-03-SMR과-데이터센터-무탄소-전력-PPA|T2-03]]** | SMR과 데이터센터 무탄소 전력 PPA | `L2` | `🚀 주류` | `[[Company-NuScale\|NuScale]]`, `[[Company-Constellation\|Constellation]]` | `[[T2-01-데이터센터의-변화|T2-01]]`, `[[T2-05-변압기-초고압-그리드-쇼티지-장기화|T2-05]]` |
| **[[T2-04-AI-전력망용-대용량-ESS와-LFP-공급망|T2-04]]** | AI 전력망용 대용량 ESS와 LFP | `L2` | `🚀 주류` | `[[Company-LG에너지솔루션\|LG에너지솔루션]]`, `[[Company-Tesla\|Tesla]]` | `[[T2-01-데이터센터의-변화|T2-01]]`, `[[T2-05-변압기-초고압-그리드-쇼티지-장기화|T2-05]]`, `[[T2-06-ESS와-한국배터리의-미국수혜|T2-06]]` |
| **[[T2-05-변압기-초고압-그리드-쇼티지-장기화|T2-05]]** | 변압기·초고압 그리드 쇼티지 장기화 | `L2` | `🚀 주류` | `[[Company-HD현대일렉트릭\|HD현대일렉트릭]]`, `[[Company-Eaton\|Eaton]]` | `[[T2-01-데이터센터의-변화|T2-01]]`, `[[T2-03-SMR과-데이터센터-무탄소-전력-PPA|T2-03]]`, `[[T2-04-AI-전력망용-대용량-ESS와-LFP-공급망|T2-04]]` |
| **[[T2-06-ESS와-한국배터리의-미국수혜|T2-06]]** | ESS와 한국 배터리의 미국 수혜 | `L0` | `🚀 주류` | `[[Company-LG에너지솔루션\|LG에너지솔루션]]`, `[[Company-삼성SDI\|삼성SDI]]` | `[[T3-01-전고체-배터리의-변화|T3-01]]`, `[[T2-04-AI-전력망용-대용량-ESS와-LFP-공급망|T2-04]]` |
| **[[T2-07-800V-48V-HVDC-전력-아키텍처-혁신|T2-07]]** | 800V·48V HVDC 전력 아키텍처 혁신 | `L2` | `🚀 주류` | `[[Company-Vicor\|Vicor]]`, `[[Company-LS-ELECTRIC\|LS ELECTRIC]]` | `[[T2-01-데이터센터의-변화|T2-01]]`, `[[T2-05-변압기-초고압-그리드-쇼티지-장기화|T2-05]]` |
| **[[T2-08-전력-포화와-분산형-AI-데이터센터-코로케이션|T2-08]]** | 전력 포화와 분산형 AI 데이터센터 코로케이션 | `L2` | `🚀 주류` | `[[Company-Equinix\|Equinix]]`, `[[Company-DigitalRealty\|Digital Realty]]` | `[[T2-01-데이터센터의-변화|T2-01]]`, `[[T4-01-금리와-데이터센터|T4-01]]` |
| **[[T2-09-온사이트-가스터빈과-연료전지-자체발전|T2-09]]** | 온사이트 가스터빈과 연료전지 자체발전 | `L2` | `🚀 주류` | `[[Company-GE-Vernova\|GE Vernova]]`, `[[Company-Bloom-Energy\|Bloom Energy]]` | `[[T2-01-데이터센터의-변화|T2-01]]`, `[[T2-03-SMR과-데이터센터-무탄소-전력-PPA|T2-03]]` |

### 3. 🤖 피지컬 AI, 모빌리티 & 로보틱스 (T3, 9개)
| ID | 가설 제목 | 스택 | 성격 | 핵심 기업 | 주요 연관 테제 |
|:---|:---|:---:|:---:|:---|:---|
| **[[T3-01-전고체-배터리의-변화|T3-01]]** | 전고체 배터리의 변화 | `L0` | `🚀 주류` | `[[Company-삼성SDI\|삼성SDI]]`, `[[Company-현대차\|현대차]]` | `[[T3-03-휴머노이드-로봇과-액추에이터-공급망|T3-03]]`, `[[T2-06-ESS와-한국배터리의-미국수혜|T2-06]]` |
| **[[T3-02-온디바이스-AI의-변화|T3-02]]** | 온디바이스 AI의 변화 | `L5` | `🚀 주류` | `[[Company-Apple\|Apple]]`, `[[Company-Qualcomm\|Qualcomm]]` | `[[T3-06-행동형-AI-에이전트와-모바일-교체-슈퍼사이클|T3-06]]`, `[[T3-07-AI-PC-보급-확대와-Arm-기반-윈도우-생태계|T3-07]]` |
| **[[T3-03-휴머노이드-로봇과-액추에이터-공급망|T3-03]]** | 휴머노이드 로봇과 액추에이터 | `L5` | `🚀 주류` | `[[Company-Tesla\|Tesla]]`, `[[Company-BostonDynamics\|Boston Dynamics]]` | `[[T3-05-피지컬-AI와-공간지능-반도체|T3-05]]`, `[[T3-09-피지컬AI와-로봇의-상용화|T3-09]]` |
| **[[T3-04-End-to-End-AI-자율주행과-로보택시|T3-04]]** | End-to-End AI 자율주행과 로보택시 | `L5` | `🚀 주류` | `[[Company-Tesla\|Tesla]]`, `[[Company-Alphabet\|Waymo]]` | `[[T3-02-온디바이스-AI의-변화|T3-02]]`, `[[T3-05-피지컬-AI와-공간지능-반도체|T3-05]]` |
| **[[T3-05-피지컬-AI와-공간지능-반도체|T3-05]]** | 피지컬 AI와 공간지능 반도체 | `L1` | `🚀 주류` | `[[Company-NVIDIA\|NVIDIA]]`, `[[Company-Qualcomm\|Qualcomm]]` | `[[T3-03-휴머노이드-로봇과-액추에이터-공급망|T3-03]]`, `[[T3-04-End-to-End-AI-자율주행과-로보택시|T3-04]]` |
| **[[T3-06-행동형-AI-에이전트와-모바일-교체-슈퍼사이클|T3-06]]** | 행동형 AI 에이전트와 모바일 교체 | `L5` | `🚀 주류` | `[[Company-Apple\|Apple]]`, `[[Company-삼성전자\|삼성전자]]` | `[[T3-02-온디바이스-AI의-변화|T3-02]]`, `[[T3-07-AI-PC-보급-확대와-Arm-기반-윈도우-생태계|T3-07]]` |
| **[[T3-07-AI-PC-보급-확대와-Arm-기반-윈도우-생태계|T3-07]]** | AI PC 보급 확대와 Arm 기반 윈도우 | `L5` | `🚀 주류` | `[[Company-Qualcomm\|Qualcomm]]`, `[[Company-Microsoft\|Microsoft]]` | `[[T3-02-온디바이스-AI의-변화|T3-02]]`, `[[T3-06-행동형-AI-에이전트와-모바일-교체-슈퍼사이클|T3-06]]` |
| **[[T3-08-AI-스마트-글래스와-경량-AR-광학계|T3-08]]** | AI 스마트 글래스와 경량 AR 광학계 | `L5` | `🚀 주류` | `[[Company-Meta\|Meta]]`, `[[Company-Apple\|Apple]]` | `[[T3-02-온디바이스-AI의-변화|T3-02]]`, `[[T3-05-피지컬-AI와-공간지능-반도체|T3-05]]` |
| **[[T3-09-피지컬AI와-로봇의-상용화|T3-09]]** | 피지컬 AI와 로봇의 상용화 | `L5` | `🚀 주류` | `[[Company-현대차\|현대차]]`, `[[Company-두산로보틱스\|두산로보틱스]]` | `[[T3-01-전고체-배터리의-변화|T3-01]]`, `[[T3-03-휴머노이드-로봇과-액추에이터-공급망|T3-03]]` |

### 4. 🏛️ 매크로 자본시장, 금리 & 밸류에이션 (T4, 5개)
| ID | 가설 제목 | 스택 | 성격 | 핵심 기업 | 주요 연관 테제 |
|:---|:---|:---:|:---:|:---|:---|
| **[[T4-01-금리와-데이터센터|T4-01]]** | 금리와 데이터센터 (CAPEX ROI) | `L3` | `🛡️ 헷지` | `[[Company-Microsoft\|Microsoft]]`, `[[Company-Amazon\|Amazon]]` | `[[T2-01-데이터센터의-변화|T2-01]]`, `[[T4-02-엔비디아와-네오클라우드|T4-02]]`, `[[T4-04-AI-버블-가능성|T4-04]]` |
| **[[T4-02-엔비디아와-네오클라우드|T4-02]]** | 엔비디아와 네오클라우드 | `L3` | `🚀 주류` | `[[Company-CoreWeave\|CoreWeave]]`, `[[Company-NVIDIA\|NVIDIA]]` | `[[T2-01-데이터센터의-변화|T2-01]]`, `[[T4-01-금리와-데이터센터|T4-01]]`, `[[T4-03-엔비디아와-GPU-금융|T4-03]]` |
| **[[T4-03-엔비디아와-GPU-금융|T4-03]]** | 엔비디아와 GPU 금융 | `L3` | `🛡️ 헷지` | `[[Company-Blackstone\|Blackstone]]`, `[[Company-CoreWeave\|CoreWeave]]` | `[[T4-02-엔비디아와-네오클라우드|T4-02]]`, `[[T4-04-AI-버블-가능성|T4-04]]` |
| **[[T4-04-AI-버블-가능성|T4-04]]** | AI 버블 가능성 (CAPEX ROI 불일치) | `L3` | `🛡️ 헷지` | `[[Company-NVIDIA\|NVIDIA]]`, `[[Company-BigTech\|빅테크]]` | `[[T4-01-금리와-데이터센터|T4-01]]`, `[[T4-02-엔비디아와-네오클라우드|T4-02]]`, `[[T4-03-엔비디아와-GPU-금융|T4-03]]` |
| **[[T4-05-10년금리-5%-재진입-가능성|T4-05]]** | 10년 금리 5% 재진입 가능성 | `L6` | `🛡️ 헷지` | `[[Company-US_Treasury\|미국채]]`, `[[Company-Fed\|연준]]` | `[[T4-01-금리와-데이터센터|T4-01]]`, `[[T4-04-AI-버블-가능성|T4-04]]` |

### 5. 💻 AI 엔터프라이즈 SW & 버티컬 에이전트 (T5, 3개)
| ID | 가설 제목 | 스택 | 성격 | 핵심 기업 | 주요 연관 테제 |
|:---|:---|:---:|:---:|:---|:---|
| **[[T5-01-오픈소스-모델-고도화와-온프레미스-사설-AI|T5-01]]** | 오픈소스 모델 고도화와 온프레미스 | `L4` | `🚀 주류` | `[[Company-Meta\|Meta]]`, `[[Company-Dell\|Dell]]` | `[[T3-02-온디바이스-AI의-변화|T3-02]]`, `[[T6-01-소버린-AI와-국가-단위-컴퓨트-인프라|T6-01]]` |
| **[[T5-02-AI-소프트웨어-레이어의-과점화|T5-02]]** | AI 소프트웨어 레이어의 과점화 | `L4` | `🚀 주류` | `[[Company-Microsoft\|Microsoft]]`, `[[Company-Alphabet\|Alphabet]]` | `[[T1-02-TPU-증가와-GPU-수요-둔화|T1-02]]`, `[[T4-02-엔비디아와-네오클라우드|T4-02]]` |
| **[[T5-03-바이오AI와-신약개발-가속|T5-03]]** | 바이오 AI와 신약 개발 가속 | `L4` | `🚀 주류` | `[[Company-Recursion\|Recursion]]`, `[[Company-Schrodinger\|Schrodinger]]` | `[[T3-02-온디바이스-AI의-변화|T3-02]]`, `[[T1-07-AI-추론-시장-폭발과-LPU-ASIC-분화|T1-07]]` |

### 6. 🌐 지정학, 소버린 AI & 공급망 안보 (T6, 2개)
| ID | 가설 제목 | 스택 | 성격 | 핵심 기업 | 주요 연관 테제 |
|:---|:---|:---:|:---:|:---|:---|
| **[[T6-01-소버린-AI와-국가-단위-컴퓨트-인프라|T6-01]]** | 소버린 AI와 국가 단위 컴퓨트 | `L3` | `🚀 주류` | `[[Company-NVIDIA\|NVIDIA]]`, `[[Company-네이버\|네이버]]` | `[[T2-01-데이터센터의-변화|T2-01]]`, `[[T5-01-오픈소스-모델-고도화와-온프레미스-사설-AI|T5-01]]` |
| **[[T6-02-중국반도체의-HBM-생산가능성|T6-02]]** | 중국 반도체의 HBM 생산 가능성 | `L1` | `🛡️ 헷지` | `[[Company-CXMT\|CXMT]]`, `[[Company-SMIC\|SMIC]]` | `[[T1-01-메모리-산업의-변화|T1-01]]`, `[[T1-07-AI-추론-시장-폭발과-LPU-ASIC-분화|T1-07]]` |
"""
    moc_path.write_text(moc_content, encoding="utf-8")
    print("  📋 [Master MOC] 41개 테제 가치사슬 및 인덱스 테이블 갱신 완료")


def sync_vault_clean():
    print("\n📂 [옵시디언 볼트 동기화 및 구 파일 정리...]")
    vault_theses = VAULT / "argus" / "Theses"
    if vault_theses.exists():
        for old_f in vault_theses.glob("*.md"):
            old_f.unlink()

    from obsidian_sync import sync_all_outputs
    sync_all_outputs()
    print("  🎉 옵시디언 볼트 완전 동기화 완료!")


if __name__ == "__main__":
    execute_migration()
    update_master_moc()
    sync_vault_clean()
    print("\n✨ T2 (AI 데이터센터, 9개) & T3 (로보틱스, 9개) 전환 및 총 41개 테제 시스템 구축 완료!")
