# Argus Pulse — 모듈별 테스트 케이스 명세서

> **작성일**: 2026-09-03  
> **검증 상태**: 전체 79개 단위 테스트 및 실전 종단간(E2E) 파이프라인 검증 통과  

---

## 1. 테스트 케이스 요약표

| 테스트 ID | 대상 모듈 | 테스트 시나리오 | 입력값 / 조건 | 기대 결과 | 상태 |
|---|---|---|---|---|---|
| **TC-01** | `html_parser.py` | 네이버 블로그 HTML 파싱 | 네이버 블로그 스마트에디터 HTML | 불필요 태그 제거 후 본문 텍스트만 추출 | **PASS** |
| **TC-02** | `html_parser.py` | 범용 웹페이지 파싱 | 한경 기사 HTML (`99.raw/hankyung/`) | 제목, 본문 텍스트 11,000자 이상 정상 추출 | **PASS** |
| **TC-03** | `html_parser.py` | 원본 파일 자동 아카이빙 | `parsed_files` 전달 및 아카이브 플래그 | `99.raw/archive/` 폴더로 파일 안전 이동 | **PASS** |
| **TC-04** | `thesis_loader.py` | 테제 파일 프론트매터 로드 | `thesis/T-01~T-09.md` | id, title, hypothesis, keywords 파싱 완료 | **PASS** |
| **TC-05** | `topic_generator.py`| 테제-뉴스 키워드 매칭 | 엔비디아, TPU, CAPEX 기사 | T-01, T-05, T-06 테제 자동 매칭 | **PASS** |
| **TC-06** | `llm_client.py` | Gemini 503/429 Fallback | Gemini API 429 Quota Exceeded 유발 | 즉시 OpenCode Muse-Spark로 무중단 전환 | **PASS** |
| **TC-07** | `blog_writer.py` | 2-Page 심층 블로그 생성 | 주제 JSON + `--critic` + `--auto` | 서론, 본론, 반론, 표, 데이터박스, 각주 포함 MD 생성 | **PASS** |
| **TC-08** | `critic.py` | 품질 자가 채점 및 보완 | 1차 초안 75점 (출처 부족) | 지적사항 반영 후 2차 87점 획득 및 PASS 승인 | **PASS** |
| **TC-09** | `thread_writer.py` | 13줄 모바일 팩트 스레드 | 주제 JSON + Angle A + compact | 1~13번 번호 매겨진 구체 수치 팩트 스레드 생성 | **PASS** |
| **TC-10** | `obsidian_sync.py` | 실시간 볼트 동기화 | 생성된 Blog / Thread MD 파일 | 실제 iCloud Obsidian 볼트 내 폴더로 즉시 복사 | **PASS** |
| **TC-11** | `hourly_monitor.py`| 매시간 감시 및 80점 필터 | 점수 85점 뉴스 수집 시뮬레이션 | 80점 이상 조건 충족 시 알림 발생 확인 | **PASS** |
| **TC-12** | `daily_digest.py` | 일일 종합 다이제스트 생성 | 하루 동안 누적된 뉴스 목록 | 테제별 카테고리 묶음 브리프 생성 및 저장 | **PASS** |

---

## 2. E2E 실전 검증 결과 기록 (2026-09-03)

### 1) E2E 블로그 생성 검증
* **소스**: `99.raw/hankyung/202605010182i.html` (구글 클라우드 폭증 및 엔비디아 하락 기사)
* **매칭 테제**: `T-06` (TPU 증가와 GPU 수요 둔화)
* **LLM 처리 경로**: Gemini 429 감지 ➔ OpenCode Muse-Spark 1.2 자동 전환
* **Critic 자가 검수**:
  - 1차: 75점 (REVISE - 인용 및 보고서 명시 부족 지적)
  - 2차: 87점 (PASS - 각주 및 출처 보강 완료)
* **최종 산출물**: [`output/blog/2026-09-03-blog-빅테크가-돈을-더-쓴다는데-왜-엔비디아는-급락했을까.md`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/output/blog/2026-09-03-blog-%EB%B9%85%ED%85%8C%ED%81%AC%EA%B0%80-%EB%8F%88%EC%9D%84-%EB%8D%94-%EC%93%B4%EB%8B%A4%EB%8A%94%EB%8D%B0-%EC%99%9C-%EC%97%94%EB%B9%84%EB%94%94%EC%95%84%EB%8A%94-%EA%B8%89%EB%9D%BD%ED%96%88%EC%9D%84%EA%B9%8C.md)
* **동기화**: `agent_vault/Blog/` 동기화 성공.

### 2) E2E 스레드 생성 검증
* **소스**: 동일 기사 (빅테크 CAPEX 대비 수익화 옥석가리기)
* **매칭 테제**: `T-05` (금리와 데이터센터 ROIC 검증)
* **각도**: Angle A (수혜/수치 계산 각도, compact 13줄)
* **최종 산출물**: [`output/thread/2026-09-03-thread-구글의-독주와-메타의-추락-월가가-빚내서-AI-하는-빅테크를-응징하기-시-A.md`](file:///Users/chansoojeon/Library/CloudStorage/Dropbox/03_code/b_0901_Argus_pulse/output/thread/2026-09-03-thread-%EA%B5%AC%EA%B8%80%EC%9D%98-%EB%8F%85%EC%A3%BC%EC%99%80-%EB%A9%94%ED%83%80%EC%9D%98-%EC%B6%94%EB%9D%BD-%EC%9B%94%EA%B0%80%EA%B0%80-%EB%B9%9A%EB%82%B4%EC%84%9C-AI-%ED%95%98%EB%8A%94-%EB%B9%85%ED%85%8C%ED%81%AC%EB%A5%BC-%EC%9D%91%EC%A7%95%ED%95%98%EA%B8%B0-%EC%8B%9C-A.md)
* **동기화**: `agent_vault/Thread/` 동기화 성공.
