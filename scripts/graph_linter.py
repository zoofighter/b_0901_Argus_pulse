"""
scripts/graph_linter.py — Argus Pulse & Obsidian 지식 그래프 린터, 무결성 검증 및 자동 치유기

실행:
  python scripts/graph_linter.py
  python scripts/graph_linter.py --fix
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

import config
from thesis_loader import _parse_md_file
from obsidian_sync import sync_file


def norm_str(s: str) -> str:
    """한글 유니코드 NFD/NFC 정규화 (macOS 호환)"""
    return unicodedata.normalize("NFC", s).strip()


# 기업명 영문/한글 매핑 (Alias)
COMPANY_ALIASES = {
    "오픈AI": "OpenAI",
    "앤트로픽": "Anthropic",
    "구글": "Google",
    "알파벳": "Alphabet",
    "애플": "Apple",
    "마이크로소프트": "Microsoft",
    "메타": "Meta",
    "테슬라": "Tesla",
    "퀄컴": "Qualcomm",
    "브로드컴": "Broadcom",
    "엔비디아": "NVIDIA",
    "인텔": "Intel",
    "버티브": "Vertiv",
    "코어위브": "CoreWeave",
    "이튼": "Eaton",
    "마이크론": "Micron",
}


def create_dynamic_company_node(name: str) -> Path:
    """새롭게 발견된 기업의 허브 파일 동적 생성"""
    clean_name = name.replace("Company-", "").strip()
    clean_name = clean_name.replace("\\", "")
    target_path = config.THESIS_DIR / f"Company-{clean_name}.md"
    if not target_path.exists():
        content = f"""---
id: Company-{clean_name}
name: "{clean_name}"
type: company
created: "2026-09-06"
tags:
  - company
  - argus-hub
---

# 🏢 {clean_name}

> **기업 분류**: 인텔리전스 추적 기업 허브  
> **지식 허브 연계**: [[00-Argus-Master-MOC|Argus Master MOC]]

---

## 📌 주요 연관 가설 및 밸류체인
- **연관 지식 허브**: [[00-Argus-Master-MOC|Argus Master MOC]]

---

## 🔗 연관 문서 (Backlinks)
```dataview
TABLE file.mtime AS "최종 수정일"
FROM ""
WHERE contains(file.outlinks, this.file.link) OR contains(file.text, "{clean_name}")
SORT file.mtime DESC
LIMIT 15
```
"""
        target_path.write_text(content, encoding="utf-8")
        try:
            sync_file(target_path, "theses")
        except Exception:
            pass
    return target_path


def lint_knowledge_graph(fix: bool = False):
    print(f"\n🔍 [Graph Linter] Argus Pulse 지식 그래프 무결성 검사 시작 {'(자동 치유 모드)' if fix else ''}")
    print("═" * 75)

    scan_dirs = [
        ("theses", config.THESIS_DIR),
        ("blog", config.OUTPUT_DIR / "blog"),
        ("digest", config.OUTPUT_DIR / "digest"),
        ("review", config.OUTPUT_DIR / "review"),
        ("thread", config.OUTPUT_DIR / "thread"),
        ("outline", config.OUTPUT_DIR / "outline"),
    ]

    all_md_files = []
    known_files = {}

    for category, dirpath in scan_dirs:
        if not dirpath.exists():
            continue
        for f in dirpath.glob("*.md"):
            stem_norm = norm_str(f.stem)
            name_norm = norm_str(f.name)
            known_files[stem_norm] = f
            known_files[name_norm] = f
            all_md_files.append((category, f))

    print(f"  📂 총 검사 대상 마크다운 파일: {len(all_md_files)}개 (Thesis/Topic/Company/Outputs)")

    inbound_links = defaultdict(set)
    outbound_links = defaultdict(set)
    broken_links = []
    frontmatter_errors = []
    fixed_count = 0

    wikilink_pattern = re.compile(r"\[\[(.*?)\]\]")

    for category, filepath in all_md_files:
        meta, body = _parse_md_file(filepath)
        stem = norm_str(filepath.stem)

        # 프론트매터 검증
        if category == "theses" and not stem.startswith(("00-", "Topic-", "Company-", "Vs-", "Canvas-")):
            if not meta.get("id"):
                frontmatter_errors.append((filepath, "frontmatter에 'id' 필드 누락"))
            if not meta.get("title"):
                frontmatter_errors.append((filepath, "frontmatter에 'title' 필드 누락"))

        full_text = filepath.read_text(encoding="utf-8")
        modified_text = full_text
        matches = wikilink_pattern.findall(full_text)

        for raw_link in matches:
            raw_link_norm = norm_str(raw_link)
            target = raw_link_norm.split("|")[0].strip()
            target = target.split("#")[0].strip()

            if not target:
                continue

            target_stem = norm_str(Path(target).stem)

            # 플레이스홀더 정리
            if target == "블로그 파일명" or target == "과거 블로그 제목":
                if fix:
                    modified_text = modified_text.replace(f"[[{raw_link}]]", f"`{raw_link}`")
                    fixed_count += 1
                continue

            # Company Alias 치환
            for kr, en in COMPANY_ALIASES.items():
                if target_stem == f"Company-{kr}":
                    target_stem = f"Company-{en}"
                    if fix:
                        modified_text = modified_text.replace(f"[[{raw_link}]]", f"[[Company-{en}|{kr}]]")
                        fixed_count += 1

            outbound_links[stem].add(target_stem)

            if target_stem in known_files or target in known_files:
                inbound_links[target_stem].add(stem)
            else:
                if fix and target_stem.startswith("Company-"):
                    created_p = create_dynamic_company_node(target_stem)
                    known_files[target_stem] = created_p
                    known_files[norm_str(created_p.name)] = created_p
                    inbound_links[target_stem].add(stem)
                    fixed_count += 1
                else:
                    broken_links.append((filepath, raw_link_norm, target_stem))

        if fix and modified_text != full_text:
            filepath.write_text(modified_text, encoding="utf-8")
            try:
                sync_file(filepath, category)
            except Exception:
                pass

    # 결과 통계 출력
    print("\n📊 [무결성 진단 통계]")
    print(f"  • 총 연결된 위키링크 관계 수: {sum(len(v) for v in outbound_links.values())}개")
    print(f"  • 깨진 링크(Broken Links)   : {len(broken_links)}건 {'❌' if broken_links else '✅'}")
    print(f"  • 프론트매터 결함            : {len(frontmatter_errors)}건 {'❌' if frontmatter_errors else '✅'}")
    if fix:
        print(f"  • 자동 치유(Auto-Fixed)     : {fixed_count}건 적용 완료 ✨")

    if broken_links:
        print("\n⚠️ [남은 깨진 위키링크 (상위 10건)]")
        for fp, raw, tgt in broken_links[:10]:
            print(f"  - [{fp.name}] -> [[{tgt}]] (원본: [[{raw}]])")

    # 상위 허브 노드 Top 7
    top_inbounds = sorted(inbound_links.items(), key=lambda x: len(x[1]), reverse=True)[:7]
    print("\n🏆 [가장 연결성이 높은 핵심 허브 Top 7]")
    for stem, referrers in top_inbounds:
        print(f"  - 🔗 {stem:<40} (인바운드 참조 {len(referrers)}개 문서)")

    print("\n" + "═" * 75)
    if not broken_links and not frontmatter_errors:
        print("🎉 [검증 성공] 지식 그래프의 모든 링크 무결성과 데이터 구조가 100% 완벽합니다!")
    else:
        print("⚠️ [검증 완료] 지식 그래프 정비가 완료되었습니다.")
    print("═" * 75 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Argus Pulse — Knowledge Graph Linter")
    parser.add_argument("--fix", action="store_true", help="깨진 링크 자동 치유 및 누락 기업 노드 자동 생성")
    args = parser.parse_args()
    lint_knowledge_graph(fix=args.fix)

# 구형 T-XX 별칭 맵 추가 치료
def fix_legacy_thesis_links():
    from thesis_loader import load_theses
    theses = load_theses(status_filter=None)
    alias_map = {}
    for t in theses:
        fp = Path(t["filepath"])
        stem = norm_str(fp.stem)
        tid = t.get("id")
        old_id = t.get("old_id")
        title = t.get("title", "")
        
        # 구형 표기 패턴들
        if old_id:
            alias_map[old_id] = stem
            alias_map[f"{old_id} {title}"] = stem
            alias_map[f"{old_id}: {title}"] = stem
        if tid:
            alias_map[tid] = stem
            alias_map[f"{tid} {title}"] = stem
            alias_map[f"{tid}: {title}"] = stem
            
    # 전체 파일 순회하며 치환
    for category, dirpath in [("theses", config.THESIS_DIR), ("output", config.OUTPUT_DIR)]:
        for f in dirpath.glob("**/*.md"):
            text = f.read_text(encoding="utf-8")
            orig = text
            for k, v in alias_map.items():
                # [[T-02 ...]] -> [[T1-01-...|T-02 ...]]
                pattern = rf'\[\[({re.escape(k)})(?:\|([^\]]+))?\]\]'
                def sub_fn(m):
                    label = m.group(2) or m.group(1)
                    return f"[[{v}|{label}]]"
                text = re.sub(pattern, sub_fn, text)
            if text != orig:
                f.write_text(text, encoding="utf-8")
                try:
                    sync_file(f, category)
                except Exception:
                    pass

