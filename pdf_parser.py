"""
pdf_parser.py — 증권사 리포트 PDF 파싱 및 메타데이터 자동 추출 모듈

특징:
  - pypdf 기반 안정적인 텍스트 추출
  - 파일명 패턴 분석: YY.MM.DD_기업명_증권사명_제목.pdf
  - 페이지별 텍스트 병합 및 정제
  - 개별 파일 및 디렉터리 일괄 파싱 지원
"""

import re
from pathlib import Path
from typing import Optional
from pypdf import PdfReader


def parse_report_filename(filename: str) -> dict:
    """
    파일명에서 날짜, 기업명, 증권사명, 리포트 제목 파싱
    예: '26.04.08_삼성전자_키움증권_너무 좋아도 걱정.pdf'
       -> date='2026-04-08', company='삼성전자', broker='키움증권', title='너무 좋아도 걱정'
    """
    stem = Path(filename).stem
    parts = stem.split("_", 3)

    meta = {
        "date": "",
        "company": "",
        "broker": "",
        "title": stem,
    }

    if len(parts) >= 4:
        raw_date, company, broker, title = parts[0], parts[1], parts[2], parts[3]
        # 날짜 포맷팅: 26.04.08 -> 2026-04-08
        date_match = re.match(r"^(\d{2})\.(\d{2})\.(\d{2})$", raw_date.strip())
        if date_match:
            yy, mm, dd = date_match.groups()
            meta["date"] = f"20{yy}-{mm}-{dd}"
        else:
            meta["date"] = raw_date.strip()

        meta["company"] = company.strip()
        meta["broker"] = broker.strip()
        meta["title"] = title.strip()
    elif len(parts) == 3:
        meta["company"] = parts[0].strip()
        meta["broker"] = parts[1].strip()
        meta["title"] = parts[2].strip()
    elif len(parts) == 2:
        meta["company"] = parts[0].strip()
        meta["title"] = parts[1].strip()

    return meta


def clean_pdf_text(text: str) -> str:
    """PDF 추출 텍스트 공백 및 노이즈 정제"""
    # 중복 공백 줄이기
    text = re.sub(r"[ \t]+", " ", text)
    # 3개 이상의 연속 개행을 2개로 축소
    text = re.sub(r"\n{3,}", "\n\n", text)
    # 줄바꿈 직전/직후 공백 제거
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(lines).strip()


def parse_pdf(filepath: str | Path) -> dict:
    """
    단일 PDF 파일 파싱
    Returns:
        {
            "filepath": str,
            "filename": str,
            "company": str,
            "broker": str,
            "title": str,
            "date": str,
            "pages": int,
            "text": str,
            "char_count": int
        }
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"PDF 파일을 찾을 수 없습니다: {path}")

    meta = parse_report_filename(path.name)
    pages_text = []

    try:
        reader = PdfReader(str(path))
        num_pages = len(reader.pages)
        for idx, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            if page_text.strip():
                pages_text.append(page_text)
    except Exception as e:
        print(f"  ⚠️ PDF 읽기 실패 ({path.name}): {e}")
        return {
            "filepath": str(path),
            "filename": path.name,
            **meta,
            "pages": 0,
            "text": "",
            "char_count": 0,
            "error": str(e)
        }

    full_text = clean_pdf_text("\n\n".join(pages_text))

    return {
        "filepath": str(path),
        "filename": path.name,
        **meta,
        "pages": num_pages,
        "text": full_text,
        "char_count": len(full_text)
    }


def parse_pdf_directory(dirpath: str | Path, recursive: bool = True) -> list[dict]:
    """디렉터리 내 모든 PDF 파싱"""
    root = Path(dirpath)
    if not root.exists():
        return []

    pattern = "**/*.pdf" if recursive else "*.pdf"
    pdf_files = sorted(list(root.glob(pattern)))
    print(f"📂 [PDF 디렉터리 스캔] {len(pdf_files)}개 파일 발견 ({root})")

    results = []
    for p in pdf_files:
        res = parse_pdf(p)
        if res["char_count"] > 0:
            results.append(res)
            print(f"  ✅ [{res['company'] or '일반'}] {res['broker']} - {res['title'][:25]} ({res['char_count']:,}자)")
        else:
            print(f"  ⚠️ 텍스트 없음: {p.name}")

    return results


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "../a_langragh/reports"
    path = Path(target)
    if path.is_dir():
        res = parse_pdf_directory(path)
        print(f"\n총 {len(res)}개 리포트 파싱 완료")
    elif path.is_file():
        res = parse_pdf(path)
        print(f"파싱 결과: {res['company']} | {res['broker']} | {res['title']} ({res['char_count']:,}자)")
        print("\n--- 미리보기 (처음 300자) ---")
        print(res["text"][:300])
