# Argus Pulse — 구현 요약 계획서 (1-Page Summary)

> **문서 버전**: 1.0.0 (Executive Summary)  
> **기준일**: 2026-09-03  

---

## 1. 핵심 아키텍처 요약

```
[원천 데이터]                  [분석 엔진]                  [최종 산출물]
• news.sqlite (매시간 감시)    • 9대 Thesis 필터링          • 2-Page 블로그 (critic 검수)
• 99.raw/ (수동 HTML/TXT)  ──► • 듀얼 LLM 무중단 Fallback  ──► • 13줄 팩트 스레드
• 증권사 리포트/PDF            • Human-in-the-Loop 선택     • 일일 다이제스트
                                                            • 옵시디언(Obsidian) 동기화
```

---

## 2. 1일 운영 사이클 (Standard Daily Routine)

| 시각 | 트리거 모듈 | 동작 내용 | 산출물 / 알림 |
|---|---|---|---|
| **08:00** | `topic_generator.py` | 밤사이 수집된 뉴스와 9대 Thesis 매칭 | 오늘의 콘텐츠 추천 3선 푸시 알림 |
| **09~21시 (매시간)** | `hourly_monitor.py` | 매시간 실시간 뉴스 크롤링 및 스코어링 | 80점 이상 충격 뉴스 감지 시 즉시 알림 |
| **수시 (사용자)** | `argus.py` / `run.sh` | 대화형 메뉴로 블로그 또는 스레드 즉시 생성 | 옵시디언 볼트에 마크다운 파일 자동 생성 |
| **21:00** | `daily_digest.py` | 하루 전체 뉴스를 테제별로 묶어 요약 | `output/digest/` 및 옵시디언 자동 저장 |

---

## 3. 원클릭 명령어 치트시트

```bash
# 1. 통합 대화형 콘솔 실행
./run.sh                  # 또는 python argus.py

# 2. 아침 주제 추천 (뉴스 기반)
./run.sh --topic          # python topic_generator.py

# 3. 수동 원시 자료 분석 및 자동 아카이빙
./run.sh --raw            # python topic_generator.py --raw 99.raw

# 4. 실시간 뉴스 감시 1회 실행
./run.sh --monitor        # python hourly_monitor.py --once

# 5. 일일 다이제스트 생성
./run.sh --digest         # python daily_digest.py

# 6. 옵시디언 전체 동기화
./run.sh --sync           # python obsidian_sync.py

# 7. 백그라운드 스케줄러 구동
./run.sh --schedule       # python scheduler.py
```

---

## 4. 장애 대응 및 품질 보증 핵심 원칙

1. **무중단 듀얼 LLM**: Gemini 장애(503/429) 발생 시 즉시 로컬 무료 OpenCode Muse-Spark로 자동 전환.
2. **품질 검수 위원(Critic)**: 80점 미만 시 발행 거부 및 자동 보완 1회 수행.
3. **데이터 주권**: 상용 클라우드 종속 없이 모든 자산은 로컬 마크다운과 사용자 옵시디언에 영구 보존.
