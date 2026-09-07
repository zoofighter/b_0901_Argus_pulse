"""
theme_discoverer.py — 미매칭(Orphan) 고득점 뉴스 기반 신규 테마 조기 발굴기

기능:
  1. news.sqlite에서 최근 N일간 score >= 70 이면서 43개 정식 테제에 매칭되지 않은 고득점 뉴스(Orphan News) 격리
  2. 키워드 급증(Spike) 분석 및 LLM 테마 군집화(Clustering)
  3. 유망 테마 발견 시 thesis/Incubator/TC-XX-[테마명].md 자동 생성
  4. 옵시디언 볼트(obs_argus/argus/Incubator/) 자동 동기화 및 디스코드 알림 발송

실행:
  python theme_discoverer.py               # 기본 실행 (최근 7일, 70점 이상)
  python theme_discoverer.py --days 3     # 최근 3일 대상
  python theme_discoverer.py --dry-run    # 파일 생성 없이 후보만 출력
"""

import argparse
import json
import re
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import config
from llm_client import call_llm
from notifier import notify_new_theme_candidate
from thesis_loader import get_active_keywords


INCUBATOR_DIR = config.THESIS_DIR / "Incubator"


def fetch_orphan_news(days: int = 7, min_score: int = 70) -> list[dict]:
    """최근 N일간 min_score 이상이면서 43개 테제와 0건 매칭된 뉴스 격리 추출"""
    if not config.NEWS_DB_PATH.exists():
        print("  ⚠️ news.sqlite 데이터베이스가 존재하지 않습니다.")
        return []

    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    conn = sqlite3.connect(config.NEWS_DB_PATH)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT id, company, title, snippet, score, source, published, url
        FROM news
        WHERE score >= ? AND (published >= ? OR collected_at >= ?)
        ORDER BY score DESC
        LIMIT 200
    """, (min_score, since, since)).fetchall()
    conn.close()

    if not rows:
        return []

    kmap = get_active_keywords()
    orphans = []

    for r in rows:
        text = f"{r['title']} {r['snippet'] or ''}"
        # 43개 테제 키워드와 단 하나라도 일치하는지 확인
        matched = False
        for tid, kws in kmap.items():
            if any(str(kw) in text for kw in kws):
                matched = True
                break

        if not matched:
            orphans.append(dict(r))

    return orphans


def get_next_tc_id() -> str:
    """Incubator 폴더를 스캔하여 다음 TC-XX 번호 생성"""
    INCUBATOR_DIR.mkdir(parents=True, exist_ok=True)
    existing_files = list(INCUBATOR_DIR.glob("TC-*.md"))
    max_num = 0
    for f in existing_files:
        m = re.match(r"TC-(\d+)", f.name)
        if m:
            num = int(m.group(1))
            if num > max_num:
                max_num = num
    return f"TC-{max_num + 1:02d}"


def cluster_orphan_news(orphan_news: list[dict]) -> list[dict]:
    """LLM을 통해 미매칭 고득점 뉴스들을 분석하고 잠재 신규 테마로 군집화"""
    if not orphan_news:
        return []

    news_list_str = "\n".join([
        f"[{i+1}] 기업: {n['company']} | 점수: {n['score']}점 | 제목: {n['title']} | 내용: {(n['snippet'] or '')[:120]}"
        for i, n in enumerate(orphan_news[:35])  # 토큰 효율성을 위해 상위 35건 대상
    ])

    prompt = f"""당신은 첨단 기술 트렌드와 산업 지형을 선제적으로 읽어내는 월스트리트 수석 리서치 애널리스트입니다.
아래 뉴스들은 기존 43개 핵심 투자 가설에 매칭되지 않은 '미매칭 고득점(70점+) 뉴스들'입니다.

이 뉴스들 속에서 최근 새롭게 태동하거나 강한 모멘텀을 형성하고 있는 **'신규 투자 테마 후보(Emerging Theme Candidates)'**를 식별하세요.
단발성 개별 기업 가십이 아니라, **향후 1~3년간 시장을 주도할 수 있는 기술 혁신, 병목 해결, 또는 산업 구조 변화**를 2건 이상 묶어서 추출하세요.

[미매칭 고득점 뉴스 목록]
{news_list_str}

[출력 지침]
- 유의미한 테마가 없으면 빈 리스트 []를 반환하세요.
- 발견된 테마는 최대 3개까지만 도출하세요.
- 각 테마는 2개 이상의 뉴스 기사를 근거로 묶여야 합니다.
- sector_candidate는 젠슨 황 5-Layer & Argus 6대 섹터 코드 중 하나를 지정하세요:
  - "T1" (에너지·전력·냉각 인프라)
  - "T2" (AI 컴퓨트·메모리·선단반도체)
  - "T3" (초고속 네트워킹·시스템 플랫폼)
  - "T4" (파운데이션 모델·엔터프라이즈 SW)
  - "T5" (피지컬 AI·자율주행·로보틱스)
  - "T6" (매크로 자본시장·밸류에이션·지정학 안보)

반드시 아래 JSON 형식으로만 응답하세요:
```json
[
  {{
    "theme_name": "간결하고 명확한 테마 명칭 (예: 광집적 CPO 기반 분산 스위치 패브릭)",
    "sector_candidate": "T3",
    "hypothesis": "가설을 명확하게 서술하는 1~2문장",
    "why_now": "왜 지금 이 테마가 부상하고 있는지 산업적 배경 2문장",
    "keywords": ["핵심키워드1", "핵심키워드2", "핵심키워드3"],
    "related_companies": ["기업1", "기업2"],
    "promotion_triggers": ["정식 테제 승격 조건1", "승격 조건2"],
    "matched_news_indices": [1, 5]
  }}
]
```"""

    resp = call_llm(prompt)
    clean = re.sub(r"^```(?:json)?\n?", "", resp.strip())
    clean = re.sub(r"\n?```$", "", clean.strip())

    try:
        data = json.loads(clean)
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"  ⚠️ 테마 클러스터링 JSON 파싱 오류: {e}")
        return []


def create_incubator_file(theme: dict, orphan_news: list[dict], tc_id: Optional[str] = None, dry_run: bool = False) -> Optional[Path]:
    """후보 테제를 thesis/Incubator/TC-XX.md 파일로 생성하고 동기화"""
    if not tc_id:
        tc_id = get_next_tc_id()
    theme_name = theme.get("theme_name", "미정").strip()
    slug = re.sub(r"[^\w\s-]", "", theme_name).strip().replace(" ", "-")
    filename = f"{tc_id}-{slug}.md"
    filepath = INCUBATOR_DIR / filename

    today_str = datetime.now().strftime("%Y-%m-%d")
    matched_indices = theme.get("matched_news_indices", [])
    matched_news = [orphan_news[idx - 1] for idx in matched_indices if 1 <= idx <= len(orphan_news)]

    sector_code = theme.get("sector_candidate", "T2")
    sector_names = {
        "T1": "AI 데이터센터 & 전력·냉각 인프라",
        "T2": "AI 컴퓨트 & 차세대 반도체",
        "T3": "초고속 네트워킹 & 시스템 플랫폼",
        "T4": "파운데이션 모델 & 엔터프라이즈 SW",
        "T5": "피지컬 AI & 자율주행·로보틱스",
        "T6": "매크로 자본시장 & 지정학 안보",
    }
    sector_name = f"{sector_names.get(sector_code, 'AI 신기술')} (후보)"

    news_md_list = "\n".join([
        f"- **[{n.get('company', '시장')}]** {n['title']} (점수: {n['score']}점, 출처: {n.get('source', '')})"
        for n in matched_news
    ]) or "- 포착된 관련 뉴스 없음"

    content = f"""---
id: {tc_id}
title: "{theme_name}"
sector: "{sector_name}"
sector_candidate: "{sector_code}"
stage: "candidate"
incubation_score: 75
first_detected: "{today_str}"
observation_days: 14
news_count: {len(matched_news)}
keywords:
{chr(10).join(f'  - "{kw}"' for kw in theme.get('keywords', []))}
candidate_companies:
{chr(10).join(f'  - "{cp}"' for cp in theme.get('related_companies', []))}
promotion_triggers:
{chr(10).join(f'  - "{tr}"' for tr in theme.get('promotion_triggers', []))}
aliases:
  - {tc_id}
  - {tc_id} {theme_name}
---

# 🧭 {tc_id} {theme_name}

> **신규 테마 인큐베이션 (Stage: Candidate / 관찰 기간: 14일)**  
> {theme.get('hypothesis', '')}

---

## 1. 신규 테마 발굴 배경 (Why Now)
- **발굴 계기**: 최근 미매칭 고득점 뉴스 풀에서 {len(matched_news)}건의 유관 뉴스가 집중 군집되어 후보 가설로 등록되었습니다.
- **산업적 배경**: {theme.get('why_now', '해당 기술 영역의 투자 가시성 급상승 중.')}

---

## 2. 초기 포착된 뉴스 및 데이터
{news_md_list}

---

## 3. 정식 테제 승격 체크리스트 (Promotion Checklist)
- [x] **초기 약한 신호 감지**: 고득점 뉴스 군집 확인 ({today_str} 포착)
- [ ] **후속 뉴스 유입 지속성**: 향후 14일간 주간 3건 이상 유입 유지
- [ ] **빅테크/공급망 촉매**: 관련 기업의 공식 투자 공시 또는 시제품 벤치마크 공개
- [ ] **기각 리스크 검토**: 대체 기술 대비 경제성 및 채택 속도 검증
"""

    if dry_run:
        print(f"\n[DRY RUN] 생성 예정 후보 테제: {filename}")
        print(f"  - 테마명: {theme_name}")
        print(f"  - 섹터: {sector_code}")
        print(f"  - 가설: {theme.get('hypothesis', '')}")
        print(f"  - 근거 뉴스: {len(matched_news)}건")
        return None

    filepath.write_text(content, encoding="utf-8")
    print(f"  🌱 [후보 테제 생성] {filepath.name}")

    # 옵시디언 동기화
    try:
        from obsidian_sync import sync_file
        sync_file(filepath, "incubator")
    except Exception as e:
        print(f"  ⚠️ 옵시디언 동기화 실패: {e}")

    # 디스코드 알림 발송
    notify_new_theme_candidate(
        theme_name=theme_name,
        hypothesis=theme.get("hypothesis", ""),
        companies=theme.get("related_companies", []),
        orphan_count=len(matched_news),
        tc_filename=filename
    )

    return filepath


def run_discovery(days: int = 7, min_score: int = 70, dry_run: bool = False) -> list[dict]:
    """신규 테마 발굴 전체 파이프라인 실행"""
    print(f"\n🔍 [Theme Discoverer] 최근 {days}일간 미매칭 고득점({min_score}점+) 뉴스 추출 중...")
    orphans = fetch_orphan_news(days=days, min_score=min_score)
    print(f"  📊 미매칭 고득점 뉴스(Orphan News): {len(orphans)}건 포착")

    if len(orphans) < 2:
        print("  ℹ️ 군집화를 위한 미매칭 고득점 뉴스가 충분하지 않습니다 (최소 2건 필요).")
        return []

    print("  🧠 LLM 기반 테마 이상 급증(Spike) 및 군집화 분석 중...")
    themes = cluster_orphan_news(orphans)
    print(f"  🎯 발굴된 신규 테마 후보: {len(themes)}개")

    # 시작 TC 번호 계산
    INCUBATOR_DIR.mkdir(parents=True, exist_ok=True)
    existing_files = list(INCUBATOR_DIR.glob("TC-*.md"))
    max_num = 0
    for f in existing_files:
        m = re.match(r"TC-(\d+)", f.name)
        if m:
            max_num = max(max_num, int(m.group(1)))

    results = []
    for i, t in enumerate(themes):
        curr_id = f"TC-{max_num + 1 + i:02d}"
        res = create_incubator_file(t, orphans, tc_id=curr_id, dry_run=dry_run)
        results.append({"theme": t, "path": str(res) if res else None})

    return results



def main():
    parser = argparse.ArgumentParser(description="Argus Pulse — 미매칭 뉴스 기반 신규 테마 발굴기")
    parser.add_argument("--days", type=int, default=7, help="분석 대상 최근 일수 (기본: 7일)")
    parser.add_argument("--min-score", type=int, default=70, help="최소 뉴스 점수 (기본: 70점)")
    parser.add_argument("--dry-run", action="store_true", help="파일 생성 없이 분석 결과만 터미널에 출력")
    args = parser.parse_args()

    run_discovery(days=args.days, min_score=args.min_score, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
