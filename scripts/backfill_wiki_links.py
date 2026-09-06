"""
scripts/backfill_wiki_links.py — 기존 산출물(Legacy Outputs) 위키링크 일괄 소급 적용 (Backfill)

실행:
  python scripts/backfill_wiki_links.py
  python scripts/backfill_wiki_links.py --dry-run
"""

import argparse
import json
import re
import sys
from pathlib import Path

# 부모 경로 추가
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

import config
from thesis_loader import (
    get_wikilink_map,
    inject_wikilinks_to_text,
    generate_knowledge_network_footer,
    _parse_md_file,
)
from obsidian_sync import sync_file


def process_markdown_file(filepath: Path, dry_run: bool = False) -> dict:
    text = filepath.read_text(encoding="utf-8")
    original_text = text
    
    meta, body = _parse_md_file(filepath)
    thesis_ids = []
    raw_thesis = meta.get("thesis") or meta.get("top_theses") or []
    if isinstance(raw_thesis, list):
        thesis_ids = [str(x) for x in raw_thesis]
    elif isinstance(raw_thesis, str):
        try:
            parsed = json.loads(raw_thesis)
            if isinstance(parsed, list):
                thesis_ids = [str(x) for x in parsed]
            else:
                thesis_ids = [raw_thesis]
        except Exception:
            thesis_ids = [t.strip() for t in raw_thesis.strip("[]'\"").split(",") if t.strip()]

    # 본문 내 위키링크 주입
    updated_body = inject_wikilinks_to_text(body, auto_keywords=True)

    # 지식 네트워크 푸터 부착 (없는 경우)
    if "## 🔗 연관 지식 네트워크" not in updated_body and "### 🔗 연관 지식 네트워크" not in updated_body:
        if thesis_ids:
            footer = generate_knowledge_network_footer(thesis_ids)
            updated_body = updated_body.rstrip() + "\n\n" + footer

    # 재조합
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            updated_text = f"---{parts[1]}---\n\n{updated_body.lstrip()}"
        else:
            updated_text = updated_body
    else:
        updated_text = updated_body

    is_modified = (updated_text != original_text)

    if is_modified and not dry_run:
        filepath.write_text(updated_text, encoding="utf-8")

    return {
        "file": filepath.name,
        "path": filepath,
        "modified": is_modified,
        "theses": thesis_ids,
    }


def backfill_all_outputs(dry_run: bool = False) -> None:
    print(f"\n🔄 [Backfill] 기존 산출물 위키링크 소급 적용 시작 {'(DRY RUN 모드)' if dry_run else ''}")
    print("═" * 75)

    target_dirs = [
        ("blog", config.OUTPUT_DIR / "blog"),
        ("digest", config.OUTPUT_DIR / "digest"),
        ("review", config.OUTPUT_DIR / "review"),
        ("thread", config.OUTPUT_DIR / "thread"),
        ("outline", config.OUTPUT_DIR / "outline"),
    ]

    total_scanned = 0
    total_modified = 0

    for category, dirpath in target_dirs:
        if not dirpath.exists():
            continue
        md_files = sorted(dirpath.glob("*.md"))
        print(f"\n📁 [{category.upper()}] {len(md_files)}개 파일 검사 중...")

        for f in md_files:
            total_scanned += 1
            res = process_markdown_file(f, dry_run=dry_run)
            status_icon = "✏️ [수정됨]" if res["modified"] else "✔️ [유지]"
            if res["modified"]:
                total_modified += 1
                print(f"  {status_icon} {f.name} (테제: {res['theses']})")
                if not dry_run:
                    try:
                        sync_file(f, category)
                    except Exception as e:
                        pass
            else:
                print(f"  {status_icon} {f.name}")

    print("\n" + "═" * 75)
    print(f"✨ [완료] 총 {total_scanned}개 파일 스캔 완료 | {total_modified}개 파일 위키링크 변환 및 동기화")
    print("═" * 75)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Argus Pulse — Legacy Outputs WikiLink Backfill")
    parser.add_argument("--dry-run", action="store_true", help="실제 파일 수정 없이 시뮬레이션만 수행")
    args = parser.parse_args()
    backfill_all_outputs(dry_run=args.dry_run)
