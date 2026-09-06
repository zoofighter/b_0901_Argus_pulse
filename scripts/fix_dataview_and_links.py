"""
scripts/fix_dataview_and_links.py
1. 옵시디언 볼트의 Dataview 설정 파일(data.json) 생성 및 활성화
2. Master MOC 및 모든 테제/허브 파일 내의 중복 슬러그(예: 메모리-산업의-변화메모리-산업의-변화) 제거
3. Dataview 쿼리 문법 및 경로(FROM)를 가장 안전하고 호환성 높은 구조로 최적화
4. 볼트로 전면 재동기화
"""

import os
import sys
import json
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


def enable_dataview_in_vault():
    """옵시디언 볼트에 Dataview 플러그인 설정 파일(data.json) 생성 및 활성화"""
    if not VAULT.exists():
        return

    dv_plugin_dir = VAULT / ".obsidian" / "plugins" / "dataview"
    dv_plugin_dir.mkdir(parents=True, exist_ok=True)

    dv_config = {
        "enableDataviewJs": True,
        "enableInlineDataview": True,
        "enableInlineDataviewJs": True,
        "enableRenderingMarkdownInTables": True,
        "defaultDateFormat": "yyyy-MM-dd",
        "defaultDateTimeFormat": "yyyy-MM-dd HH:mm:ss",
        "maxRecursiveRenderDepth": 4,
        "tableIdColumnName": "테제",
        "tableGroupColumnName": "그룹",
        "inlineJsQueryPrefix": "$=",
        "inlineQueryPrefix": "=",
        "dataviewJsKeyword": "dataviewjs"
    }

    data_json_path = dv_plugin_dir / "data.json"
    data_json_path.write_text(json.dumps(dv_config, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  ⚙️ [Dataview 설정 완료] {data_json_path}")


def clean_duplicated_links():
    """모든 마크다운 파일 내의 중복 치환 슬러그 정규화"""
    # 38개 테제 정확한 파일명 매핑
    thesis_map = {}
    for f in THESIS_DIR.glob("*.md"):
        if f.name.startswith(("SC-", "DC-", "RB-", "SW-", "GE-", "MC-")):
            code = f.name.split("-")[0] + "-" + f.name.split("-")[1]
            slug = f.name.replace(".md", "")
            thesis_map[code] = slug

    print("\n🧹 링크 중복 슬러그 검사 및 정규화 진행 중...")
    for f in sorted(THESIS_DIR.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        modified = False

        # 1. 00-Master-MOC 및 본문 내 중복 슬러그 교정
        for code, exact_slug in thesis_map.items():
            # 예: [[SC-01-메모리-산업의-변화메모리-산업의-변화| -> [[SC-01-메모리-산업의-변화|
            # 정규식 패턴 치환
            import re
            pattern = re.compile(rf"\[\[{re.escape(code)}-[^\|\]]+\|")
            for m in pattern.findall(text):
                correct = f"[[{exact_slug}|"
                if m != correct:
                    text = text.replace(m, correct)
                    modified = True

        # 2. Dataview 쿼리 안정성 강화
        # FROM "argus/Theses" -> FROM "argus/Theses" OR "Theses" OR "thesis"
        # WHERE 절에 null 체크 및 안전한 문자열 비교
        if "```dataview" in text:
            text = text.replace('FROM "argus/Theses"', 'FROM "argus/Theses" OR "Theses" OR "thesis"')
            text = text.replace('FROM "argus" OR "output"', 'FROM "argus" OR "output" OR ""')
            modified = True

        if modified:
            f.write_text(text, encoding="utf-8")
            print(f"  ✨ [링크 교정 완료] {f.name}")


def sync_all():
    """최종 정리된 파일들을 볼트로 일괄 복사"""
    from obsidian_sync import sync_all_outputs
    sync_all_outputs()


if __name__ == "__main__":
    print("🚀 [Dataview 점검 및 링크 무결성 복구 시작]\n")
    enable_dataview_in_vault()
    clean_duplicated_links()
    print("\n📂 [옵시디언 볼트로 최종 동기화]")
    sync_all()
    print("\n🎉 모든 점검과 복구가 완료되었습니다!")
