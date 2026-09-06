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

    for md_file in sorted([f for f in THESIS_DIR.glob("*.md") if not f.name.startswith(("00-", "Topic-", "Company-", "Vs-"))]):
        meta, body = _parse_md_file(md_file)
        if not meta:
            continue
        meta["body"] = body  # 본문 (지지/반박 근거 등)
        meta["filepath"] = str(md_file)

        if status_filter is None or meta.get("status") == status_filter:
            theses.append(meta)

    return theses


def load_thesis_by_id(thesis_id: str) -> Optional[dict]:
    """특정 Thesis ID로 단일 Thesis 로드. 1순위: id 정확 일치, 2순위: old_id/aliases 매칭"""
    all_theses = load_theses(status_filter=None)
    # 1순위: ID 정확 일치
    for thesis in all_theses:
        if thesis.get("id") == thesis_id:
            return thesis
    # 2순위: old_id 또는 별칭 매칭
    for thesis in all_theses:
        if thesis.get("old_id") == thesis_id or thesis_id in thesis.get("aliases", []):
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
    for md_file in [f for f in THESIS_DIR.glob("*.md") if not f.name.startswith(("00-", "Topic-", "Company-", "Vs-"))]:
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
    for md_file in [f for f in THESIS_DIR.glob("*.md") if not f.name.startswith(("00-", "Topic-", "Company-", "Vs-"))]:
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


def get_thesis_momentum_ranking(
    days: int = 2,
    status_filter: Optional[str] = "active",
    limit: Optional[int] = None,
    db_path: Optional[Path] = None,
) -> list[dict]:
    """
    최근 N일간 뉴스 DB 데이터를 기반으로 시장 모멘텀(News Momentum) 랭킹을 산출.
    
    점수 계산 로직:
      - raw_momentum_score: 매칭된 뉴스 점수 합산 (최근 24시간 뉴스 1.2배 가중치)
      - news_count: 매칭된 뉴스 기사 건수
      - avg_news_score: 매칭된 뉴스의 평균 점수
      - momentum_score (종합 점수): raw_momentum_score + (priority * 10) + (confidence * 0.2)
      - rank: 종합 모멘텀 점수(내림차순) 기준 1위~N위 부여
    """
    from datetime import datetime, timedelta
    import sqlite3

    try:
        import config
        news_db = db_path or config.NEWS_DB_PATH
    except Exception:
        import os
        env_path = os.getenv("NEWS_DB_PATH")
        news_db = db_path or (Path(env_path) if env_path else Path(__file__).parent.parent / "b_0826_news_research" / "db" / "news.sqlite")

    news_list = []
    if news_db and Path(news_db).exists():
        try:
            since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            conn = sqlite3.connect(str(news_db))
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT company, ticker, title, snippet, score, source, published, collected_at
                FROM news
                WHERE (published >= ? OR collected_at >= ?)
                ORDER BY score DESC
            """, (since, since)).fetchall()
            conn.close()
            news_list = [dict(r) for r in rows]
        except Exception as e:
            # DB 연결 실패 시 빈 리스트로 안전하게 폴백
            news_list = []

    theses = load_theses(status_filter=status_filter)
    ranked = []
    one_day_ago = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    for t in theses:
        keywords = t.get("keywords", [])
        matched_news = []
        raw_momentum = 0.0

        for n in news_list:
            title = n.get("title", "")
            snippet = n.get("snippet", "")
            text = f"{title} {snippet}"

            if any(str(kw) in text for kw in keywords if kw):
                score = float(n.get("score") or 50.0)
                pub = str(n.get("published") or n.get("collected_at") or "")
                weight = 1.2 if pub >= one_day_ago else 1.0
                raw_momentum += score * weight
                matched_news.append(n)

        news_count = len(matched_news)
        avg_score = round(sum(float(n.get("score") or 0) for n in matched_news) / news_count, 1) if news_count > 0 else 0.0
        max_score = max([int(n.get("score") or 0) for n in matched_news], default=0)

        priority = float(t.get("priority") or 3)
        confidence = float(t.get("confidence") or 50)
        composite_score = round(raw_momentum + (priority * 10.0) + (confidence * 0.2), 1)

        t_copy = dict(t)
        t_copy["news_count"] = news_count
        t_copy["raw_momentum_score"] = round(raw_momentum, 1)
        t_copy["momentum_score"] = composite_score
        t_copy["avg_news_score"] = avg_score
        t_copy["max_news_score"] = max_score
        t_copy["matched_news"] = matched_news[:5]
        ranked.append(t_copy)

    # 1차 정렬: raw_momentum_score (뉴스 발생량/점수)
    # 2차 정렬: composite_score (우선순위/신뢰도 가미)
    ranked.sort(
        key=lambda x: (x["raw_momentum_score"], x["momentum_score"], x.get("priority", 0), x.get("confidence", 0)),
        reverse=True
    )

    for i, t in enumerate(ranked, 1):
        t["rank"] = i

    if limit:
        return ranked[:limit]
    return ranked


def sync_thesis_ranks_to_files(days: int = 2, db_path: Optional[Path] = None) -> list[dict]:
    """
    모든 Thesis의 시장 모멘텀 랭킹을 계산하여
    각 T-*.md 파일의 frontmatter에 rank, momentum, news_count 필드를 자동 갱신 저장.
    동시에 Obsidian 볼트로 자동 미러링 동기화.
    """
    from datetime import datetime
    ranked_theses = get_thesis_momentum_ranking(days=days, status_filter=None, db_path=db_path)
    rank_map = {t["id"]: t for t in ranked_theses}
    now_str = datetime.now().strftime("%Y-%m-%dT%H:%M")

    updated_count = 0
    for md_file in [f for f in THESIS_DIR.glob("*.md") if not f.name.startswith(("00-", "Topic-", "Company-", "Vs-"))]:
        meta, body = _parse_md_file(md_file)
        tid = meta.get("id")
        if tid and tid in rank_map:
            t_data = rank_map[tid]
            meta["rank"] = int(t_data["rank"])
            meta["momentum"] = float(t_data["momentum_score"])
            meta["news_count"] = int(t_data["news_count"])
            meta["last_ranked"] = now_str
            _save_md_file(md_file, meta, body)
            updated_count += 1

            # Obsidian 자동 동기화
            try:
                from obsidian_sync import sync_file
                sync_file(md_file, "theses")
            except Exception:
                pass

    print(f"  📝 [Thesis Frontmatter 갱신] 총 {updated_count}개 Thesis MD 파일에 rank & momentum 저장 완료")
    return ranked_theses



# ── Obsidian 위키링크 지식 그래프 연동 헬퍼 ────────────────────────

def get_wikilink_map() -> dict:
    """
    thesis/ 디렉토리 내의 테제, 토픽, 기업, MOC 파일들을 분석하여
    키워드 -> 위키링크 맵을 반환.
    """
    theses = load_theses(status_filter=None)
    thesis_map = {}
    for t in theses:
        tid = t.get("id")
        old_id = t.get("old_id")
        title = t.get("title", "")
        fp = Path(t.get("filepath", ""))
        stem = fp.stem
        link = f"[[{stem}|{tid} {title}]]"
        short_link = f"[[{stem}|{tid}]]"
        
        if tid:
            thesis_map[tid] = (short_link, link, stem)
        if old_id:
            thesis_map[old_id] = (short_link, link, stem)
        for alias in t.get("aliases", []):
            thesis_map[alias] = (short_link, link, stem)

    topic_map = {}
    for f in THESIS_DIR.glob("Topic-*.md"):
        topic_name = f.stem.replace("Topic-", "")
        topic_map[topic_name] = f"[[{f.stem}|{topic_name}]]"

    company_map = {}
    for f in THESIS_DIR.glob("Company-*.md"):
        comp_name = f.stem.replace("Company-", "")
        company_map[comp_name] = f"[[{f.stem}|{comp_name}]]"

    return {
        "theses": thesis_map,
        "topics": topic_map,
        "companies": company_map,
        "moc": "[[00-Argus-Master-MOC|Argus Master MOC]]"
    }


def inject_wikilinks_to_text(text: str, auto_keywords: bool = True) -> str:
    """
    본문 텍스트 내의 테제 ID(T1-01, T-01 등), 주요 기업, 주요 기술 토픽을
    옵시디언 위키링크로 변환 (이미 링크 처리된 부분 [[...]] 이나 [...]은 보호).
    """
    wmap = get_wikilink_map()
    
    # 1. 테제 ID 변환 (T[1-6]-[0-9]{2} 또는 T-[0-9]{2})
    def replace_thesis(match):
        tid = match.group(0)
        if tid in wmap["theses"]:
            return wmap["theses"][tid][0]
        return tid

    # 이미 위키링크 안에 있는 것은 건너뛰기 위해 정규식 보호 처리
    # 예: [[...]] 내부는 건너뛰고 일반 텍스트의 Thesis ID 치환
    pattern = r'(?<!\[\[)(?<![A-Za-z0-9_])(T[1-6]-\d{2}|T-\d{2})(?![A-Za-z0-9_])(?!\]\])'
    text = re.sub(pattern, replace_thesis, text)

    if auto_keywords:
        # 2. 기업명 변환 (긴 이름부터 매칭)
        sorted_companies = sorted(wmap["companies"].keys(), key=len, reverse=True)
        for comp in sorted_companies:
            if len(comp) < 2:
                continue
            link = wmap["companies"][comp]
            # 이미 대괄호 안에 들어있지 않은 단어만 치환
            # 정규식 negative lookbehind/lookahead
            esc_comp = re.escape(comp)
            comp_pattern = rf'(?<!\[\[)(?<![가-힣a-zA-Z0-9])({esc_comp})(?![가-힣a-zA-Z0-9])(?!\]\])(?![^\[]*\])'
            # 본문에서 최대 3회까지만 치환하여 가독성 유지
            text = re.sub(comp_pattern, link, text, count=3)

        # 3. 토픽명 변환
        sorted_topics = sorted(wmap["topics"].keys(), key=len, reverse=True)
        for top in sorted_topics:
            if len(top) < 2:
                continue
            link = wmap["topics"][top]
            esc_top = re.escape(top)
            top_pattern = rf'(?<!\[\[)(?<![가-힣a-zA-Z0-9])({esc_top})(?![가-힣a-zA-Z0-9])(?!\]\])(?![^\[]*\])'
            text = re.sub(top_pattern, link, text, count=2)

    return text


def generate_knowledge_network_footer(thesis_ids: list[str], extra_topics: Optional[list[str]] = None, extra_companies: Optional[list[str]] = None) -> str:
    """
    마크다운 문서 하단에 부착할 표준 '🔗 연관 지식 네트워크 (Knowledge Network)' 위키링크 섹션 생성
    """
    wmap = get_wikilink_map()
    lines = [
        "---",
        "## 🔗 연관 지식 네트워크 (Knowledge Network)",
        "",
        "### 📌 관련 투자 테제 (Investment Theses)",
    ]

    added_theses = set()
    for tid in thesis_ids:
        t = load_thesis_by_id(tid)
        if t:
            fp = Path(t.get("filepath", ""))
            link = f"- [[{fp.stem}|{t.get('id')} {t.get('title')}]]"
            lines.append(link)
            added_theses.add(t.get("id"))
        elif tid in wmap["theses"]:
            stem = wmap["theses"][tid][2]
            lines.append(f"- [[{stem}|{tid}]]")
            added_theses.add(tid)

    if not added_theses:
        lines.append("- 연관 테제 없음")

    # 관련 기술 토픽
    lines.append("\n### 🏷️ 핵심 기술 토픽 (Topics)")
    topic_links = []
    # 테제에서 추출하거나 인자로 받은 토픽
    all_topics = set(extra_topics or [])
    for tid in thesis_ids:
        t = load_thesis_by_id(tid)
        if t:
            for top_name, top_link in wmap["topics"].items():
                if top_name in str(t.get("keywords", [])) or top_name in t.get("title", ""):
                    all_topics.add(top_name)
    
    for top in sorted(all_topics):
        if top in wmap["topics"]:
            topic_links.append(wmap["topics"][top])
    
    if topic_links:
        lines.append("- " + " · ".join(topic_links))
    else:
        lines.append("- 관련 기술 토픽 없음")

    # 관련 기업 허브
    lines.append("\n### 🏢 관련 기업 허브 (Companies)")
    comp_links = []
    all_comps = set(extra_companies or [])
    for tid in thesis_ids:
        t = load_thesis_by_id(tid)
        if t:
            for c in t.get("related_companies", []):
                all_comps.add(c)

    for comp in sorted(all_comps):
        if comp in wmap["companies"]:
            comp_links.append(wmap["companies"][comp])
        else:
            comp_links.append(f"[[Company-{comp}|{comp}]]")

    if comp_links:
        lines.append("- " + " · ".join(comp_links))
    else:
        lines.append("- 관련 기업 허브 없음")

    # Master MOC 링크
    lines.append(f"\n### 🗺️ 인덱스 허브\n- {wmap['moc']}")

    return "\n".join(lines)


# ── 사용 예시 및 CLI ────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Argus Pulse — Thesis Loader & Momentum Ranking")
    parser.add_argument("--rank", "--momentum", action="store_true", help="시장 모멘텀 랭킹 출력")
    parser.add_argument("--sync", action="store_true", help="랭킹 계산 후 T-*.md frontmatter 갱신 및 옵시디언 동기화")
    parser.add_argument("--days", type=int, default=2, help="모멘텀 계산 기준 일수 (기본: 2일)")
    parser.add_argument("--limit", type=int, default=10, help="출력할 상위 테제 개수 (기본: 10개)")
    parser.add_argument("--all", action="store_true", help="active/watch 전체 포함")
    args = parser.parse_args()

    status_filter = None if args.all else "active"

    if args.sync:
        print(f"\n🔄 [Argus Pulse] 최근 {args.days}일간 모멘텀 랭킹 계산 및 Thesis MD 프론트매터 자동 갱신...")
        sync_thesis_ranks_to_files(days=args.days)

    if args.rank or not args.sync:
        print(f"\n🔥 [Argus Pulse] 최근 {args.days}일간 시장 모멘텀(News Momentum) Thesis 랭킹 Top {args.limit}")
        print("═" * 82)
        print(f"{'순위':^4} | {'ID':^6} | {'가설 제목':<24} | {'뉴스':^5} | {'모멘텀 점수':^10} | {'신뢰도':^6} | {'우선도':^5}")
        print("─" * 82)
        ranked_theses = get_thesis_momentum_ranking(days=args.days, status_filter=status_filter, limit=args.limit)
        for t in ranked_theses:
            print(f" {t['rank']:^3} | {t['id']:^6} | {t['title'][:22]:<24} | {t['news_count']:^5} | {t['momentum_score']:^10.1f} | {t['confidence']:^5}% | P{t.get('priority', 3)}")
        print("═" * 82)


