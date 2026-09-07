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
    "canvas": "argus/Canvas",
    "incubator": "argus/Incubator",
    "chronicles": "argus/Chronicles",
    "analogies": "argus/Analogies",
    "topics": "argus/Topics",
    "topic": "argus/Topics",
    "companies": "argus/Companies",
    "company": "argus/Companies",
    "moc": "argus",
    "docs": "argus/Docs",
    "vs": "argus/Vs",
    "vs_hub": "argus/Vs",
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


def sync_file(filepath: str | Path, category: str, force: bool = False) -> Path | None:
    """단일 마크다운/캔버스 파일을 옵시디언 볼트로 증분 동기화(변경된 파일만 복사)"""
    src = Path(filepath)
    if not src.exists():
        return None

    target_dir = get_target_dir(category)
    if not target_dir:
        return None

    dest = target_dir / src.name
    try:
        # 증분 동기화: 이미 존재하고 크기 및 수정 시간이 같으면 불필요한 I/O 건너뜀
        if not force and dest.exists():
            src_stat = src.stat()
            dest_stat = dest.stat()
            if dest_stat.st_mtime >= src_stat.st_mtime and dest_stat.st_size == src_stat.st_size:
                return dest

        shutil.copy2(src, dest)
        print(f"  📓 [Obsidian 동기화] {category.upper()} -> {dest.relative_to(config.OBSIDIAN_PATH)}")
        return dest
    except Exception as e:
        print(f"  ❌ [Obsidian 동기화 실패] {src.name}: {e}")
        return None


def sync_all_outputs() -> dict[str, int]:
    """모든 생성된 콘텐츠 및 테제/문서를 옵시디언 볼트로 일괄 동기화"""
    vault = config.OBSIDIAN_PATH
    if not vault or not vault.exists():
        print(f"  ⚠️ 옵시디언 볼트 경로가 존재하지 않습니다: {vault}")
        return {}

    counts = {
        "blog": 0, "thread": 0, "outline": 0, "digest": 0, "review": 0,
        "theses": 0, "incubator": 0, "chronicles": 0, "analogies": 0,
        "topics": 0, "companies": 0, "vs": 0, "docs": 0, "moc": 0
    }

    # 1. Output 디렉터리 동기화
    for cat in ["blog", "thread", "outline", "digest", "review"]:
        src_dir = config.OUTPUT_DIR / cat
        if not src_dir.exists():
            continue

        for md_file in src_dir.glob("*.md"):
            res = sync_file(md_file, cat)
            if res:
                counts[cat] += 1

    # 2. Thesis 및 하위 지식 디렉터리 동기화
    if config.THESIS_DIR.exists():
        for t_file in sorted([f for f in config.THESIS_DIR.glob("*.md") if not f.name.startswith(("00-", "Topic-", "Company-", "Vs-"))]):
            if sync_file(t_file, "theses"):
                counts["theses"] += 1
        # Incubator, Chronicles, Analogies 하위 폴더 동기화
        for sub_cat in ["incubator", "chronicles", "analogies"]:
            sub_dir = config.THESIS_DIR / sub_cat.capitalize()
            if sub_dir.exists():
                for sub_f in sub_dir.glob("*.md"):
                    if sync_file(sub_f, sub_cat):
                        counts[sub_cat] += 1

        for top_file in config.THESIS_DIR.glob("Topic-*.md"):
            if sync_file(top_file, "topics"):
                counts["topics"] += 1
        for c_file in config.THESIS_DIR.glob("Company-*.md"):
            if sync_file(c_file, "companies"):
                counts["companies"] += 1
        for v_file in config.THESIS_DIR.glob("Vs-*.md"):
            if sync_file(v_file, "vs"):
                counts["vs"] += 1
        for canvas_file in config.THESIS_DIR.glob("*.canvas"):
            if sync_file(canvas_file, "canvas"):
                counts["canvas"] = counts.get("canvas", 0) + 1
        moc_file = config.THESIS_DIR / "00-Argus-Master-MOC.md"
        if moc_file.exists() and sync_file(moc_file, "moc"):
            counts["moc"] += 1

    # 3. Docs 동기화
    docs_dir = config.ROOT_DIR / "docs"
    if docs_dir.exists():
        for doc_file in docs_dir.glob("*.md"):
            if sync_file(doc_file, "docs"):
                counts["docs"] += 1

    print("\n✅ 동기화 완료 요약:")
    for cat, cnt in counts.items():
        if cnt > 0:
            print(f"   - {cat:<10}: {cnt}개 파일")

    return counts


if __name__ == "__main__":
    sync_all_outputs()
