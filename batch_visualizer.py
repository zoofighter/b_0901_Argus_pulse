"""
batch_visualizer.py — Argus Pulse 배치 실행 모니터링 및 옵시디언 시각화 대시보드 자동 생성기

기능:
  1. logs/ 디렉터리의 각 배치 크론 로그 상태(성공, 실패, 대기, 실행시각) 파싱
  2. 오늘 날짜로 생성된 인텔리전스 산출물(Blog, Brief, Digest, Incubator) 집계
  3. 옵시디언 볼트용 마스터 대시보드 노트(00-Argus-Pipeline-Dashboard.md) 생성 및 동기화
  4. 옵시디언 인터랙티브 캔버스 파이프라인 맵(00-Argus-Batch-Pipeline.canvas) 생성 및 동기화
  5. 터미널 콘솔 컬러 상태 요약표 출력

실행:
  python batch_visualizer.py          # 대시보드 및 캔버스 자동 빌드 & 볼트 동기화
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import config

DASHBOARD_MD_PATH = config.THESIS_DIR / "00-Argus-Pipeline-Dashboard.md"
PIPELINE_CANVAS_PATH = config.THESIS_DIR / "00-Argus-Batch-Pipeline.canvas"

BATCH_TASKS = [
    {
        "time": "08:00",
        "name": "아침 주제 추천 & 기획안 생성",
        "module": "topic_generator.py --auto",
        "log": "cron_topic.log",
        "target_dir": "output/outline",
        "obsidian_folder": "argus/Outline",
        "stage": "Morning"
    },
    {
        "time": "08:05",
        "name": "미매칭 뉴스 기반 신규 테마 발굴",
        "module": "theme_discoverer.py",
        "log": "cron_theme.log",
        "target_dir": "thesis/Incubator",
        "obsidian_folder": "argus/Incubator",
        "stage": "Morning"
    },
    {
        "time": "09:00~21:00",
        "name": "실시간 뉴스 감시 (매 정각)",
        "module": "hourly_monitor.py --once",
        "log": "cron_monitor.log",
        "target_dir": "logs",
        "obsidian_folder": "argus",
        "stage": "Hourly"
    },
    {
        "time": "13:00",
        "name": "오후 블로그 사후 검증 리뷰 (RAG)",
        "module": "review_generator.py --rag",
        "log": "cron_review.log",
        "target_dir": "output/review",
        "obsidian_folder": "argus/Review",
        "stage": "Midday"
    },
    {
        "time": "13:05",
        "name": "변곡점 1-Page 투자 메모 작성",
        "module": "thesis_brief_writer.py --inflection-only",
        "log": "cron_brief.log",
        "target_dir": "output/brief",
        "obsidian_folder": "argus/Review",
        "stage": "Midday"
    },
    {
        "time": "21:00",
        "name": "데일리 다이제스트 종합 요약 (RAG)",
        "module": "daily_digest.py --rag",
        "log": "cron_digest.log",
        "target_dir": "output/digest",
        "obsidian_folder": "argus/Digest",
        "stage": "Nightly"
    },
    {
        "time": "21:05",
        "name": "테제 마일스톤/기각 감사 & 모멘텀 랭킹",
        "module": "thesis_checker.py --smart",
        "log": "cron_checker.log",
        "target_dir": "thesis",
        "obsidian_folder": "argus/Theses",
        "stage": "Nightly"
    }
]


def check_task_log(log_filename: str) -> dict:
    """로그 파일 상태를 점검하여 실행 결과, 시각, 상태 배지 반환"""
    log_path = config.ROOT_DIR / "logs" / log_filename
    today = datetime.now().date()

    if not log_path.exists():
        return {
            "status": "⏳ 미실행",
            "badge": "🔴 미기록",
            "last_run": "-",
            "summary": "로그 파일 없음",
            "is_today": False,
            "has_error": False
        }

    stat = log_path.stat()
    last_dt = datetime.fromtimestamp(stat.st_mtime)
    is_today = (last_dt.date() == today)
    time_str = last_dt.strftime("%Y-%m-%d %H:%M:%S")

    # 최근 10줄 읽기
    try:
        lines = log_path.read_text(encoding="utf-8", errors="replace").strip().splitlines()
        tail = lines[-10:] if lines else []
    except Exception:
        tail = []

    has_error = any("Traceback" in l or "Error" in l or "실패" in l or "Exception" in l for l in tail)
    last_line = tail[-1].strip() if tail else "로그 내용 없음"
    # 앞쪽 ANSI 코드 등 제거
    last_line = last_line[:80]

    if is_today:
        if has_error:
            status = "🚨 에러"
            badge = "❌ 실패"
        else:
            status = "✅ 정상"
            badge = "🟢 성공"
    else:
        status = "⏳ 대기 중"
        badge = "⚪ 과거 기록"

    return {
        "status": status,
        "badge": badge,
        "last_run": time_str,
        "summary": last_line,
        "is_today": is_today,
        "has_error": has_error
    }


def get_today_artifacts() -> dict:
    """오늘 날짜로 생성된 주요 산출물 파일 리스트 집계"""
    today_str = datetime.now().strftime("%Y-%m-%d")
    artifacts = {
        "briefs": list(config.OUTPUT_DIR.glob(f"brief/{today_str}-*.md")),
        "reviews": list(config.OUTPUT_DIR.glob(f"review/{today_str}-*.md")),
        "digests": list(config.OUTPUT_DIR.glob(f"digest/{today_str}-*.md")),
        "blogs": list(config.OUTPUT_DIR.glob(f"blog/{today_str}-*.md")),
        "outlines": list(config.OUTPUT_DIR.glob(f"outline/{today_str}-*.md")),
        "incubator": [
            f for f in (config.THESIS_DIR / "Incubator").glob("TC-*.md")
            if today_str in f.read_text(encoding="utf-8", errors="replace")
        ]
    }
    return artifacts


def generate_markdown_dashboard(task_statuses: list[dict], artifacts: dict) -> str:
    """옵시디언 마크다운 대시보드 노트 생성"""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    today_str = datetime.now().strftime("%Y-%m-%d")

    # 전체 상태 요약 계산
    total_today = sum(1 for t in task_statuses if t["log_info"]["is_today"])
    total_error = sum(1 for t in task_statuses if t["log_info"]["has_error"])
    health_status = "🟢 ALL SYSTEMS OPERATIONAL" if total_error == 0 else f"🚨 ATTENTION REQUIRED ({total_error} ERRORS)"

    table_rows = []
    for t in task_statuses:
        info = t["log_info"]
        table_rows.append(
            f"| **`{t['time']}`** | **{t['name']}** | `{t['module']}` | {info['badge']} | `{info['last_run']}` | {info['summary']} | `[[{t['obsidian_folder']}|📂 바로가기]]` |"
        )

    # 산출물 불릿 생성
    artifact_lines = []
    for cat, files in artifacts.items():
        if files:
            file_links = ", ".join([f"`[[{f.name}]]`" for f in files[:4]])
            artifact_lines.append(f"- **{cat.upper()} ({len(files)}건)**: {file_links}")
    if not artifact_lines:
        artifact_lines.append("- *(금일 아직 생성된 자동화 산출물이 없습니다)*")

    content = f"""---
title: "Argus Pulse — 24시간 자동화 파이프라인 대시보드"
type: system-dashboard
created: {today_str}
updated: {now_str}
tags:
  - argus-pulse
  - system-dashboard
  - pipeline-status
  - devops
---

# 🦅 Argus Pulse 24시간 자동화 파이프라인 관제 대시보드

> **시스템 상태**: `{health_status}`  
> **최근 점검 시각**: `{now_str}` | **옵시디언 볼트**: `obs_argus`

---

## 🗺️ 24시간 인터랙티브 파이프라인 가치사슬 맵

```mermaid
flowchart LR
    subgraph S1 ["🌅 08:00 아침 인텔리전스"]
        A1["아침 기획안 추천<br/>(topic_generator.py)"]
        A2["🌱 신규 테마 발굴<br/>(theme_discoverer.py)"]
    end

    subgraph S2 ["🔍 09:00~21:00 실시간 감시"]
        B1["80점+ 핫뉴스 모니터링<br/>(hourly_monitor.py)"]
        B2["Orphan News 풀 격리"]
    end

    subgraph S3 ["☀️ 13:00 오후 사후검증 & 투자메모"]
        C1["블로그 사후검증 리뷰<br/>(review_generator.py)"]
        C2["🎯 1-Page 투자 메모<br/>(thesis_brief_writer.py)"]
    end

    subgraph S4 ["🌙 21:00 야간 종합 & 테제 감사"]
        D1["데일리 다이제스트<br/>(daily_digest.py)"]
        D2["🚨 마일스톤/기각 감사<br/>(thesis_checker.py)"]
    end

    S1 -->|아침 뉴스 팩트| S2
    S2 -->|오전 핫뉴스 전달| S3
    S3 -->|변곡점 감시 지속| S2
    S2 -->|일일 누적 데이터| S4
    S4 -->|마스터 MOC 갱신| MOC["🧭 Master MOC<br/>& 5-Layer Canvas"]

    style S1 fill:#ecfdf5,stroke:#10b981,stroke-width:2px
    style S2 fill:#fef3c7,stroke:#f59e0b,stroke-width:2px
    style S3 fill:#fee2e2,stroke:#ef4444,stroke-width:2px
    style S4 fill:#f3e8ff,stroke:#a855f7,stroke-width:2px
    style MOC fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#ffffff
```

> 💡 **캔버스 뷰어**: **[[00-Argus-Batch-Pipeline.canvas|🎨 24시간 파이프라인 전용 캔버스 보드 열기]]**

---

## 🚦 배치 실행 현황 모니터링 (Live Health Check)

| 스케줄 | 파이프라인 단계 | 실행 모듈 | 상태 | 최근 실행 시각 | 최종 로그 요약 | 산출물 위치 |
|:---:|:---|:---|:---:|:---:|:---|:---:|
{chr(10).join(table_rows)}

---

## 📦 금일 생성된 주요 인텔리전스 산출물 ({today_str})

{chr(10).join(artifact_lines)}

---

## 📊 Dataview 실시간 인텔리전스 허브

### 🎯 1. 최근 생성된 1-Page 투자 메모 (Thesis Briefs)
```dataview
TABLE file.mtime AS "작성시각", thesis_id AS "테제 ID", confidence AS "신뢰도", status AS "상태"
FROM "argus/Review" OR "Review"
WHERE contains(file.name, "brief")
SORT file.mtime DESC
LIMIT 5
```

### 🌱 2. 인큐베이션 중인 신규 테마 후보 (Emerging Theses)
```dataview
TABLE first_detected AS "발굴일자", sector_candidate AS "추천섹터", news_count AS "근거뉴스", stage AS "단계"
FROM "argus/Incubator" OR "Incubator"
SORT file.mtime DESC
LIMIT 5
```

### 🚨 3. 최근 변곡점/마일스톤 경보 테제
```dataview
TABLE confidence AS "신뢰도", milestone_status AS "마일스톤 상태", falsification_triggered AS "기각 여부", last_checked AS "점검시각"
FROM "argus/Theses" OR "Theses"
WHERE milestone_status != "NONE" OR falsification_triggered = true
SORT last_checked DESC
LIMIT 5
```

---

## 🛠️ 터미널 빠른 수동 실행 명령어 (CLI Shortcuts)

```bash
# 1. 24시간 배치 상태 즉시 새로고침
python batch_visualizer.py

# 2. 미매칭 뉴스 기반 신규 테마 발굴 실행
python theme_discoverer.py

# 3. 1-Page 투자 메모 즉시 작성 (특정 테제)
python thesis_brief_writer.py --id T2-01

# 4. 전체 테제 신뢰도 및 마일스톤 스마트 감사
python thesis_checker.py --smart
```
"""
    return content


def generate_pipeline_canvas(task_statuses: list[dict]) -> dict:
    """옵시디언 캔버스(00-Argus-Batch-Pipeline.canvas) JSON 데이터 생성"""
    nodes = []
    edges = []

    # Title Node
    nodes.append({
        "id": "header",
        "x": 0,
        "y": -400,
        "width": 1400,
        "height": 100,
        "type": "text",
        "text": "# ⚙️ Argus Pulse 24시간 자율 배치 파이프라인 캔버스 (Live Architecture)\n> 데이터 수집 ➔ 모니터링 ➔ 1-Page 투자 메모 ➔ 종합 다이제스트 ➔ 5-Layer MOC 갱신"
    })

    # Stages and x-coordinates
    stages_cfg = [
        {"stage": "Morning", "title": "🌅 08:00 아침 인텔리전스", "x": 0, "color": "4"},
        {"stage": "Hourly", "title": "🔍 09:00~21:00 실시간 감시", "x": 380, "color": "3"},
        {"stage": "Midday", "title": "☀️ 13:00 사후검증 & 변곡점", "x": 760, "color": "1"},
        {"stage": "Nightly", "title": "🌙 21:00 야간 다이제스트", "x": 1140, "color": "5"},
    ]

    for sc in stages_cfg:
        nodes.append({
            "id": f"group_{sc['stage']}",
            "x": sc["x"],
            "y": -260,
            "width": 340,
            "height": 70,
            "type": "text",
            "text": f"### {sc['title']}"
        })

    # Task Cards
    stage_counters = {"Morning": 0, "Hourly": 0, "Midday": 0, "Nightly": 0}
    prev_stage_last_node = None

    for i, t in enumerate(task_statuses):
        stage = t["stage"]
        sc_info = next(s for s in stages_cfg if s["stage"] == stage)
        y_pos = -160 + stage_counters[stage] * 220
        stage_counters[stage] += 1

        node_id = f"task_node_{i+1}"
        info = t["log_info"]
        card_text = f"**{t['time']} | {t['name']}**\n\n- 모듈: `{t['module']}`\n- 상태: **{info['badge']}**\n- 최근 실행: `{info['last_run']}`\n- 폴더: `{t['obsidian_folder']}`\n- 요약: {info['summary'][:60]}"

        nodes.append({
            "id": node_id,
            "x": sc_info["x"],
            "y": y_pos,
            "width": 340,
            "height": 190,
            "type": "text",
            "text": card_text
        })

    # Horizontal Flow Edges
    edges.append({
        "id": "e_m_to_h",
        "fromNode": "task_node_1",
        "fromSide": "right",
        "toNode": "task_node_3",
        "toSide": "left",
        "label": "신규 테마 & 추천 기획안 인계"
    })
    edges.append({
        "id": "e_h_to_mid",
        "fromNode": "task_node_3",
        "fromSide": "right",
        "toNode": "task_node_4",
        "toSide": "left",
        "label": "오전 핫뉴스 ➔ 사후 검증 및 투자메모 작성"
    })
    edges.append({
        "id": "e_mid_to_night",
        "fromNode": "task_node_5",
        "fromSide": "right",
        "toNode": "task_node_6",
        "toSide": "left",
        "label": "변곡점 테제 ➔ 일일 종합 다이제스트 반영"
    })

    return {"nodes": nodes, "edges": edges}


def run_visualizer():
    """배치 상태 수집, 대시보드 마크다운 및 캔버스 빌드, 볼트 동기화"""
    print("\n🔍 [Batch Visualizer] 24시간 파이프라인 실행 상태 수집 중...")
    task_statuses = []
    for t in BATCH_TASKS:
        t_copy = dict(t)
        t_copy["log_info"] = check_task_log(t["log"])
        task_statuses.append(t_copy)

    artifacts = get_today_artifacts()

    # 1. 마크다운 대시보드 파일 생성
    md_content = generate_markdown_dashboard(task_statuses, artifacts)
    DASHBOARD_MD_PATH.write_text(md_content, encoding="utf-8")
    print(f"  📄 [대시보드 노트 생성] {DASHBOARD_MD_PATH.name}")

    # 2. 캔버스 파일 생성
    canvas_data = generate_pipeline_canvas(task_statuses)
    PIPELINE_CANVAS_PATH.write_text(json.dumps(canvas_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  🎨 [파이프라인 캔버스 생성] {PIPELINE_CANVAS_PATH.name}")

    # 3. 옵시디언 볼트 동기화
    try:
        from obsidian_sync import sync_file
        # 대시보드는 argus 루트에 동기화
        sync_file(DASHBOARD_MD_PATH, "moc")
        sync_file(PIPELINE_CANVAS_PATH, "canvas")
        print(f"  📓 [Obsidian 동기화 완료] obs_argus 볼트 반영")
    except Exception as e:
        print(f"  ⚠️ 옵시디언 동기화 실패: {e}")

    # 4. 콘솔 요약표 출력
    print("\n" + "═" * 78)
    print("🦅 Argus Pulse 24시간 배치 파이프라인 현황")
    print("═" * 78)
    for t in task_statuses:
        info = t["log_info"]
        print(f"  {t['time']:<12} | {t['name']:<24} | {info['badge']:<8} | {info['last_run']}")
    print("═" * 78)


if __name__ == "__main__":
    run_visualizer()
