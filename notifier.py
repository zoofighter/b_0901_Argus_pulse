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


if __name__ == "__main__":
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
