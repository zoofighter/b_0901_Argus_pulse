"""
notifier.py — 알림 모듈 (Discord 웹훅 / 콘솔 로깅)

기능:
  - 고득점 뉴스 감지 알림
  - 오늘의 주제 추천 완료 알림
  - 블로그 / 스레드 생성 완료 알림
  - 데일리 다이제스트 전송
"""

import json
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
import config


def send_discord(message: str, embeds: list[dict] = None) -> bool:
    """디스코드 웹훅 전송. 미설정 시 콘솔 출력만 수행."""
    if not config.DISCORD_WEBHOOK:
        # 웹훅 URL이 없으면 조용히 True 반환 (로컬 모드)
        return True

    payload = {"content": message}
    if embeds:
        payload["embeds"] = embeds

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            config.DISCORD_WEBHOOK,
            data=data,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "ArgusPulseNotifier/1.0"
            }
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status in (200, 204)
    except Exception as e:
        print(f"  ⚠️  디스코드 전송 실패: {e}")
        return False


def notify_hot_news(news: dict, matched_thesis_ids: list[str]) -> bool:
    """80점 이상 핫 뉴스 발생 시 즉각 알림"""
    company = news.get("company") or news.get("source") or "시장"
    title = news.get("title", "")
    score = news.get("score", 0)
    thesis_str = ", ".join(matched_thesis_ids) if matched_thesis_ids else "미매칭"

    embed = {
        "title": f"🚨 [속보/고득점 뉴스] {score}점 — {company}",
        "description": f"**{title}**\n\n- 관련 Thesis: `{thesis_str}`\n- 출처: {news.get('source', '')}",
        "color": 0xFF4500,  # 오렌지레드
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    print(f"📢 [알림] 핫 뉴스: [{score}점] {company} - {title}")
    return send_discord(message=f"🔥 **{company}** 고득점 뉴스 감지 ({score}점)", embeds=[embed])


def notify_topics_ready(topics: list[dict]) -> bool:
    """오늘의 추천 주제가 준비되었을 때 알림"""
    fields = []
    for t in topics[:3]:
        rank = t.get("rank", "")
        title = t.get("title", "")
        angle = t.get("angle", "")
        thesis = ", ".join(t.get("thesis_ids", []))
        fields.append({
            "name": f"[{rank}] {title}",
            "value": f"관점: {angle} | Thesis: `{thesis}`\n훅: {t.get('hook', '')}",
            "inline": False
        })

    embed = {
        "title": "📋 오늘의 Argus Pulse 콘텐츠 기획안 도착",
        "description": "새로운 추천 주제 3개가 생성되었습니다. 터미널에서 선택해주세요.",
        "fields": fields,
        "color": 0x1E90FF,  # 도저블루
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    return send_discord(message="💡 **오늘의 콘텐츠 기획안이 도착했습니다.**", embeds=[embed])


def notify_content_generated(content_type: str, title: str, filepath: str | Path, summary: str = "") -> bool:
    """블로그 또는 스레드 생성 완료 알림"""
    path_obj = Path(filepath)
    embed = {
        "title": f"✅ {content_type.upper()} 초안 생성 완료",
        "description": f"**{title}**\n\n파일 경로:\n`{path_obj.name}`\n\n{summary[:200]}",
        "color": 0x32CD32,  # 라임그린
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    print(f"📢 [알림] {content_type} 생성 완료: {title}")
    return send_discord(message=f"🎉 **{content_type}** 초안 생성이 완료되었습니다!", embeds=[embed])


def notify_thesis_inflection(thesis: dict, eval_result: dict, old_conf: int, new_conf: int) -> bool:
    """테제 신뢰도 급변(±10p), 마일스톤 달성, 또는 가설 기각 발생 시 디스코드 긴급 경보"""
    tid = thesis.get("id", "")
    title = thesis.get("title", "")
    delta = new_conf - old_conf

    milestone_status = eval_result.get("milestone_status", "NONE")
    falsification_triggered = bool(eval_result.get("falsification_triggered", False))

    # 발송 조건 점검: |delta| >= 10, milestone ACHIEVED, 또는 falsification_triggered
    is_inflection = abs(delta) >= 10 or milestone_status == "ACHIEVED" or falsification_triggered
    if not is_inflection:
        return True

    # 색상 및 태그 결정
    if falsification_triggered:
        color = 0xFF0000  # 적색 (Red Flag)
        tag = "🚨 [가설 기각 트리거 발생 (Red Flag)]"
        action = "포트폴리오 해당 테제 관련 자산 비중 축소 및 전면 재검토 필요"
    elif milestone_status == "ACHIEVED":
        color = 0x00FF00  # 녹색 (Milestone Hit)
        tag = "🎯 [핵심 마일스톤 달성 (Catalyst Hit)]"
        action = "단기 모멘텀 확인, 밸류에이션 반영률 및 차기 마일스톤 점검"
    elif delta >= 10:
        color = 0xFFA500  # 황색 (Positive Inflection)
        tag = f"⚡ [신뢰도 대폭 상향 경보 (+{delta}%p)]"
        action = "가설 지지 팩트 지속성 확인 및 비중 확대 기회 탐색"
    else:
        color = 0xFF6347  # 토마토 레드 (Negative Inflection)
        tag = f"⚠️ [신뢰도 대폭 하향 경보 ({delta}%p)]"
        action = "가설 훼손 요인 및 경쟁 리스크 확인 후 리스크 관리"

    fields = [
        {"name": "신뢰도 변화", "value": f"`{old_conf}%` ➔ `{new_conf}%` ({delta:+d}%p)", "inline": True},
        {"name": "마일스톤 상태", "value": f"`{milestone_status}`\n{eval_result.get('milestone_evidence', '없음')[:120]}", "inline": True},
    ]

    if falsification_triggered:
        fields.append({
            "name": "🚨 기각 조건 도달 사유",
            "value": eval_result.get("falsification_reason", "조건 충족"),
            "inline": False
        })

    supp = eval_result.get("supporting_evidence", "없음")
    counter = eval_result.get("counter_evidence", "없음")
    if supp != "없음":
        fields.append({"name": "✅ 지지 팩트 (Bull)", "value": supp, "inline": False})
    if counter != "없음":
        fields.append({"name": "⚠️ 반박/리스크 (Bear)", "value": counter, "inline": False})

    fields.append({"name": "💡 대응 액션 가이드", "value": action, "inline": False})

    embed = {
        "title": f"{tag} [{tid}] {title}",
        "description": f"**핵심 가설**: {thesis.get('hypothesis', '')}\n**평가 근거**: {eval_result.get('reason', '')}",
        "fields": fields,
        "color": color,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    print(f"📢 [긴급 경보] {tag} [{tid}] {title} ({old_conf}% -> {new_conf}%)")
    return send_discord(message=f"🚨 **Argus Pulse 가설 변곡점 긴급 경보** — [{tid}] {title}", embeds=[embed])


def notify_new_theme_candidate(theme_name: str, hypothesis: str, companies: list[str], orphan_count: int, tc_filename: str) -> bool:
    """신규 테마 후보(Incubator/TC-XX) 발굴 시 디스코드 알림"""
    comp_str = ", ".join(companies) if companies else "미정"
    embed = {
        "title": f"🌱 [신규 테마 발굴] {theme_name}",
        "description": f"**핵심 가설**: {hypothesis}\n\n- 미매칭 고득점 뉴스: **{orphan_count}건** 군집\n- 관련 기업: `{comp_str}`\n- 후보 테제: `Incubator/{tc_filename}`",
        "color": 0x9370DB,  # 미디엄 퍼플
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    print(f"📢 [신규 테마 발굴] {theme_name} ({orphan_count}건 뉴스)")
    return send_discord(message=f"🌟 **신규 테마 후보가 발굴되어 인큐베이터에 등록되었습니다!**", embeds=[embed])

    import sys
    print("=== Notifier 모듈 점검 ===")
    if not config.DISCORD_WEBHOOK:
        print("  ℹ️ DISCORD_WEBHOOK_URL이 .env에 설정되지 않았습니다. (콘솔 모드로 동작)")
    else:
        print(f"  🔗 DISCORD_WEBHOOK_URL: {config.DISCORD_WEBHOOK[:30]}...")
        if "--test" in sys.argv or len(sys.argv) == 1:
            print("  📨 디스코드 테스트 알림 발송 중...")
            ok = send_discord("🦅 **Argus Pulse** 알림 시스템 연동 테스트 메시지입니다.")
            if ok:
                print("  ✅ 디스코드 웹훅 전송 성공!")
            else:
                print("  ❌ 디스코드 웹훅 전송 실패. URL을 확인하세요.")

    test_news = {"company": "SK하이닉스", "title": "HBM4 조기 양산 체제 돌입", "score": 95, "source": "뉴스"}
    notify_hot_news(test_news, ["T-02"])
    print("✅ Notifier 동작 테스트 완료")
