# 🚀 옵시디언 상호링크 아키텍처 기반 후속 고도화 작업 제안서

> **작성일**: 2026-09-06  
> **기준 문서**: `2026-09-06-obsidian-bidirectional-linking-architecture-and-guide.md`  
> **시스템**: Argus Pulse / Obsidian Knowledge Graph System  

---

## 1. 추진 배경 및 목표

38개 전체 투자 테제(`T-01` ~ `T-38`), 16개 핵심 기술 토픽(`Topic-*.md`), 15개 기업 허브(`Company-*.md`) 및 Master MOC(`00-Argus-Master-MOC.md`)의 구축으로 지식 그래프의 **골격(Backbone)**이 완성되었습니다.

다음 단계는 이 지식 그래프가 **매일 실행되는 자동 수집·생성 파이프라인과 실시간으로 연동되어 살아 숨 쉬는 인텔리전스 생태계**로 작동하도록 고도화하는 것입니다.

---

## 2. 5대 추가 작업 트랙 (Prioritized Proposals)

```
[Track 1: 생성 파이프라인 자동 링크 주입] ──► 신규 생성물 실시간 지식망 결합
[Track 2: 기존 산출물 위키링크 소급 적용] ──► 과거 28개 레거시 산출물 완전 연결
[Track 3: 4대 섹터별 인터랙티브 Canvas]   ──► 시각적 인과관계 캔버스 구축
[Track 4: 볼트 기존 Companies 완벽 통합]   ──► 사용자 기존 기업 노트와 테제 융합
[Track 5: 그래프 린터 & 무결성 검증기]   ──► 깨진 링크 및 고립 노드 상시 방지
```

---

### 📌 Track 1: AI 생성 파이프라인 상호링크 자동 주입 (최우선 추천 ⭐⭐⭐)

- **대상 파일**: `blog_writer.py`, `daily_digest.py`, `thread_writer.py`, `review_generator.py`
- **목적**: LLM이 새로운 블로그나 다이제스트를 작성할 때, 본문과 하단 레퍼런스에 표준 위키링크(`[[T-XX-파일명|제목]]`, `[[Topic-토픽]]`, `[[Company-기업]]`)를 자동으로 생성하도록 프롬프트 및 후처리 로직 업그레이드.
- **주요 개선 내용**:
  1. `daily_digest.py`: 다이제스트 섹션 헤더를 `### [[T1-01-데이터센터의-변화|T-01 데이터센터의 변화]]`로 출력하여 매일의 다이제스트가 해당 테제 노드에 자동 결합.
  2. `blog_writer.py`: 본문 작성 시 키워드 매칭을 통해 `[[Topic-HBM|HBM]]`, `[[Company-SK하이닉스|SK하이닉스]]`를 인라인 자동 변환하고, 하단에 `### 🔗 연관 지식 네트워크` 섹션을 표준 포맷으로 자동 삽입.
  3. `thread_writer.py` & `review_generator.py`: 상위 테제 및 Master MOC 링크 자동 부착.

---

### 📌 Track 2: 기존 산출물(Legacy Outputs) 위키링크 소급 적용 (Backfill)

- **대상 파일**: `output/blog/` (14개), `output/review/` (5개), `output/digest/` (3개), `output/thread/` (6개)
- **목적**: 이전에 생성된 총 28개 기존 마크다운 산출물 내의 단순 텍스트(`T-01`, `SK하이닉스`, `HBM` 등)를 표준 위키링크 포맷으로 일괄 변환하여 그래프의 연결 단절을 완전히 해소.
- **기대 효과**: 그래프 뷰에서 고립되어 있던 과거 글들이 `T-02`, `Topic-HBM`, `Company-SK하이닉스` 주변으로 즉시 군집화됨.

---

### 📌 Track 3: 4대 섹터별 인터랙티브 옵시디언 캔버스(Canvas) 구축

- **대상 파일**: `argus/01-반도체-메모리.canvas`, `argus/02-인프라-전력.canvas` 등
- **목적**: 복잡한 인과관계를 텍스트뿐만 아니라 옵시디언의 내장 기능인 **Visual Canvas(`.canvas`)**로 시각화하여, 노드 카드 간 화살표를 드래그하고 조망할 수 있는 대화형 분석 맵 제공.
- **제작 대상 캔버스 4종**:
  1. `01-Silicon-Compute.canvas` (반도체 미세화 한계 ➔ HBM4 ASIC ➔ CoWoS 패키징 ➔ 유리기판)
  2. `02-Power-Cooling-Infra.canvas` (GPU 발열 ➔ 액체냉각 ➔ 전력망 쇼티지 ➔ SMR/ESS)
  3. `03-Physical-AI-Robotics.canvas` (공간지능 ➔ NPU 엣지 ➔ E2E 자율주행 ➔ 휴머노이드)
  4. `04-Macro-Valuation-Cloud.canvas` (금리 5% ➔ CAPEX ROI ➔ GPU 금융 ➔ 버블 리스크)

---

### 📌 Track 4: 볼트 기존 `Companies/` 폴더와 Argus 테제 100% 융합

- **대상 위치**: `agent_vault/Companies/KR/`, `agent_vault/Companies/US/`
- **목적**: 사용자가 기존에 보유하고 있던 기업 노트(`Companies/KR/삼성전자/삼성전자.md`, `Companies/US/NVIDIA/NVIDIA.md` 등)의 `## 관련 노트` 섹션에 Argus 테제 링크와 Dataview 블록을 일괄 연결.
- **기대 효과**: 기업 분석 노트를 열었을 때 해당 기업이 어떤 Argus 가설에 영향을 받는지, 최근 어떤 Argus 블로그/리포트에 언급되었는지가 실시간으로 표출됨.

---

### 📌 Track 5: 지식 그래프 린터 & 무결성 검증기 (`scripts/lint_graph.py`)

- **목적**: 볼트 내 모든 마크다운 파일의 위키링크 유효성을 주기적으로 검사하는 자동화 툴.
- **기능**:
  - 존재하지 않는 파일이나 깨진 링크(Dead link / Unresolved link) 자동 탐지
  - 고립 노드(Orphan notes) 탐지 및 연관 MOC/토픽 추천
  - NFC/NFD 유니코드 인코딩 불일치 자동 교정

---

## 3. 추천 실행 로드맵 (Roadmap)

| 단계 | 작업 내용 | 소요 및 우선순위 |
|:---:|:---|:---:|
| **1단계** | **Track 1: AI 생성 파이프라인(blog, digest, review) 자동 위키링크 주입** | 즉시 착수 (High) |
| **2단계** | **Track 2: 기존 28개 산출물 위키링크 일괄 소급 적용(Backfill)** | 즉시 착수 (High) |
| **3단계** | **Track 4: 볼트 내 기존 기업 노트(`Companies/*`)와 테제 자동 매핑** | 권장 (Medium) |
| **4단계** | **Track 3 & 5: 4대 섹터별 Canvas 맵 구축 및 Graph Linter 개발** | 점진적 확장 (Low) |

---

## 4. 의사결정 요청

위 5가지 트랙 중 **어떤 작업을 우선적으로 진행할지** 선택해 주시면 즉시 구현 및 배포를 진행하겠습니다:

1. **[옵션 A - 파이프라인 & 기존 데이터 완성 (Track 1 + 2)]**: 앞으로 생성될 글의 자동 링크 주입과 기존 글 28개의 소급 적용을 먼저 완료하여 완벽한 연결성을 확보.
2. **[옵션 B - 기존 볼트 기업 노트 완전 융합 (Track 4)]**: 사용자의 `Companies/KR`, `Companies/US` 노트를 테제와 즉시 통합.
3. **[옵션 C - 5대 트랙 전체 일괄 진행 (Full Suite)]**: Track 1부터 5까지 종합적으로 순차 진행.
