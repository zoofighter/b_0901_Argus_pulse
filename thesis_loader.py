"""
thesis_loader.py
thesis/ 폴더의 MD 파일들을 읽어서 딕셔너리 리스트로 반환.
frontmatter 라이브러리가 없어도 PyYAML로 자동 fallback 파싱 지원.
"""
from pathlib import Path
from typing import Optional
import re
import yaml

try:
    import frontmatter
    HAS_FRONTMATTER = True
except ImportError:
    HAS_FRONTMATTER = False


THESIS_DIR = Path(__file__).parent / "thesis"


def _parse_md_file(filepath: Path) -> tuple[dict, str]:
    """MD 파일에서 프론트매터(dict)와 본문(str)을 추출"""
    text = filepath.read_text(encoding="utf-8")
    if HAS_FRONTMATTER:
        post = frontmatter.loads(text)
        return dict(post.metadata), post.content
    
    # PyYAML fallback 파싱
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            raw_meta = parts[1]
            body = parts[2].lstrip("\r\n")
            meta = yaml.safe_load(raw_meta) or {}
            return meta, body
    return {}, text


def _save_md_file(filepath: Path, metadata: dict, body: str) -> None:
    """MD 파일에 프론트매터와 본문을 저장"""
    if HAS_FRONTMATTER:
        post = frontmatter.Post(body, **metadata)
        with open(filepath, "wb") as f:
            frontmatter.dump(post, f)
    else:
        yaml_str = yaml.dump(metadata, allow_unicode=True, sort_keys=False)
        content = f"---\n{yaml_str}---\n\n{body}"
        filepath.write_text(content, encoding="utf-8")


def load_theses(status_filter: Optional[str] = "active") -> list[dict]:
    """
    thesis/ 폴더의 T-*.md 파일을 읽어 프론트매터를 반환.
    
    Args:
        status_filter: "active" | "watch" | "archived" | None (전체)
    
    Returns:
        [{id, title, hypothesis, direction, confidence, priority,
          status, keywords, related_companies, ...}, ...]
    """
    theses = []

    for md_file in sorted(THESIS_DIR.glob("T-*.md")):
        meta, body = _parse_md_file(md_file)
        if not meta:
            continue
        meta["body"] = body  # 본문 (지지/반박 근거 등)
        meta["filepath"] = str(md_file)

        if status_filter is None or meta.get("status") == status_filter:
            theses.append(meta)

    return theses


def load_thesis_by_id(thesis_id: str) -> Optional[dict]:
    """특정 Thesis ID로 단일 Thesis 로드. 예: load_thesis_by_id("T-01")"""
    for thesis in load_theses(status_filter=None):
        if thesis.get("id") == thesis_id:
            return thesis
    return None


def get_active_keywords() -> dict[str, list[str]]:
    """
    active Thesis의 키워드를 {thesis_id: [keywords]} 형태로 반환.
    뉴스 스코어링 시 Thesis 매칭에 사용.
    """
    return {
        t["id"]: t.get("keywords", [])
        for t in load_theses(status_filter="active")
    }


def update_thesis_confidence(thesis_id: str, new_confidence: int) -> bool:
    """
    Thesis MD 파일의 confidence 값을 갱신.
    Thesis Checker 에이전트가 점검 후 호출.
    """
    for md_file in THESIS_DIR.glob("T-*.md"):
        meta, body = _parse_md_file(md_file)
        if meta.get("id") == thesis_id:
            meta["confidence"] = max(0, min(100, new_confidence))
            from datetime import datetime
            meta["last_checked"] = datetime.now().strftime("%Y-%m-%dT%H:%M")
            _save_md_file(md_file, meta, body)
            return True
    return False


def append_thesis_evidence(thesis_id: str, date_str: str, supporting: str = None, counter: str = None) -> bool:
    """Thesis MD 본문의 지지/반박 근거 섹션에 날짜별 기록 추가"""
    for md_file in THESIS_DIR.glob("T-*.md"):
        meta, body = _parse_md_file(md_file)
        if meta.get("id") == thesis_id:
            modified = False
            if supporting and supporting.strip() not in ("없음", "-"):
                line = f"- {date_str}: {supporting.strip()}"
                if "## 지지 근거" in body:
                    body = body.replace("## 지지 근거", f"## 지지 근거\n{line}")
                else:
                    body += f"\n\n## 지지 근거\n{line}"
                modified = True

            if counter and counter.strip() not in ("없음", "-"):
                line = f"- {date_str}: {counter.strip()}"
                if "## 반박 근거" in body:
                    body = body.replace("## 반박 근거", f"## 반박 근거\n{line}")
                else:
                    body += f"\n\n## 반박 근거\n{line}"
                modified = True

            if modified:
                _save_md_file(md_file, meta, body)
                return True
    return False


# ── 사용 예시 ────────────────────────────────────────────────
if __name__ == "__main__":
    # 전체 active Thesis 출력
    theses = load_theses()
    print(f"총 로드된 Active Thesis: {len(theses)}개\n")
    for t in theses:
        print(f"[{t['id']}] {t['title']} | confidence={t.get('confidence')}% | priority={t.get('priority')}")

    # Thesis 매칭용 키워드 맵
    keyword_map = get_active_keywords()
    print(f"\n키워드 맵 (총 {len(keyword_map)}개 테제 등록됨):")
    for tid, kws in list(keyword_map.items())[:5]:
        print(f"  {tid}: {kws[:4]}...")
