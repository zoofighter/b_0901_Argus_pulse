"""
html_parser.py — 수동 입력 소스 파싱

지원 형식:
  - 네이버 블로그 저장 HTML (se-main-container)
  - 일반 HTML 웹페이지
  - 마크다운 (.md)
  - 텍스트 (.txt)
  - 폴더 (99.raw 등) — 내부 파일 전체 처리

실행:
  python html_parser.py 99.raw/파일명.html
  python html_parser.py 99.raw/           # 폴더 전체
"""

import html
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    print("⚠️  bs4 미설치: pip install beautifulsoup4")


# ── 네이버 블로그 파서 ────────────────────────────────────────────────────────

def _extract_naver_blog(soup) -> str:
    """네이버 스마트에디터 본문 추출"""
    for selector in ["se-main-container", "postViewArea", "post_content", "se-viewer"]:
        main = soup.find(class_=selector)
        if main:
            for tag in main(["script", "style"]):
                tag.decompose()
            return main.get_text(separator="\n")
    return ""


def _extract_generic(soup) -> str:
    """범용 HTML 본문 추출"""
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()
    for selector in ["article", "main", ".content", "#content", "body"]:
        el = soup.select_one(selector)
        if el:
            return el.get_text(separator="\n")
    return soup.get_text(separator="\n")


def _clean_lines(raw_text: str, min_len: int = 3) -> str:
    """빈 줄·짧은 줄 제거 후 정제된 텍스트 반환"""
    lines = []
    for line in raw_text.split("\n"):
        stripped = line.strip()
        if stripped and len(stripped) >= min_len:
            lines.append(stripped)
    return "\n".join(lines)


# ── 공개 API ─────────────────────────────────────────────────────────────────

def parse_html(filepath: str | Path) -> str:
    """
    HTML 파일에서 본문 텍스트 추출.
    네이버 블로그 → 범용 순으로 시도.

    Returns:
        정제된 본문 텍스트 (실패 시 빈 문자열)
    """
    if not BS4_AVAILABLE:
        return ""

    filepath = Path(filepath)
    try:
        raw = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"  ⚠️  파일 읽기 실패 ({filepath.name}): {e}")
        return ""

    decoded = html.unescape(raw)
    soup = BeautifulSoup(decoded, "html.parser")

    # 네이버 블로그 우선 시도
    text = _extract_naver_blog(soup)
    if not text.strip():
        text = _extract_generic(soup)

    return _clean_lines(text)


def parse_file(filepath: str | Path) -> dict:
    """
    파일 형식 자동 감지 후 파싱.

    Returns:
        {"filename": str, "content": str, "type": str, "char_count": int}
    """
    filepath = Path(filepath)
    suffix = filepath.suffix.lower()

    if suffix == ".html":
        content = parse_html(filepath)
        ftype = "html"
    elif suffix in (".md", ".markdown"):
        content = _clean_lines(filepath.read_text(encoding="utf-8", errors="ignore"))
        ftype = "markdown"
    elif suffix == ".txt":
        content = _clean_lines(filepath.read_text(encoding="utf-8", errors="ignore"))
        ftype = "text"
    else:
        content = ""
        ftype = "unknown"

    return {
        "filename": filepath.name,
        "filepath": str(filepath),
        "content": content,
        "type": ftype,
        "char_count": len(content),
    }


def parse_raw_folder(folder: str | Path = "99.raw") -> list[dict]:
    """
    지정 폴더의 모든 지원 파일을 파싱.

    Returns:
        parse_file() 결과 목록 (내용 있는 파일만)
    """
    folder = Path(folder)
    if not folder.exists():
        print(f"  ⚠️  폴더 없음: {folder}")
        return []

    results = []
    supported = {".html", ".md", ".txt", ".markdown"}

    for f in sorted(folder.iterdir()):
        if f.is_dir() or f.suffix.lower() not in supported:
            continue
        parsed = parse_file(f)
        if parsed["char_count"] > 50:
            results.append(parsed)
            print(f"  ✅ {f.name[:55]:<55} [{parsed['type']}] {parsed['char_count']:,}자")
        else:
            print(f"  ⚠️  {f.name[:55]:<55} 본문 추출 실패 (내용 부족)")

    return results


def archive_processed_files(filepaths: list[str | Path], archive_dir: str | Path = None) -> list[Path]:
    """처리 완료된 raw 파일들을 archive/ 폴더로 이동"""
    import shutil
    archived = []
    for fp in filepaths:
        p = Path(fp)
        if not p.exists() or p.is_dir():
            continue
        target_folder = Path(archive_dir) if archive_dir else p.parent / "archive"
        target_folder.mkdir(parents=True, exist_ok=True)
        dst = target_folder / p.name
        try:
            shutil.move(str(p), str(dst))
            print(f"  📦 [아카이빙] {p.name} -> archive/{p.name}")
            archived.append(dst)
        except Exception as e:
            print(f"  ⚠️  아카이빙 실패 ({p.name}): {e}")
    return archived


def merge_contents(parsed_list: list[dict], separator: str = "\n\n---\n\n") -> str:
    """여러 파일 내용을 하나의 컨텍스트로 합치기"""
    parts = []
    for p in parsed_list:
        header = f"[출처: {p['filename']}]"
        parts.append(f"{header}\n{p['content']}")
    return separator.join(parts)


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="HTML / Markdown 파서 및 아카이빙")
    parser.add_argument("targets", nargs="*", default=["99.raw"], help="파싱할 파일 또는 디렉토리")
    parser.add_argument("--archive", action="store_true", help="파싱 완료 후 archive/ 폴더로 이동")
    args = parser.parse_args()

    for target in args.targets:
        path = Path(target)
        print(f"\n{'='*60}")
        print(f"대상: {target}")
        print('='*60)

        if path.is_dir():
            results = parse_raw_folder(path)
            if results:
                merged = merge_contents(results)
                print(f"\n총 {len(results)}개 파일, 합산 {len(merged):,}자")
                print("\n--- 미리보기 (처음 500자) ---")
                print(merged[:500])
                if args.archive:
                    print("\n📦 아카이빙 실행 중...")
                    archive_processed_files([r["filepath"] for r in results])
        elif path.is_file():
            result = parse_file(path)
            print(f"타입: {result['type']}")
            print(f"추출 글자 수: {result['char_count']:,}자")
            print("\n--- 미리보기 (처음 500자) ---")
            print(result["content"][:500])
            if args.archive:
                print("\n📦 아카이빙 실행 중...")
                archive_processed_files([result["filepath"]])
        else:
            print(f"파일/폴더를 찾을 수 없음: {target}")
