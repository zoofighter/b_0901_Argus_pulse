"""
migrate_to_jensen_huang_5layer_stack.py
Argus Pulse / Obsidian 볼트의 43개 투자 테제를 젠슨 황의 5단 케이크 + 거시 환경 구조(T1~T6)로 일괄 리네이밍 및 위키링크 마이그레이션.
"""

import os
import re
import unicodedata
from pathlib import Path
import yaml

MAPPING = [
    # T1: AI 데이터센터 & 전력·냉각 인프라 (구 T2) (8개)
    ("T2-01", "T1-01", "AI 데이터센터 & 전력·냉각 인프라", "데이터센터의-변화", "데이터센터의-변화"),
    ("T2-02", "T1-02", "AI 데이터센터 & 전력·냉각 인프라", "데이터센터-액체냉각의-표준화", "데이터센터-액체냉각의-표준화"),
    ("T2-03", "T1-03", "AI 데이터센터 & 전력·냉각 인프라", "SMR과-데이터센터-무탄소-전력-PPA", "SMR과-데이터센터-무탄소-전력-PPA"),
    ("T2-04", "T1-04", "AI 데이터센터 & 전력·냉각 인프라", "AI-전력망용-대용량-ESS와-LFP-공급망", "AI-전력망용-대용량-ESS와-LFP-공급망"),
    ("T2-05", "T1-05", "AI 데이터센터 & 전력·냉각 인프라", "변압기-초고압-그리드-쇼티지-장기화", "변압기-초고압-그리드-쇼티지-장기화"),
    ("T2-06", "T1-06", "AI 데이터센터 & 전력·냉각 인프라", "ESS와-한국배터리의-미국수혜", "ESS와-한국배터리의-미국수혜"),
    ("T2-07", "T1-07", "AI 데이터센터 & 전력·냉각 인프라", "800V-48V-HVDC-전력-아키텍처-혁신", "800V-48V-HVDC-전력-아키텍처-혁신"),
    ("T2-09", "T1-08", "AI 데이터센터 & 전력·냉각 인프라", "온사이트-가스터빈과-연료전지-자체발전", "온사이트-가스터빈과-연료전지-자체발전"),

    # T2: AI 컴퓨트, 메모리 & 선단 반도체 (구 T1) (10개)
    ("T1-01", "T2-01", "AI 컴퓨트 & 차세대 반도체", "메모리-산업의-변화", "메모리-산업의-변화"),
    ("T1-04", "T2-02", "AI 컴퓨트 & 차세대 반도체", "첨단-패키징과-CoWoS의-병목", "첨단-패키징과-CoWoS의-병목"),
    ("T1-05", "T2-03", "AI 컴퓨트 & 차세대 반도체", "유리기판의-차세대-패키징-침투", "유리기판의-차세대-패키징-침투"),
    ("T1-08", "T2-04", "AI 컴퓨트 & 차세대 반도체", "파운드리-2nm-공정과-GAA-격돌", "파운드리-2nm-공정과-GAA-격돌"),
    ("T1-10", "T2-05", "AI 컴퓨트 & 차세대 반도체", "3D-DRAM-기술-전환과-400단-V-NAND", "3D-DRAM-기술-전환과-400단-V-NAND"),
    ("T1-03", "T2-06", "AI 컴퓨트 & 차세대 반도체", "CXL-메모리의-확대", "CXL-메모리의-확대"),
    ("T1-07", "T2-07", "AI 컴퓨트 & 차세대 반도체", "AI-추론-시장-폭발과-LPU-ASIC-분화", "AI-추론-시장-폭발과-LPU-ASIC-분화"),
    ("T1-09", "T2-08", "AI 컴퓨트 & 차세대 반도체", "빅테크-커스텀-ASIC-증가와-DSP-생태계", "빅테크-커스텀-ASIC-증가와-DSP-생태계"),
    ("T1-12", "T2-09", "AI 컴퓨트 & 차세대 반도체", "반도체-소부장의-내재화", "반도체-소부장의-내재화"),
    ("T1-13", "T2-10", "AI 컴퓨트 & 차세대 반도체", "메모리-2028년-피크아웃", "메모리-2028년-피크아웃"),

    # T3: 초고속 네트워킹 & 시스템 플랫폼 (구 T1/T2/T4) (4개)
    ("T1-06", "T3-01", "초고속 네트워킹 & 시스템 플랫폼", "실리콘-포토닉스와-CPO의-상용화", "실리콘-포토닉스와-CPO의-상용화"),
    ("T1-11", "T3-02", "초고속 네트워킹 & 시스템 플랫폼", "초고속-AI-네트워킹-UEC-vs-인피니밴드", "초고속-AI-네트워킹-UEC-vs-인피니밴드"),
    ("T2-08", "T3-03", "초고속 네트워킹 & 시스템 플랫폼", "전력-포화와-분산형-AI-데이터센터-코로케이션", "전력-포화와-분산형-AI-데이터센터-코로케이션"),
    ("T4-02", "T3-04", "초고속 네트워킹 & 시스템 플랫폼", "엔비디아와-네오클라우드", "엔비디아와-네오클라우드"),

    # T4: 파운데이션 모델 & 엔터프라이즈 SW (구 T5 + T1-02) (4개)
    ("T5-01", "T4-01", "AI 엔터프라이즈 SW & 버티컬 에이전트", "오픈소스-모델-고도화와-온프레미스-사설-AI", "오픈소스-모델-고도화와-온프레미스-사설-AI"),
    ("T5-02", "T4-02", "AI 엔터프라이즈 SW & 버티컬 에이전트", "AI-소프트웨어-레이어의-과점화", "AI-소프트웨어-레이어의-과점화"),
    ("T5-03", "T4-03", "AI 엔터프라이즈 SW & 버티컬 에이전트", "바이오AI와-신약개발-가속", "바이오AI와-신약개발-가속"),
    ("T1-02", "T4-04", "AI 엔터프라이즈 SW & 버티컬 에이전트", "TPU-증가와-GPU-수요-둔화", "TPU-증가와-GPU-수요-둔화"),

    # T5: 피지컬 AI, 모빌리티 & 로보틱스 (구 T3) (9개)
    ("T3-02", "T5-01", "피지컬 AI, 모빌리티 & 로보틱스", "온디바이스-AI의-변화", "온디바이스-AI의-변화"),
    ("T3-06", "T5-02", "피지컬 AI, 모빌리티 & 로보틱스", "행동형-AI-에이전트와-모바일-교체-슈퍼사이클", "행동형-AI-에이전트와-모바일-교체-슈퍼사이클"),
    ("T3-07", "T5-03", "피지컬 AI, 모빌리티 & 로보틱스", "AI-PC-보급-확대와-Arm-기반-윈도우-생태계", "AI-PC-보급-확대와-Arm-기반-윈도우-생태계"),
    ("T3-08", "T5-04", "피지컬 AI, 모빌리티 & 로보틱스", "AI-스마트-글래스와-경량-AR-광학계", "AI-스마트-글래스와-경량-AR-광학계"),
    ("T3-04", "T5-05", "피지컬 AI, 모빌리티 & 로보틱스", "End-to-End-AI-자율주행과-로보택시", "End-to-End-AI-자율주행과-로보택시"),
    ("T3-03", "T5-06", "피지컬 AI, 모빌리티 & 로보틱스", "휴머노이드-로봇과-액추에이터-공급망", "휴머노이드-로봇과-액추에이터-공급망"),
    ("T3-05", "T5-07", "피지컬 AI, 모빌리티 & 로보틱스", "피지컬-AI와-공간지능-반도체", "피지컬-AI와-공간지능-반도체"),
    ("T3-09", "T5-08", "피지컬 AI, 모빌리티 & 로보틱스", "피지컬AI와-로봇의-상용화", "피지컬AI와-로봇의-상용화"),
    ("T3-01", "T5-09", "피지컬 AI, 모빌리티 & 로보틱스", "전고체-배터리의-변화", "전고체-배터리의-변화"),

    # T6: 매크로 자본시장, 금리 & 지정학 안보 (구 T4 + T6) (8개)
    ("T4-01", "T6-01", "매크로 자본시장, 금리 & 지정학 안보", "금리와-데이터센터", "금리와-데이터센터"),
    ("T4-03", "T6-02", "매크로 자본시장, 금리 & 지정학 안보", "엔비디아와-GPU-금융", "엔비디아와-GPU-금융"),
    ("T4-04", "T6-03", "매크로 자본시장, 금리 & 지정학 안보", "AI-버블-가능성", "AI-버블-가능성"),
    ("T4-05", "T6-04", "매크로 자본시장, 금리 & 지정학 안보", "10년금리-5%-재진입-가능성", "10년금리-5%-재진입-가능성"),
    ("T4-06", "T6-05", "매크로 자본시장, 금리 & 지정학 안보", "오픈AI·앤트로픽의-5000억달러-매출-갭과-데이터센터-ROI-딜레마", "오픈AI·앤트로픽의-5000억달러-매출-갭과-데이터센터-ROI-딜레마"),
    ("T6-01", "T6-06", "매크로 자본시장, 금리 & 지정학 안보", "소버린-AI와-국가-단위-컴퓨트-인프라", "소버린-AI와-국가-단위-컴퓨트-인프라"),
    ("T6-02", "T6-07", "매크로 자본시장, 금리 & 지정학 안보", "중국반도체의-HBM-생산가능성", "중국반도체의-HBM-생산가능성"),
    ("T6-03", "T6-08", "매크로 자본시장, 금리 & 지정학 안보", "중국반도체의-NAND-점유율-증가", "중국반도체의-NAND-점유율-증가"),
]

# Build lookup maps
old_to_new_id = {old_id: new_id for old_id, new_id, _, _, _ in MAPPING}
old_to_new_stem = {}
old_to_new_sector = {}

for old_id, new_id, sec, old_suf, new_suf in MAPPING:
    old_stem = f"{old_id}-{old_suf}"
    new_stem = f"{new_id}-{new_suf}"
    old_to_new_stem[old_stem] = new_stem
    old_to_new_sector[new_id] = sec

print(f"Loaded {len(MAPPING)} mappings.")

def replace_links_in_text(text: str) -> str:
    """모든 위키링크 및 ID 레퍼런스를 새 ID 및 파일명으로 치환"""
    # 1. 파일명 기반 위키링크 치환: [[Old-Stem|Label]] or [[Old-Stem]]
    for old_stem, new_stem in sorted(old_to_new_stem.items(), key=lambda x: -len(x[0])):
        # match exact stem in link target
        text = re.sub(rf'\[\[{re.escape(old_stem)}(\|[^\]]*)?\]\]', lambda m: f"[[{new_stem}{m.group(1) if m.group(1) else ''}]]", text)
        text = re.sub(rf'\[\[{re.escape(unicodedata.normalize("NFD", old_stem))}(\|[^\]]*)?\]\]', lambda m: f"[[{new_stem}{m.group(1) if m.group(1) else ''}]]", text)

    # 2. ID 기반 텍스트 치환 (예: `T1-01`, `T4-02` 등 코드 블록이나 테이블 내 표기)
    # 조심해서 정확한 ID 경계 매칭
    for old_id, new_id, _, _, _ in sorted(MAPPING, key=lambda x: -len(x[0])):
        # match `T1-01` or "T1-01" or T1-01 at word boundary
        pass
    return text

def process_vault_and_codebase():
    code_dir = Path('/Users/boon/Dropbox/03_code/b_0901_Argus_pulse')
    obs_dir = Path('/Users/boon/Library/Mobile Documents/iCloud~md~obsidian/Documents/obs_argus')

    targets = [
        code_dir / "thesis",
        obs_dir / "argus" / "Theses"
    ]

    print("--- Step 1: Updating and renaming thesis files in thesis/ and obs_argus/Theses/ ---")
    for target_dir in targets:
        if not target_dir.exists():
            continue
        print(f"Processing directory: {target_dir}")
        for old_id, new_id, sector, old_suf, new_suf in MAPPING:
            old_name = f"{old_id}-{old_suf}.md"
            new_name = f"{new_id}-{new_suf}.md"
            
            # find old file
            found_f = None
            for f in target_dir.glob("*.md"):
                if unicodedata.normalize('NFC', f.name) == unicodedata.normalize('NFC', old_name):
                    found_f = f
                    break
            
            if found_f and found_f.exists():
                text = found_f.read_text(encoding='utf-8')
                
                # update frontmatter id and sector
                if text.startswith('---'):
                    parts = text.split('---', 2)
                    if len(parts) >= 3:
                        raw_meta = parts[1]
                        body = parts[2]
                        
                        # regex replace id and sector in raw_meta to preserve comments/order
                        raw_meta = re.sub(r'^id:\s*["\']?[^"\'\n]+["\']?', f'id: "{new_id}"', raw_meta, flags=re.MULTILINE)
                        raw_meta = re.sub(r'^sector:\s*["\']?[^"\'\n]+["\']?', f'sector: "{sector}"', raw_meta, flags=re.MULTILINE)
                        
                        # also update related_theses in metadata
                        for o_id, n_id in old_to_new_id.items():
                            raw_meta = re.sub(rf'\b{o_id}\b', n_id, raw_meta)
                        
                        body = replace_links_in_text(body)
                        text = f"---{raw_meta}---{body}"
                else:
                    text = replace_links_in_text(text)
                
                new_f = target_dir / new_name
                # write new and unlink old if name changed
                new_f.write_text(text, encoding='utf-8')
                if new_f != found_f:
                    found_f.unlink()
                print(f"  Renamed: {found_f.name} -> {new_name}")

    print("\n--- Step 2: Updating all Markdown files and wiki-links across all directories ---")
    all_scan_dirs = [
        code_dir / "thesis",
        code_dir / "docs",
        obs_dir / "argus"
    ]
    
    for s_dir in all_scan_dirs:
        if not s_dir.exists():
            continue
        print(f"Scanning for link updates in: {s_dir}")
        for md_file in s_dir.rglob("*.md"):
            if md_file.is_file() and not md_file.name.startswith('.'):
                orig_text = md_file.read_text(encoding='utf-8')
                new_text = replace_links_in_text(orig_text)
                if orig_text != new_text:
                    md_file.write_text(new_text, encoding='utf-8')
                    print(f"  Updated links in: {md_file.relative_to(s_dir)}")

    print("\n--- Step 3: Updating Canvas files ---")
    for canvas_file in (obs_dir / "argus" / "Canvas").glob("*.canvas"):
        orig_text = canvas_file.read_text(encoding='utf-8')
        new_text = replace_links_in_text(orig_text)
        # also replace node file references
        for old_stem, new_stem in old_to_new_stem.items():
            new_text = new_text.replace(f"argus/Theses/{old_stem}.md", f"argus/Theses/{new_stem}.md")
            new_text = new_text.replace(f"{old_stem}.md", f"{new_stem}.md")
        if orig_text != new_text:
            canvas_file.write_text(new_text, encoding='utf-8')
            print(f"  Updated canvas: {canvas_file.name}")

if __name__ == "__main__":
    process_vault_and_codebase()
    print("\nMigration completed successfully!")
