# Argus Pulse — 시스템 에러 및 배치 장애 분석 보고서

> **문서 번호**: INC-20260904-01  
> **작성 일자**: 2026-09-04  
> **작성자**: Antigravity  
> **관련 모듈**: `topic_generator.py`, `thesis_checker.py`, `hourly_monitor.py`, `crontab.txt`  
> **상태**: 🟢 원인 분석 완료 및 긴급 코드 패치 완료 (해결됨)

---

## 1. 개요 (Executive Summary)

2026년 9월 4일 오전, Argus Pulse 배치 시스템 점검 중 다음과 같은 문제점이 확인되어 원인 분석 및 해결 조치를 완료하였습니다.

1. **[에러 1] 08:00 아침 주제 추천 배치 비정상 종료 (`EOFError`)**: 기획안 생성 및 디스코드 발송 후 사용자 입력 대기 단계에서 크래시 발생 → **코드 수정 완료**
2. **[지연 2] `thesis_checker.py` 실행 시 약 10분 소요 현상**: 29개 전수 가설 순차 점검 및 Gemini Quota 초과로 인한 로컬 모델 Fallback 지연 → **원인 규명 및 최적화 가이드 수립**
3. **[확인 3] 09:00 / 10:00 모니터링 알림 미수신**: 80점 이상 고득점 뉴스 부재로 인한 정상 무음(Silent) 처리 확인

---

## 2. 상세 에러 분석 및 조치 내역

### 🚨 [에러 1] `topic_generator.py`의 Crontab 비대화형 환경 EOFError

#### 1) 발생 현상
* 2026-09-04 08:00 Crontab 스케줄에 의해 `python topic_generator.py --auto`가 실행됨.
* 최근 2일간 뉴스 15건 수집 및 3개 추천 주제(HBM4 커스텀 ASIC, 데이터센터 전력 병목 등) 생성 후 `logs/2026-09-04-topics.json` 저장과 디스코드 알림 발송까지는 성공함.
* 그러나 스크립트 종료 직전 터미널 대화형 입력 대기 코드에서 `EOFError`가 발생하며 비정상 종료됨.

#### 2) 에러 로그 (`logs/cron_topic.log`)
```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
번호 선택 + 포맷 (예: 1b=블로그, 1br=RAG심층블로그, 2t=스레드, 2tr=RAG심층스레드, s=건너뜀)
→ Traceback (most recent call last):
  File "/Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/topic_generator.py", line 354, in <module>
    main()
  File "/Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/topic_generator.py", line 291, in main
    choice = input("→ ").strip().lower()
             ^^^^^^^^^^^
EOFError: EOF when reading a line
```

#### 3) 근본 원인 (Root Cause)
* Crontab 백그라운드 실행 환경은 사용자의 키보드 입력(stdin)이 연결되지 않는 비대화형(Non-interactive) 환경입니다.
* `topic_generator.py`는 기획안 출력 후 Human-in-the-Loop 선택을 위해 `choice = input("→ ")`를 무조건 호출하도록 작성되어 있어, 입력 스트림의 끝(EOF)을 만나 예외가 발생했습니다.

#### 4) 조치 사항 (Patch)
* `sys.stdin.isatty()` 검사를 도입하여 터미널이 직접 연결되지 않은 배치/Crontab 환경에서는 `input()` 대기를 건너뛰고 정상 종료(Exit Code 0)하도록 수정했습니다.
* `input()` 호출부를 `try-except (EOFError, KeyboardInterrupt)`로 감싸 비정상 종료를 원천 방지했습니다.

```python
# topic_generator.py 수정 코드
# ── Human in the Loop (대화형 환경에서만 실행) ─────────────────────────
if not sys.stdin.isatty():
    print("\n✅ [배치 모드] 오늘의 주제 추천이 완료되어 저장 및 알림이 전송되었습니다.")
    return

print()
print("━" * 60)
print("번호 선택 + 포맷 (예: 1b=블로그, 1br=RAG심층블로그, 2t=스레드, 2tr=RAG심층스레드, s=건너뜀)")
try:
    choice = input("→ ").strip().lower()
except (EOFError, KeyboardInterrupt):
    print("\n입력이 취소되었습니다.")
    return
```

---

### ⏳ [지연 2] `thesis_checker.py` 실행 시 10분 소요 원인 분석

#### 1) 발생 현상
* `thesis_checker.py` 실행 시 약 8~10분 이상 프로세스가 종료되지 않아 동결(Freeze/Error)로 오인됨.

#### 2) 원인 분석
1. **가설 수 대폭 증가**: 초기 4~9개에서 29개(전체 38개)로 가설 수가 증가하여 순차 점검 대상이 많아짐.
2. **Gemini Free Tier Quota 초과 (429 RESOURCE_EXHAUSTED)**:
   * Gemini 3.7 Flash 무료 티어 한도(일일 20회)에 도달하여 API 호출이 실패함.
3. **로컬 대체 모델(OpenCode) 자동 전환에 따른 레이턴시**:
   * `llm_client.py`의 Fallback 로직에 따라 `opencode/muse-spark-1.2-contributor-free` CLI가 subprocess로 구동됨.
   * 로컬 CLI 추론은 1건당 약 15~25초 소요되며, **29개 가설 × 약 20초 = 총 580초 (약 9.6분)**가 소요됨.
4. **결론**: 에러가 아닌 **전수 순차 처리 및 로컬 모델 추론 시간에 따른 정상 지연**임.

#### 3) 개선 권장 방안
* **단일 가설 실행**: `python thesis_checker.py --id T-02` (10~15초 완료)
* **스마트 선별 점검**: 배치 실행 시 당일 관련 뉴스가 발생한 가설(2~4건)만 타겟팅하여 점검하도록 코드 개선 권장.
* **Gemini 유료 플랜 적용 시**: 전체 29개 점검도 30초~1분 이내 완료 가능.

---

### 🔍 [확인 3] 09:00 / 10:00 모니터링 알림 미수신 원인

#### 1) 점검 내용
* `logs/cron_monitor.log` 확인 결과:
  * 09:00:01 → 뉴스 100건 수집 완료, 80점 이상 고득점 뉴스 없음
  * 10:00:01 → 신규 뉴스 0건 확인
* 시스템 설계상 80점 이상의 긴급 고득점 뉴스가 없을 때는 사용자에게 불필요한 알림 피로도를 주지 않기 위해 **무음(Silent)으로 정상 완료**되도록 되어 있습니다.

---

## 3. 종합 조치 및 검증 결과

| 점검 항목 | 조치 전 | 조치 후 | 검증 상태 |
|---|---|---|:---:|
| **08:00 주제 추천 배치** | `EOFError` 비정상 종료 | `sys.stdin.isatty()` 감지 후 정상 종료 | 🟢 검증 완료 (`Exit Code 0`) |
| **디스코드 알림 발송** | 크래시 전 발송되었으나 불안정 | 안전하게 발송 후 정상 종료 | 🟢 정상 동작 |
| **`thesis_checker.py` 가이드** | 10분 지연으로 오류 오인 | 단일 가설 옵션 및 동작 원리 문서화 | 🟢 가이드 수립 |

---

> [!NOTE]
> 해당 수정 사항은 현재 코드베이스에 즉시 반영되어 있으며, 내일 08:00 아침 배치부터 오류 없이 안전하게 실행됩니다.
