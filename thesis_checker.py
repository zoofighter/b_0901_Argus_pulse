"""
thesis_checker.py — 투자 가설(Thesis) 자동 점검 및 신뢰도(Confidence) 갱신 모듈

기능:
  - Active Thesis(기본) 또는 전체 Thesis 대상
  - 최근 뉴스 DB + ChromaDB 증권사 리포트 교차 대조
  - LLM을 통한 지지 근거 / 반박 근거 추출 및 신뢰도 변화량(delta: -15 ~ +15) 계산
  - Thesis MD 파일의 confidence, last_checked 및 본문 근거 섹션 자동 갱신
  - 변경된 Thesis 파일 옵시디언 자동 미러링

실행:
  python thesis_checker.py             # Active Thesis 전체 자동 점검
  python thesis_checker.py --id T-02   # 특정 Thesis 지정 점검
  python thesis_checker.py --all       # 38개 전체 Thesis 점검
"""

import argparse
import json
import re
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

import config
from llm_client import call_llm
from notifier import send_discord
from rag_engine import search as rag_search
from thesis_loader import (
    append_thesis_evidence,
    get_active_keywords,
    load_theses,
    load_thesis_by_id,
    update_thesis_confidence,
)


def fetch_recent_news_for_thesis(keywords: list[str], days: int = 7) -> list[dict]:
    """최근 N일간 키워드 일치 뉴스 조회"""
    if not config.NEWS_DB_PATH.exists() or not keywords:
        return []

    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    conn = sqlite3.connect(config.NEWS_DB_PATH)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT company, title, snippet, score, published
        FROM news
        WHERE published >= ? OR collected_at >= ?
        ORDER BY score DESC
        LIMIT 50
    """, (since, since)).fetchall()
    conn.close()

    matched = []
    for r in rows:
        text = f"{r['title']} {r['snippet'] or ''}"
        if any(kw in text for kw in keywords):
            matched.append(dict(r))
    return matched[:8]


def evaluate_thesis(thesis: dict, news_items: list[dict], rag_chunks: list[dict]) -> dict:
    """LLM을 통해 가설 지지/반박 근거 및 신뢰도 변동 점수 산출"""
    news_text = "\n".join([f"- [{n.get('company','')}] {n['title']} (점수: {n['score']})" for n in news_items]) or "(최근 7일 관련 뉴스 없음)"
    rag_text = "\n".join([f"- [{c['metadata'].get('company','')} | {c['metadata'].get('broker','')}] {c['text'][:150]}..." for c in rag_chunks]) or "(관련 증권사 리포트 청크 없음)"

    prompt = f"""당신은 엄격하고 객관적인 투자 전략가입니다.
아래 [투자 가설]에 대해 최근 관측된 [뉴스 팩트]와 [증권사 리포트 데이터]를 종합하여
가설의 유효성을 냉정하게 평가하고 JSON 형식으로만 응답하세요.

[투자 가설]
- ID: {thesis['id']}
- 제목: {thesis['title']}
- 핵심 가설: {thesis.get('hypothesis', '')}
- 방향성: {thesis.get('direction', 'bullish')}
- 현재 신뢰도: {thesis.get('confidence', 70)}%

[최근 7일 관련 뉴스]
{news_text}

[증권사 리포트 데이터]
{rag_text}

[평가 기준]
1. supporting_evidence: 가설을 뒷받침하는 새로운 팩트/수치 1문장 요약 (새로운 근거 없으면 "없음")
2. counter_evidence: 가설을 위협하거나 반박하는 리스크/팩트 1문장 요약 (반박 없으면 "없음")
3. confidence_delta: 신뢰도 변화량 정수 (-15 ~ +15 범위, 근거가 미미하면 0)
4. reason: 평가 이유 한 문장

반드시 아래 JSON 형식으로만 출력하세요:
```json
{{
  "supporting_evidence": "...",
  "counter_evidence": "...",
  "confidence_delta": 0,
  "reason": "..."
}}
```"""

    resp = call_llm(prompt)
    clean = re.sub(r"^```(?:json)?\n?", "", resp.strip())
    clean = re.sub(r"\n?```$", "", clean.strip())

    try:
        return json.loads(clean)
    except Exception as e:
        # JSON 파싱 실패 시 기본값
        print(f"  ⚠️ 평가 응답 JSON 파싱 실패: {e}")
        return {
            "supporting_evidence": "없음",
            "counter_evidence": "없음",
            "confidence_delta": 0,
            "reason": "LLM 파싱 오류"
        }


def check_thesis(thesis: dict) -> dict:
    """단일 Thesis 점검 및 갱신"""
    tid = thesis["id"]
    title = thesis["title"]
    curr_conf = int(thesis.get("confidence", 70))
    kws = thesis.get("keywords", [])

    print(f"\n🔍 [{tid}] {title} (현재 신뢰도: {curr_conf}%) 점검 중...")

    # 1. 최근 뉴스 수집
    news_items = fetch_recent_news_for_thesis(kws, days=7)
    # 2. RAG 증권사 리포트 검색
    rag_query = f"{title} {thesis.get('hypothesis', '')}"
    rag_chunks = rag_search(rag_query, n_results=3)

    # 3. LLM 평가
    eval_result = evaluate_thesis(thesis, news_items, rag_chunks)
    delta = int(eval_result.get("confidence_delta", 0))
    # 안전 제한: 1회 최대 ±15
    delta = max(-15, min(15, delta))
    new_conf = max(0, min(100, curr_conf + delta))

    supp = eval_result.get("supporting_evidence", "없음")
    counter = eval_result.get("counter_evidence", "없음")
    reason = eval_result.get("reason", "")

    today_str = date.today().isoformat()

    # 4. 파일 갱신
    if delta != 0:
        update_thesis_confidence(tid, new_conf)
        print(f"  📊 신뢰도 변동: {curr_conf}% → {new_conf}% ({delta:+d}%)")
    else:
        print(f"  📊 신뢰도 유지: {curr_conf}% (변동 없음)")

    if supp != "없음" or counter != "없음":
        append_thesis_evidence(tid, today_str, supporting=supp, counter=counter)
        if supp != "없음":
            print(f"  ✅ [지지 근거 추가] {supp}")
        if counter != "없음":
            print(f"  ⚠️ [반박 근거 추가] {counter}")

    # 옵시디언 동기화
    try:
        from obsidian_sync import sync_file
        # thesis 폴더는 옵시디언 vault/argus/Theses에 동기화
        vault_theses = config.OBSIDIAN_PATH / "argus" / "Theses"
        vault_theses.mkdir(parents=True, exist_ok=True)
        for md_file in config.THESIS_DIR.glob(f"{tid}-*.md"):
            import shutil
            shutil.copy2(md_file, vault_theses / md_file.name)
    except Exception:
        pass

    return {
        "id": tid,
        "title": title,
        "old_conf": curr_conf,
        "new_conf": new_conf,
        "delta": delta,
        "supporting": supp,
        "counter": counter,
        "reason": reason
    }


def run_checker(target_theses: list[dict]) -> list[dict]:
    """Thesis 목록 일괄 점검 실행"""
    print(f"\n🦅 [Thesis Checker] {len(target_theses)}개 가설 자동 점검 시작")
    results = []
    for t in target_theses:
        res = check_thesis(t)
        results.append(res)

    print("\n" + "═" * 60)
    print("📋 [Thesis 점검 종합 결과]")
    print("═" * 60)
    changed = []
    for r in results:
        sign = f"{r['delta']:+d}%" if r['delta'] != 0 else "유지"
        print(f"  [{r['id']}] {r['title'][:20]:<20} : {r['old_conf']}% → {r['new_conf']}% ({sign})")
        if r['delta'] != 0:
            changed.append(f"{r['id']} ({sign})")

    # Discord 알림
    if changed:
        send_discord(
            message=f"📊 **Thesis 신뢰도 자동 갱신 알림**\n변동 가설: `{', '.join(changed)}`"
        )

    return results


def main():
    parser = argparse.ArgumentParser(description="Argus Pulse — Thesis 자동 점검기")
    parser.add_argument("--id", type=str, help="특정 Thesis ID 지정 점검 (예: T-02)")
    parser.add_argument("--all", action="store_true", help="전체 38개 Thesis 점검")
    args = parser.parse_args()

    if args.id:
        t = load_thesis_by_id(args.id.upper())
        if not t:
            print(f"❌ Thesis를 찾을 수 없습니다: {args.id}")
            return
        run_checker([t])
    elif args.all:
        theses = load_theses(status_filter=None)
        run_checker(theses)
    else:
        # 기본: Active Thesis 점검
        theses = load_theses(status_filter="active")
        run_checker(theses)


if __name__ == "__main__":
    main()
