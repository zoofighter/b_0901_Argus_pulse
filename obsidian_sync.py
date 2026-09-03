"""
obsidian_sync.py — 옵시디언(Obsidian) 볼트 자동 동기화 모듈

기능:
  - output/에 생성된 마크다운 결과물을 사용자 옵시디언 볼트로 자동 복사
  - 카테고리별 폴더 자동 분류:
      * blog   -> Content/Blog/
      * thread -> Content/Thread/
      * digest -> Digest/
      * review -> Reports/Review/
  - 전체 일괄 동기화 및 단일 파일 실시간 동기화 지원

실행:
  python obsidian_sync.py          # output/ 내 모든 파일 일괄 동기화
"""

import shutil
from pathlib import Path
import config

FOLDER_MAP = {
    "blog": "argus/Blog",
    "thread": "argus/Thread",
    "outline": "argus/Outline",
    "digest": "argus/Digest",
    "review": "argus/Review",
    "theses": "argus/Theses",
    "thesis": "argus/Theses",
}


def get_target_dir(category: str) -> Path | None:
    """옵시디언 볼트 내 카테고리별 대상 디렉터리 경로 반환 (없으면 생성)"""
    vault = config.OBSIDIAN_PATH
    if not vault or not vault.exists():
        return None

    sub_dir = FOLDER_MAP.get(category.lower(), "Content")
    target = vault / sub_dir
    target.mkdir(parents=True, exist_ok=True)
    return target


def sync_file(filepath: str | Path, category: str) -> Path | None:
    """단일 마크다운 파일을 옵시디언 볼트로 동기화(복사)"""
    src = Path(filepath)
    if not src.exists():
        return None

    target_dir = get_target_dir(category)
    if not target_dir:
        return None

    dst = target_dir / src.name
    try:
        shutil.copy2(src, dst)
        print(f"  📓 [Obsidian 동기화] {category.upper()} -> {dst.relative_to(config.OBSIDIAN_PATH)}")
        return dst
    except Exception as e:
        print(f"  ⚠️  옵시디언 복사 실패: {e}")
        return None


def sync_all_outputs() -> dict:
    """output/ 폴더 내의 모든 생성물을 옵시디언으로 일괄 동기화"""
    vault = config.OBSIDIAN_PATH
    print(f"\n📂 [Obsidian 전체 동기화 시작]")
    print(f"   볼트 위치: {vault}")

    if not vault.exists():
        print(f"  ❌ 옵시디언 볼트 경로가 존재하지 않습니다: {vault}")
        return {}

    counts = {"blog": 0, "thread": 0, "digest": 0, "review": 0}

    for cat in counts.keys():
        src_dir = config.OUTPUT_DIR / cat
        if not src_dir.exists():
            continue

        for md_file in src_dir.glob("*.md"):
            res = sync_file(md_file, cat)
            if res:
                counts[cat] += 1

    print("\n✅ 동기화 완료 요약:")
    for cat, cnt in counts.items():
        print(f"   - {cat:<7}: {cnt}개 파일")

    return counts


if __name__ == "__main__":
    sync_all_outputs()
