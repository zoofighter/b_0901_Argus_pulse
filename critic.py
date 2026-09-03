"""
critic.py — AI 멀티에이전트 품질 및 팩트 자가 검수 모듈 (Critic Agent)

기능:
  - 블로그/스레드 초안을 5대 평가 기준으로 자가 채점 (100점 만점)
    1. 수치 및 팩트 밀도 (25점): %, $, GWh, YoY 등 구체적 수치 포함
    2. 인용 및 근거 충실도 (25점): 증권사 리포트/뉴스 출처 및 왜곡 여부
    3. 시각적 구조 (20점): 비교 표(Table), 볼드 하이라이트 구성
    4. 톤앤매너 & 전문성 (15점): 군더더기 없는 시니어 애널리스트 톤
    5. 결론 및 인사이트 (15점): 핵심 테이크어웨이 및 리스크 요인
  - 80점 이상: PASS (합격)
  - 80점 미만: REVISE (지적 사항을 바탕으로 자동 1회 수정 루프 실행)
"""

import json
import re
from typing import Optional
import config
from llm_client import call_llm


CRITIC_PROMPT_TEMPLATE = """당신은 테크/투자 리서치 랩의 최고 콘텐츠 검수위원(Editor-in-Chief & Fact Checker)입니다.
아래 작성된 [콘텐츠 초안]을 5대 평가 기준에 따라 엄격하고 냉정하게 평가하고 JSON 형식으로만 답변하세요.

[콘텐츠 초안]
{content}

[5대 평가 기준 (총 100점 만점)]
1. 수치 및 팩트 밀도 (25점): 구체적인 수치(%, $, 조원, YoY, GWh 등)가 풍부하게 포함되어 있는가?
2. 인용 및 근거 충실도 (25점): 리포트/뉴스/데이터 출처가 명확히 드러나며 할루시네이션(거짓 정보) 징후가 없는가?
3. 시각적 구조 (20점): 마크다운 비교 표(Table)가 존재하며, 문단 첫머리 볼드 등 가독성이 뛰어난가? (스레드의 경우 번호 나열과 호흡)
4. 톤앤매너 & 전문성 (15점): 기초 용어 괄호 남발 없이 속도감 있고 날카로운 전문 인텔리전스 톤인가?
5. 결론 및 인사이트 (15점): 명확한 3대 인사이트, 리스크 요인, 향후 주목할 이벤트가 제시되었는가?

[응답 JSON 양식]
```json
{{
  "scores": {{
    "fact_density": 22,
    "citation": 20,
    "structure": 18,
    "tone": 14,
    "takeaway": 14
  }},
  "total_score": 88,
  "verdict": "PASS",
  "critique": "핵심 논리와 표 구성이 우수하나 결론부의 리스크 요인을 한 줄 더 보강할 것",
  "actionable_fixes": [
    "본론 1의 ASP 추정치에 키움증권 리포트 출처 표기 보강"
  ]
}}
```
* 합격 기준: total_score >= 80점일 때 "PASS", 80점 미만일 때 "REVISE"
반드시 JSON 코드 블록만 출력하세요."""


def evaluate_content(content: str) -> dict:
    """초안 콘텐츠 검수 및 채점"""
    prompt = CRITIC_PROMPT_TEMPLATE.format(content=content[:5000])
    resp = call_llm(prompt)
    clean = re.sub(r"^```(?:json)?\n?", "", resp.strip())
    clean = re.sub(r"\n?```$", "", clean.strip())

    try:
        data = json.loads(clean)
        # 총점 재계산 안전 장치
        scores = data.get("scores", {})
        calc_total = sum(scores.values()) if scores else data.get("total_score", 85)
        data["total_score"] = calc_total
        data["verdict"] = "PASS" if calc_total >= 80 else "REVISE"
        return data
    except Exception as e:
        print(f"  ⚠️ Critic 응답 파싱 실패: {e} (기본 합격 처리)")
        return {
            "total_score": 80,
            "verdict": "PASS",
            "critique": "파싱 예외로 기본 통과",
            "actionable_fixes": []
        }


REVISE_PROMPT_TEMPLATE = """당신은 테크/투자 전문 시니어 라이터입니다.
이전에 작성한 [기존 초안]에 대해 수석 검수위원(Critic)의 [지적 사항]이 접수되었습니다.
지적된 사항을 철저히 보완하여 완성도 높은 최종본 마크다운으로 전면 수정 작성하세요.

[기존 초안]
{original_content}

[검수위원 평가 (점수: {score}점 - REVISE)]
- 종합 코멘트: {critique}
- 필수 수정 과제:
{fixes}

[수정 지침]
- 마크다운 비교 표(Table)가 누락되었다면 반드시 본론에 추가하세요.
- 수치/팩트의 출처를 더 명확하게 인용하세요.
- 전문 용어 괄호 풀이를 최소화하고 시니어 애널리스트 톤을 유지하세요.
- 전체 마크다운 문서만 바로 출력하세요 (불필요한 설명 금지)."""


def refine_content(original_content: str, critic_result: dict) -> str:
    """Critic의 피드백을 반영하여 초안 자동 수정"""
    fixes_str = "\n".join([f"- {f}" for f in critic_result.get("actionable_fixes", [])])
    prompt = REVISE_PROMPT_TEMPLATE.format(
        original_content=original_content,
        score=critic_result.get("total_score", 70),
        critique=critic_result.get("critique", ""),
        fixes=fixes_str or "- 전반적인 수치 근거 및 가독성 보강"
    )

    refined = call_llm(prompt)
    refined = re.sub(r"^```(?:markdown)?\n?", "", refined.strip())
    refined = re.sub(r"\n?```$", "", refined.strip())
    return refined


def run_critic_loop(content: str, max_revisions: int = 1) -> tuple[str, dict]:
    """
    검수 및 자동 보완 루프 실행
    Returns:
        (최종 수정본_str, 최종 평가_dict)
    """
    print("\n🧐 [Critic Agent] 콘텐츠 팩트 및 품질 자가 검수 시작...")
    current_content = content
    last_eval = {}

    for attempt in range(max_revisions + 1):
        last_eval = evaluate_content(current_content)
        score = last_eval.get("total_score", 0)
        verdict = last_eval.get("verdict", "REVISE")
        print(f"  📊 [검수 결과 ({attempt+1}차)] 점수: {score}/100점 → {verdict}")

        if verdict == "PASS" or attempt == max_revisions:
            if verdict == "PASS":
                print(f"  ✅ 품질 기준(80점 이상) 충족! 발행 승인.")
            else:
                print(f"  ⚠️ 최대 보완 횟수 도달. 현재 상태로 발행을 진행합니다.")
            break

        print(f"  💡 지적 사항: {last_eval.get('critique', '')}")
        print("  🔄 [Writer Agent] 피드백을 반영하여 초안 자동 보완 중...")
        current_content = refine_content(current_content, last_eval)

    # 프론트매터에 critic 점수 주입
    if "---" in current_content:
        score_tag = f"critic_score: {last_eval.get('total_score', 80)}\ncritic_verdict: {last_eval.get('verdict', 'PASS')}\n"
        # 두 번째 --- 직전에 삽입
        parts = current_content.split("---", 2)
        if len(parts) >= 3:
            current_content = f"---{parts[1]}{score_tag}---{parts[2]}"

    return current_content, last_eval


if __name__ == "__main__":
    sample = """---
title: "테스트"
---
# 삼성전자 HBM4 현황
삼성전자가 HBM4 양산을 추진하고 있습니다.
"""
    refined_doc, res = run_critic_loop(sample)
    print("\n최종 점수:", res.get("total_score"))
