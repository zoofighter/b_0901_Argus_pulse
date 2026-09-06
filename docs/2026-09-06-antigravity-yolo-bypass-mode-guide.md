# Antigravity IDE & CLI — YOLO / Bypass (Auto-Approve) 자율 실행 모드 가이드

> **작성일자**: 2026-09-06  
> **문서 유형**: 시스템 환경설정 및 에이전트 자율성 가이드  
> **대상 플랫폼**: Google Antigravity IDE (VS Code 기반) & Antigravity CLI (`agy`)  

---

## 1. 개요 (Overview)

Antigravity 에이전트는 기본적으로 안전을 위해 터미널 명령어 실행, 파일 덮어쓰기, 계획 승인 등 중요한 단계마다 사용자에게 **확인(Approve / Proceed)**을 요청합니다.

그러나 빠른 개발과 논스톱 자율 실행을 위해 매번 발생하는 승인 팝업이나 대기 상태를 건너뛰고 전자동으로 작업을 완수하도록 하는 **'YOLO / Bypass (Auto-Approve)' 모드**를 지원합니다.

---

## 2. Antigravity IDE (VS Code 기반) 설정 가이드

IDE 환경에서는 환경설정(Settings)을 통해 에이전트의 터미널 및 도구 실행 권한 정책을 영구적 혹은 프로젝트 단위로 변경할 수 있습니다.

### ① 터미널 명령어 자동 실행 (Always Proceed)
1. **설정 창 열기**: `Cmd + ,` (macOS) 또는 `Ctrl + ,` (Windows/Linux)
2. **검색창 입력**: `Agent Terminal` 또는 `Auto Execution`
3. **핵심 설정 변경**:
   * **`Agent > Terminal Command Auto Execution`**
     * 기본값: `Ask` (명령어마다 실행 여부 대화상자 표시)
     * **변경값: `Always Proceed` (또는 `Allow`)**  
       ➔ 에이전트가 제안하는 모든 쉘/터미널 명령어가 확인 대기 없이 즉시 백그라운드/포그라운드에서 실행됩니다.

### ② 권한 허용 목록 (Permission Allow List)
* **`Agent > Permissions: Allow List`**:
  * 신뢰할 수 있는 특정 CLI 도구나 명령어 패턴(예: `git *`, `npm test`, `python *`)을 사전에 등록하여 화이트리스트 방식으로 자동 승인할 수 있습니다.
  * 완전한 바이패스를 위해 와일드카드(`*`)를 등록하는 방식도 지원됩니다.

### ③ 계획 수립(Planning Mode) 승인 건너뛰기
복잡한 작업 시 에이전트가 `implementation_plan.md`를 생성하고 `Proceed` 버튼 클릭을 기다리는 단계를 생략하려면 다음 방식을 활용합니다.

1. **프롬프트 지침 부여**:
   * 프롬프트 시작 또는 끝에 **"계획 승인(Plan) 없이 바로 실행해줘"** 또는 **"Bypass plan, execute directly"** 명시
2. **슬래시 명령어 `/goal` 활용**:
   * 채팅창에 `/goal [요구사항]` 입력 시, 에이전트가 중간 확인을 최소화하고 목표 달성까지 딥 다이브하여 자율 질주합니다.

---

## 3. Antigravity CLI (`agy`) 실행 플래그

터미널 기반 CLI(`agy`)에서는 실행 시 전용 플래그를 통해 즉각적인 YOLO 모드 전환이 가능합니다.

```bash
# 1. 완전한 YOLO 모드 (모든 권한 요청 100% 자동 승인)
# 터미널 명령어, 파일 쓰기, 브라우저 조작 등 일체의 확인 없이 자율 실행
agy --dangerously-skip-permissions

# 2. 파일 수정 승인 생략 모드 (Accept-Edits)
# 코드 및 문서 수정 승인 팝업을 건너뛰고 연속 작업 수행
agy --mode=accept-edits
```

---

## 4. ⚠️ 보안 및 안전 주의사항 (Safety & Blast Radius)

> [!CAUTION]
> **YOLO / Bypass 모드 활성화 시 필수 확인 사항**
> 
> 1. **파괴적 명령어 즉시 실행 위험**:  
>    에이전트의 판단 착오나 예외 상황 시 `rm -rf`, 잘못된 의존성 삭제, Git 강제 리셋(`git reset --hard`) 등이 사용자 확인 없이 바로 수행될 수 있습니다.
> 2. **작업 환경 격리 권장**:  
>    * 완전 바이패스 모드는 반드시 **Git으로 변경 사항이 커밋되어 언제든 롤백 가능한 상태**이거나,
>    * **Docker 컨테이너, DevContainer, 샌드박스 가상환경** 내부에서 활성화하는 것을 강력히 권장합니다.
> 3. **네트워크 및 민감 정보 보호**:  
>    외부 API 호출이나 비가역적 클라우드 리소스 변경이 포함된 프로젝트에서는 `Ask` 정책을 유지하는 것이 안전합니다.
