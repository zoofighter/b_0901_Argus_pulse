"""
ingest.py — RAG 지식 DB 구축 및 지식 순환 인제스트 도구

사용법:
  python ingest.py --status              # DB 현황 확인
  python ingest.py --pdf                 # a_langragh/reports/ 내 증권사 PDF 인제스트
  python ingest.py --pdf 경로            # 특정 폴더/파일 PDF 인제스트
  python ingest.py --raw                 # 99.raw 폴더 파일 인제스트
  python ingest.py --output              # output/ 내 자체 산출물 재인제스트 (지식 순환)
  python ingest.py --all                 # 전체 일괄 인제스트
"""

import argparse
import sys
from pathlib import Path

import config
from html_parser import parse_file, parse_raw_folder
from pdf_parser import parse_pdf, parse_pdf_directory
from rag_engine import (
    COLLECTION_KNOWLEDGE,
    COLLECTION_REPORTS,
    get_db_status,
    ingest_document,
)


def ingest_pdf_reports(target_dir: Path = None) -> int:
    """증권사 PDF 리포트 인제스트"""
    path = target_dir or config.PDF_REPORTS_DIR
    if not path.exists():
        print(f"❌ PDF 경로를 찾을 수 없습니다: {path}")
        return 0

    print(f"\n📂 [PDF 인제스트 시작] {path}")
    if path.is_file():
        parsed_items = [parse_pdf(path)]
    else:
        parsed_items = parse_pdf_directory(path)

    total_chunks = 0
    success_files = 0

    for item in parsed_items:
        if not item.get("text"):
            continue
        meta = {
            "source_type": "analyst_pdf",
            "filename": item["filename"],
            "filepath": item["filepath"],
            "company": item.get("company", ""),
            "broker": item.get("broker", ""),
            "title": item.get("title", ""),
            "date": item.get("date", ""),
        }
        chunks = ingest_document(item["text"], meta, COLLECTION_KNOWLEDGE)
        total_chunks += chunks
        success_files += 1

    print(f"✅ PDF 인제스트 완료: {success_files}개 파일 → 총 {total_chunks:,}개 청크 저장")
    return total_chunks


def ingest_raw_folder(target_dir: Path = None) -> int:
    """99.raw 및 archive 폴더 내 자료 인제스트"""
    path = target_dir or config.RAW_DIR
    if not path.exists():
        print(f"❌ 경로를 찾을 수 없습니다: {path}")
        return 0

    print(f"\n📂 [수동 자료(Raw) 인제스트 시작] {path}")
    items = parse_raw_folder(path)
    # archive 폴더도 함께 확인
    archive_dir = path / "archive"
    if archive_dir.exists():
        items.extend(parse_raw_folder(archive_dir))

    total_chunks = 0
    for item in items:
        meta = {
            "source_type": "raw_scraped",
            "filename": item["filename"],
            "filepath": item["filepath"],
            "title": item["filename"],
            "date": "",
        }
        chunks = ingest_document(item["content"], meta, COLLECTION_KNOWLEDGE)
        total_chunks += chunks

    print(f"✅ Raw 자료 인제스트 완료: {len(items)}개 파일 → 총 {total_chunks:,}개 청크 저장")
    return total_chunks


def ingest_generated_outputs() -> int:
    """output/ 내 자체 산출물 재인제스트 (지식 순환 루프)"""
    print(f"\n🔄 [자체 산출물 재인제스트(지식 순환) 시작] {config.OUTPUT_DIR}")
    total_chunks = 0
    count = 0

    for sub in ["blog", "thread", "digest", "review"]:
        sub_dir = config.OUTPUT_DIR / sub
        if not sub_dir.exists():
            continue

        for md_file in sub_dir.glob("*.md"):
            try:
                text = md_file.read_text(encoding="utf-8")
                meta = {
                    "source_type": f"argus_{sub}",
                    "filename": md_file.name,
                    "filepath": str(md_file),
                    "title": md_file.stem,
                    "category": sub,
                }
                chunks = ingest_document(text, meta, COLLECTION_REPORTS)
                total_chunks += chunks
                count += 1
            except Exception as e:
                print(f"  ⚠️ 인제스트 실패 ({md_file.name}): {e}")

    print(f"✅ 산출물 재인제스트 완료: {count}개 파일 → 총 {total_chunks:,}개 청크 저장")
    return total_chunks


def print_status():
    """ChromaDB 상태 출력"""
    status = get_db_status()
    print("\n📊 [Argus Pulse ChromaDB 현황]")
    print(f"   위치: {config.CHROMA_DB_PATH}")
    print(f"   1. {COLLECTION_KNOWLEDGE} (외부 지식: PDF/웹자료) : {status.get(COLLECTION_KNOWLEDGE, 0):,}개 청크")
    print(f"   2. {COLLECTION_REPORTS}   (내부 지식: 생성 리포트)   : {status.get(COLLECTION_REPORTS, 0):,}개 청크")
    total = sum(status.values())
    print(f"   👉 전체 보유 지식 청크: {total:,}개\n")


def main():
    parser = argparse.ArgumentParser(description="Argus Pulse — RAG 지식 인제스트 도구")
    parser.add_argument("--status", action="store_true", help="ChromaDB 현황 확인")
    parser.add_argument("--pdf", nargs="?", const=str(config.PDF_REPORTS_DIR), help="증권사 PDF 리포트 인제스트")
    parser.add_argument("--raw", nargs="?", const=str(config.RAW_DIR), help="수동 raw 자료 인제스트")
    parser.add_argument("--output", action="store_true", help="output/ 자체 생성물 재인제스트")
    parser.add_argument("--all", action="store_true", help="전체 데이터 소스 일괄 인제스트")
    args = parser.parse_args()

    if args.status or len(sys.argv) == 1:
        print_status()
        return

    if args.all:
        ingest_pdf_reports()
        ingest_raw_folder()
        ingest_generated_outputs()
        print_status()
        return

    if args.pdf:
        ingest_pdf_reports(Path(args.pdf))
    if args.raw:
        ingest_raw_folder(Path(args.raw))
    if args.output:
        ingest_generated_outputs()

    print_status()


if __name__ == "__main__":
    main()
