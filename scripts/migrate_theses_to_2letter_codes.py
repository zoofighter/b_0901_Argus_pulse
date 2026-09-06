"""
scripts/migrate_theses_to_2letter_codes.py
38개 테제 파일명을 2자리 영문 섹터 코드(SC, DC, RB, SW, GE, MC)로 일괄 전환하고,
내부 메타데이터, 상호링크, Topic/Company/Vs/MOC 허브 및 파이썬 로더를 전면 갱신하여 옵시디언 볼트로 동기화.
"""

import os
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

# ── 38개 테제 구 ID ➔ 신규 2자리 섹터 ID 매핑 ───────────────────────────────
ID_MAP = {
    # 💾 SC (Silicon & Compute / 반도체) - 13개
    "T-02": ("SC-01", "메모리-산업의-변화", "메모리 산업의 변화", "AI 컴퓨트 & 차세대 반도체", "S1", "consensus", "L1 (칩/패키징)", "L1", ["KR", "US", "TW"], "2026~2027", ["Vs-TSMC동맹-vs-삼성턴키"]),
    "T-06": ("SC-02", "TPU-증가와-GPU-수요-둔화", "TPU 증가와 GPU 수요 둔화", "AI 컴퓨트 & 차세대 반도체", "S1", "contrarian", "L1 (칩/패키징)", "L1", ["US", "TW"], "2026~2027", ["Vs-GPU-vs-TPU-ASIC"]),
    "T-07": ("SC-03", "CXL-메모리의-확대", "CXL 메모리의 확대", "AI 컴퓨트 & 차세대 반도체", "S1", "consensus", "L1 (칩/패키징)", "L1", ["KR", "US"], "2026H2~2027", []),
    "T-10": ("SC-04", "첨단-패키징과-CoWoS의-병목", "첨단 패키징과 CoWoS의 병목", "AI 컴퓨트 & 차세대 반도체", "S1", "consensus", "L1 (칩/패키징)", "L1", ["TW", "KR", "US"], "2026~2027", ["Vs-TSMC동맹-vs-삼성턴키"]),
    "T-11": ("SC-05", "유리기판의-차세대-패키징-침투", "유리기판의 차세대 패키징 침투", "AI 컴퓨트 & 차세대 반도체", "S1", "consensus", "L0 (소부장/기판)", "L0", ["KR", "US"], "2027~2028", []),
    "T-14": ("SC-06", "실리콘-포토닉스와-CPO의-상용화", "실리콘 포토닉스와 CPO의 상용화", "AI 컴퓨트 & 차세대 반도체", "S1", "consensus", "L3 (네트워킹)", "L3", ["US", "TW"], "2027~2028", ["Vs-인피니밴드-vs-울트라이더넷"]),
    "T-15": ("SC-07", "AI-추론-시장-폭발과-LPU-ASIC-분화", "AI 추론 시장 폭발과 LPU·ASIC 분화", "AI 컴퓨트 & 차세대 반도체", "S1", "consensus", "L1 (칩/패키징)", "L1", ["US", "KR"], "2026~2027", ["Vs-GPU-vs-TPU-ASIC"]),
    "T-16": ("SC-08", "파운드리-2nm-공정과-GAA-격돌", "파운드리 2nm 공정과 GAA 격돌", "AI 컴퓨트 & 차세대 반도체", "S1", "consensus", "L1 (칩/패키징)", "L1", ["TW", "KR", "US"], "2026H2~2027", ["Vs-TSMC동맹-vs-삼성턴키"]),
    "T-24": ("SC-09", "빅테크-커스텀-ASIC-증가와-DSP-생태계", "빅테크 커스텀 ASIC 증가와 DSP 생태계", "AI 컴퓨트 & 차세대 반도체", "S1", "consensus", "L1 (칩/패키징)", "L1", ["US", "KR", "TW"], "2026~2027", ["Vs-GPU-vs-TPU-ASIC"]),
    "T-28": ("SC-10", "3D-DRAM-기술-전환과-400단-V-NAND", "3D DRAM 기술 전환과 400단 V-NAND", "AI 컴퓨트 & 차세대 반도체", "S1", "consensus", "L1 (칩/패키징)", "L1", ["KR", "US"], "2027~2029", []),
    "T-29": ("SC-11", "초고속-AI-네트워킹-UEC-vs-인피니밴드", "초고속 AI 네트워킹 UEC vs 인피니밴드", "AI 컴퓨트 & 차세대 반도체", "S1", "consensus", "L3 (네트워킹)", "L3", ["US"], "2026~2027", ["Vs-인피니밴드-vs-울트라이더넷"]),
    "T-33": ("SC-12", "반도체-소부장의-내재화", "반도체 소부장의 내재화", "AI 컴퓨트 & 차세대 반도체", "S1", "consensus", "L0 (소부장)", "L0", ["KR"], "2026~2027", []),
    "T-35": ("SC-13", "메모리-2028년-피크아웃", "메모리 2028년 피크아웃", "AI 컴퓨트 & 차세대 반도체", "S1", "contrarian", "L1 (칩/패키징)", "L1", ["KR", "US"], "2027H2~2028", []),

    # ⚡ DC (Data Center & Power Infra / 전력·인프라) - 6개
    "T-01": ("DC-01", "데이터센터의-변화", "데이터센터의 변화", "AI 데이터센터 & 전력·냉각 인프라", "S2", "consensus", "L2 (물리인프라)", "L2", ["US", "KR"], "2026~2027", ["Vs-공랭-vs-액체냉각"]),
    "T-12": ("DC-02", "데이터센터-액체냉각의-표준화", "데이터센터 액체냉각의 표준화", "AI 데이터센터 & 전력·냉각 인프라", "S2", "consensus", "L2 (물리인프라)", "L2", ["US", "KR"], "2026~2027", ["Vs-공랭-vs-액체냉각"]),
    "T-13": ("DC-03", "SMR과-데이터센터-무탄소-전력-PPA", "SMR과 데이터센터 무탄소 전력 PPA", "AI 데이터센터 & 전력·냉각 인프라", "S2", "consensus", "L2 (물리인프라)", "L2", ["US", "KR"], "2027~2028", []),
    "T-22": ("DC-04", "AI-전력망용-대용량-ESS와-LFP-공급망", "AI 전력망용 대용량 ESS와 LFP 공급망", "AI 데이터센터 & 전력·냉각 인프라", "S2", "consensus", "L2 (물리인프라)", "L2", ["KR", "US", "CN"], "2026~2027", []),
    "T-23": ("DC-05", "변압기-초고압-그리드-쇼티지-장기화", "변압기·초고압 그리드 쇼티지 장기화", "AI 데이터센터 & 전력·냉각 인프라", "S2", "consensus", "L2 (물리인프라)", "L2", ["KR", "US", "EU"], "2026~2028", []),
    "T-32": ("DC-06", "ESS와-한국배터리의-미국수혜", "ESS와 한국 배터리의 미국 수혜", "AI 데이터센터 & 전력·냉각 인프라", "S2", "consensus", "L0 (소재/배터리)", "L0", ["KR", "US"], "2026~2027", []),

    # 🤖 RB (Robotics & Physical AI / 로보틱스·디바이스) - 9개
    "T-03": ("RB-01", "전고체-배터리의-변화", "전고체 배터리의 변화", "피지컬 AI, 모빌리티 & 로보틱스", "S3", "consensus", "L0 (소재/배터리)", "L0", ["KR", "JP", "US"], "2026H2~2028", []),
    "T-04": ("RB-02", "온디바이스-AI의-변화", "온디바이스 AI의 변화", "피지컬 AI, 모빌리티 & 로보틱스", "S3", "consensus", "L5 (디바이스)", "L5", ["US", "KR"], "2026~2027", []),
    "T-17": ("RB-03", "휴머노이드-로봇과-액추에이터-공급망", "휴머노이드 로봇과 액추에이터 공급망", "피지컬 AI, 모빌리티 & 로보틱스", "S3", "consensus", "L5 (디바이스)", "L5", ["US", "KR"], "2027~2029", []),
    "T-18": ("RB-04", "End-to-End-AI-자율주행과-로보택시", "End-to-End AI 자율주행과 로보택시", "피지컬 AI, 모빌리티 & 로보틱스", "S3", "consensus", "L5 (디바이스)", "L5", ["US", "KR"], "2026~2027", []),
    "T-19": ("RB-05", "피지컬-AI와-공간지능-반도체", "피지컬 AI와 공간지능 반도체", "피지컬 AI, 모빌리티 & 로보틱스", "S3", "consensus", "L1 (칩/패키징)", "L1", ["US", "JP"], "2026~2028", []),
    "T-20": ("RB-06", "행동형-AI-에이전트와-모바일-교체-슈퍼사이클", "행동형 AI 에이전트와 모바일 교체 슈퍼사이클", "피지컬 AI, 모빌리티 & 로보틱스", "S3", "consensus", "L5 (디바이스)", "L5", ["US", "KR"], "2026~2027", []),
    "T-21": ("RB-07", "AI-PC-보급-확대와-Arm-기반-윈도우-생태계", "AI PC 보급 확대와 Arm 기반 윈도우 생태계", "피지컬 AI, 모빌리티 & 로보틱스", "S3", "consensus", "L5 (디바이스)", "L5", ["US"], "2026~2027", []),
    "T-27": ("RB-08", "AI-스마트-글래스와-경량-AR-광학계", "AI 스마트 글래스와 경량 AR 광학계", "피지컬 AI, 모빌리티 & 로보틱스", "S3", "consensus", "L5 (디바이스)", "L5", ["US", "KR"], "2026~2027", []),
    "T-30": ("RB-09", "피지컬AI와-로봇의-상용화", "피지컬 AI와 로봇의 상용화", "피지컬 AI, 모빌리티 & 로보틱스", "S3", "consensus", "L5 (디바이스)", "L5", ["KR", "US"], "2026~2028", []),

    # 💻 SW (Software & Agents / 엔터프라이즈 SW) - 3개
    "T-25": ("SW-01", "오픈소스-모델-고도화와-온프레미스-사설-AI", "오픈소스 모델 고도화와 온프레미스 사설 AI", "AI 엔터프라이즈 SW & 버티컬 에이전트", "S4", "consensus", "L4 (모델/SW)", "L4", ["US"], "2026~2027", []),
    "T-31": ("SW-02", "AI-소프트웨어-레이어의-과점화", "AI 소프트웨어 레이어의 과점화", "AI 엔터프라이즈 SW & 버티컬 에이전트", "S4", "consensus", "L4 (모델/SW)", "L4", ["US"], "2026~2027", []),
    "T-34": ("SW-03", "바이오AI와-신약개발-가속", "바이오 AI와 신약 개발 가속", "AI 엔터프라이즈 SW & 버티컬 에이전트", "S4", "consensus", "L4 (모델/SW)", "L4", ["US", "KR"], "2026~2028", []),

    # 🌐 GE (Geopolitics & Sovereign / 지정학·소버린) - 2개
    "T-26": ("GE-01", "소버린-AI와-국가-단위-컴퓨트-인프라", "소버린 AI와 국가 단위 컴퓨트 인프라", "지정학, 소버린 AI & 공급망 안보", "S5", "consensus", "L3 (클라우드)", "L3", ["Global", "KR", "US"], "2026~2028", []),
    "T-36": ("GE-02", "중국반도체의-HBM-생산가능성", "중국 반도체의 HBM 생산 가능성", "지정학, 소버린 AI & 공급망 안보", "S5", "contrarian", "L1 (칩/패키징)", "L1", ["CN", "KR"], "2026~2027", []),

    # 🏛️ MC (Macro & Markets / 매크로·자본시장) - 5개
    "T-05": ("MC-01", "금리와-데이터센터", "금리와 데이터센터", "매크로 자본시장, 금리 & 밸류에이션", "S6", "contrarian", "L3 (클라우드)", "L3", ["US"], "2026~2027", []),
    "T-08": ("MC-02", "엔비디아와-네오클라우드", "엔비디아와 네오클라우드", "매크로 자본시장, 금리 & 밸류에이션", "S6", "consensus", "L3 (클라우드)", "L3", ["US"], "2026~2027", ["Vs-GPU-vs-TPU-ASIC"]),
    "T-09": ("MC-03", "엔비디아와-GPU-금융", "엔비디아와 GPU 금융", "매크로 자본시장, 금리 & 밸류에이션", "S6", "contrarian", "L3 (클라우드)", "L3", ["US"], "2026~2027", []),
    "T-37": ("MC-04", "AI-버블-가능성", "AI 버블 가능성", "매크로 자본시장, 금리 & 밸류에이션", "S6", "contrarian", "L3 (클라우드)", "L3", ["US"], "2026~2027", []),
    "T-38": ("MC-05", "10년금리-5%-재진입-가능성", "10년 금리 5% 재진입 가능성", "매크로 자본시장, 금리 & 밸류에이션", "S6", "contrarian", "L6 (매크로)", "L6", ["US"], "2026~2027", []),
}

# 구 ID ➔ 신규 ID 매핑 딕셔너리
OLD_TO_NEW_ID = {k: v[0] for k, v in ID_MAP.items()}
OLD_TO_NEW_FILE = {k: f"{v[0]}-{v[1]}.md" for k, v in ID_MAP.items()}


def update_code_loaders():
    """thesis_loader.py와 obsidian_sync.py의 탐색 패턴 수정"""
    loader_path = ROOT_DIR / "thesis_loader.py"
    if loader_path.exists():
        content = loader_path.read_text(encoding="utf-8")
        # THESIS_DIR.glob("T-*.md") -> THESIS_DIR.glob("*.md") 필터링
        new_content = content.replace('for md_file in sorted(THESIS_DIR.glob("T-*.md")):', 'for md_file in sorted([f for f in THESIS_DIR.glob("*.md") if not f.name.startswith(("00-", "Topic-", "Company-", "Vs-"))]):')
        new_content = new_content.replace('for md_file in THESIS_DIR.glob("T-*.md"):', 'for md_file in [f for f in THESIS_DIR.glob("*.md") if not f.name.startswith(("00-", "Topic-", "Company-", "Vs-"))]:')
        loader_path.write_text(new_content, encoding="utf-8")
        print("  🔧 [thesis_loader.py] 다중 접두사 지원 완료")


def migrate_thesis_files():
    """모든 38개 테제 파일명 변경 및 내부 링크 일괄 갱신"""
    # 1. 기존 T-*.md 파일 읽기
    existing_files = list(THESIS_DIR.glob("T-*.md"))
    print(f"\n📂 총 {len(existing_files)}개 기존 테제 파일 변환 시작...")

    for p in existing_files:
        raw_text = p.read_text(encoding="utf-8")
        if not raw_text.startswith("---"):
            continue
        parts = raw_text.split("---", 2)
        if len(parts) < 3:
            continue

        meta = yaml.safe_load(parts[1]) or {}
        body = parts[2].lstrip("\r\n")

        old_id = meta.get("id")
        if old_id not in ID_MAP:
            # 혹시 매핑에 없는 경우 안전 처리
            continue

        new_id, slug, title, sector, sector_id, nature, stack_name, stack_layer, geo, horizon, vs_list = ID_MAP[old_id]
        new_filename = f"{new_id}-{slug}.md"

        # 메타데이터 업데이트
        meta["id"] = new_id
        meta["old_id"] = old_id
        meta["title"] = title
        meta["sector"] = sector
        meta["sector_id"] = sector_id
        meta["thesis_nature"] = nature
        meta["stack_layer"] = stack_layer
        meta["stack_name"] = stack_name
        meta["geography"] = geo
        meta["time_horizon"] = horizon
        meta["related_vs"] = vs_list

        # Aliases 구성: 신규 ID, 신규 풀네임, 구 ID, 구 풀네임, 한글제목 모두 등록
        aliases = meta.get("aliases", [])
        for a in [new_id, f"{new_id} {title}", old_id, f"{old_id} {title}", title]:
            if a not in aliases:
                aliases.append(a)
        meta["aliases"] = aliases

        # related_theses 신규 ID로 변환
        new_rel = []
        for r in meta.get("related_theses", []):
            new_rel.append(OLD_TO_NEW_ID.get(r, r))
        meta["related_theses"] = new_rel

        # 본문 내 구 ID 링크 치환 (예: [[T-02...]] -> [[SC-01...]])
        updated_body = body
        # 제목 헤더 치환
        for old_k, (n_id, s_name, t_name, *_) in ID_MAP.items():
            old_file_pattern = f"{old_k}-"
            new_file_pattern = f"{n_id}-{s_name}"
            # [[T-XX-파일명|...]] 치환
            for old_f in OLD_TO_NEW_FILE.keys():
                updated_body = updated_body.replace(f"[[{old_f}", f"[[{OLD_TO_NEW_FILE[old_f].replace('.md', '')}")
            updated_body = updated_body.replace(f"# {old_k} ", f"# {n_id} ")
            updated_body = updated_body.replace(f"{old_k} {t_name}", f"{n_id} {t_name}")
            updated_body = updated_body.replace(f'contains(thesis, "{old_k}")', f'contains(thesis, "{n_id}") OR contains(thesis, "{old_k}")')

        # 새 파일 저장
        new_path = THESIS_DIR / new_filename
        yaml_str = yaml.dump(meta, allow_unicode=True, sort_keys=False)
        new_path.write_text(f"---\n{yaml_str}---\n\n{updated_body}", encoding="utf-8")
        
        # 구 파일 삭제
        p.unlink()
        print(f"  ✅ [변환 완료] {old_id} ➔ {new_id} ({new_filename})")


def update_all_hubs_and_moc():
    """Topic, Company, Vs Hubs 및 Master MOC 내의 구 테제 링크를 신규 ID로 일괄 치환"""
    print("\n🔄 모든 Hub 문서 및 Master MOC 링크 최신화 중...")

    # 모든 MD 파일 대상 치환
    for f in THESIS_DIR.glob("*.md"):
        content = f.read_text(encoding="utf-8")
        modified = False
        for old_id, (new_id, slug, title, *_) in ID_MAP.items():
            new_fname = f"{new_id}-{slug}"
            if old_id in content:
                # 위키링크 치환
                content = content.replace(f"[[{old_id}-", f"[[{new_fname}")
                content = content.replace(f"|{old_id}]]", f"|{new_id}]]")
                content = content.replace(f"|{old_id} ", f"|{new_id} ")
                content = content.replace(f'"{old_id}"', f'"{new_id}"')
                content = content.replace(f"'{old_id}'", f"'{new_id}'")
                modified = True

        if modified:
            f.write_text(content, encoding="utf-8")
            print(f"  📝 [허브 갱신] {f.name}")


def sync_to_vault_clean():
    """옵시디언 볼트의 Theses 폴더를 신규 파일들로 교체 및 일괄 동기화"""
    if not VAULT.exists():
        print(f"  ❌ 옵시디언 볼트 경로 없음: {VAULT}")
        return

    print(f"\n📂 [옵시디언 볼트 동기화 진행 중...]")
    vault_theses = VAULT / "argus" / "Theses"
    if vault_theses.exists():
        # 기존 구 T-*.md 파일들 정리
        for old_f in vault_theses.glob("T-*.md"):
            old_f.unlink()

    # obsidian_sync 실행
    from obsidian_sync import sync_all_outputs
    sync_all_outputs()
    print("  🎉 옵시디언 볼트 완전 동기화 완료!")


if __name__ == "__main__":
    print("🚀 [Argus Pulse] 2자리 섹터 코드(SC, DC, RB, SW, GE, MC) 마이그레이션 시작\n")
    update_code_loaders()
    migrate_thesis_files()
    update_all_hubs_and_moc()
    sync_to_vault_clean()
    print("\n✨ 모든 테제 이름이 섹터별 2자리 코드로 완벽하게 재정의되었습니다!")
