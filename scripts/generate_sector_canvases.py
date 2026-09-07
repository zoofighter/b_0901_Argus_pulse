"""
scripts/generate_sector_canvases.py — 젠슨 황 5단 케이크 + 거시 환경 6대 섹터 인터랙티브 옵시디언 캔버스(.canvas) 생성기
"""

import json
import shutil
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))
import config

THESIS_DIR = ROOT_DIR / "thesis"

# 볼트 내부 기준 상대 경로
def p_thesis(name): return f"argus/Theses/{name}"
def p_topic(name):  return f"argus/Topics/{name}"
def p_comp(name):   return f"argus/Companies/{name}"


def create_canvas_01():
    """1. T1: 에너지 & 전력 & 냉각 인프라 캔버스 (젠슨 황 1단)"""
    nodes = [
        {"id": "h1", "x": -400, "y": -300, "width": 1200, "height": 100, "type": "text", "text": "# ⚡ [Sector 1] AI 데이터센터 & 전력·냉각 인프라 맵 (젠슨 황 1단)\n> 전력 밀도 폭증 ➔ 수랭식 냉각 전환 ➔ 초고압 변압기 쇼티지 ➔ 무탄소 SMR & 대용량 ESS"},
        
        {"id": "top_liquid", "x": -350, "y": -100, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-액체냉각.md")},
        {"id": "top_grid", "x": 50, "y": -100, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-전력그리드.md")},
        {"id": "top_smr", "x": 450, "y": -100, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-SMR.md")},
        
        {"id": "t1_01", "x": -350, "y": 200, "width": 320, "height": 240, "type": "file", "file": p_thesis("T1-01-데이터센터의-변화.md")},
        {"id": "t1_02", "x": 50, "y": 200, "width": 320, "height": 240, "type": "file", "file": p_thesis("T1-02-데이터센터-액체냉각의-표준화.md")},
        {"id": "t1_05", "x": 450, "y": 200, "width": 320, "height": 240, "type": "file", "file": p_thesis("T1-05-변압기-초고압-그리드-쇼티지-장기화.md")},
        
        {"id": "t1_04", "x": -350, "y": 500, "width": 320, "height": 240, "type": "file", "file": p_thesis("T1-04-AI-전력망용-대용량-ESS와-LFP-공급망.md")},
        {"id": "t1_07", "x": 50, "y": 500, "width": 320, "height": 240, "type": "file", "file": p_thesis("T1-07-800V-48V-HVDC-전력-아키텍처-혁신.md")},
        {"id": "top_ess", "x": 450, "y": 500, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-ESS.md")},
        
        {"id": "c_vertiv", "x": -350, "y": 820, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-Vertiv.md")},
        {"id": "c_hd", "x": -50, "y": 820, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-HD현대일렉트릭.md")},
        {"id": "c_ls", "x": 250, "y": 820, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-LS-ELECTRIC.md")},
        {"id": "c_ge", "x": 550, "y": 820, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-GE-Vernova.md")},
    ]
    
    edges = [
        {"id": "e1_1", "fromNode": "top_liquid", "fromSide": "right", "toNode": "top_grid", "toSide": "left", "label": "냉각 전력 소모"},
        {"id": "e1_2", "fromNode": "top_grid", "fromSide": "right", "toNode": "top_smr", "toSide": "left", "label": "기저부하 확보"},
        {"id": "e1_3", "fromNode": "top_liquid", "fromSide": "bottom", "toNode": "t1_02", "toSide": "top", "label": "DLC 표준화"},
        {"id": "e1_4", "fromNode": "top_grid", "fromSide": "bottom", "toNode": "t1_05", "toSide": "top", "label": "리드타임 4년+"},
        {"id": "e1_5", "fromNode": "t1_02", "fromSide": "bottom", "toNode": "c_vertiv", "toSide": "top", "label": "CDU 독점 공급"},
        {"id": "e1_6", "fromNode": "t1_05", "fromSide": "bottom", "toNode": "c_hd", "toSide": "top", "label": "초고압 변압기 수혜"},
        {"id": "e1_7", "fromNode": "t1_05", "fromSide": "bottom", "toNode": "c_ls", "toSide": "top", "label": "배전/스위치기어"},
    ]
    return {"nodes": nodes, "edges": edges}


def create_canvas_02():
    """2. T2: AI 컴퓨트, 메모리 & 선단 반도체 캔버스 (젠슨 황 2단)"""
    nodes = [
        {"id": "h2", "x": -400, "y": -300, "width": 1200, "height": 100, "type": "text", "text": "# 💾 [Sector 2] AI 컴퓨트 · 메모리 · 선단 반도체 밸류체인 맵 (젠슨 황 2단)\n> HBM4 커스텀화 ➔ 첨단 패키징(CoWoS/유리기판) ➔ 2nm GAA ➔ 빅테크 커스텀 ASIC/TPU 생태계"},
        
        {"id": "top_hbm", "x": -350, "y": -100, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-HBM.md")},
        {"id": "top_cowos", "x": 50, "y": -100, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-CoWoS.md")},
        {"id": "top_glass", "x": 450, "y": -100, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-유리기판.md")},
        
        {"id": "top_asic", "x": -350, "y": 200, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-ASIC.md")},
        {"id": "top_gaa", "x": 50, "y": 200, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-2nm-GAA.md")},
        {"id": "top_cxl", "x": 450, "y": 200, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-CXL.md")},
        
        {"id": "t2_01", "x": -350, "y": 500, "width": 320, "height": 240, "type": "file", "file": p_thesis("T2-01-메모리-산업의-변화.md")},
        {"id": "t2_02", "x": 50, "y": 500, "width": 320, "height": 240, "type": "file", "file": p_thesis("T2-02-첨단-패키징과-CoWoS의-병목.md")},
        {"id": "t2_07", "x": 450, "y": 500, "width": 320, "height": 240, "type": "file", "file": p_thesis("T2-07-AI-추론-시장-폭발과-LPU-ASIC-분화.md")},
        
        {"id": "t2_08", "x": -350, "y": 800, "width": 320, "height": 240, "type": "file", "file": p_thesis("T2-08-빅테크-커스텀-ASIC-증가와-DSP-생태계.md")},
        {"id": "t2_11", "x": 50, "y": 800, "width": 320, "height": 240, "type": "file", "file": p_thesis("T2-11-TPU-증가와-GPU-수요-둔화.md")},
        {"id": "t2_03", "x": 450, "y": 800, "width": 320, "height": 240, "type": "file", "file": p_thesis("T2-03-유리기판의-차세대-패키징-침투.md")},
        
        {"id": "c_hynix", "x": -350, "y": 1100, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-SK하이닉스.md")},
        {"id": "c_samsung", "x": -50, "y": 1100, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-삼성전자.md")},
        {"id": "c_tsmc", "x": 250, "y": 1100, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-TSMC.md")},
        {"id": "c_nvda", "x": 550, "y": 1100, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-NVIDIA.md")},
    ]
    
    edges = [
        {"id": "e2_1", "fromNode": "top_hbm", "fromSide": "right", "toNode": "top_cowos", "toSide": "left", "label": "2.5D 통합"},
        {"id": "e2_2", "fromNode": "top_cowos", "fromSide": "right", "toNode": "top_glass", "toSide": "left", "label": "대면적 기판 혁신"},
        {"id": "e2_3", "fromNode": "top_hbm", "fromSide": "bottom", "toNode": "t2_01", "toSide": "top", "label": "HBM4 커스텀화"},
        {"id": "e2_4", "fromNode": "top_cowos", "fromSide": "bottom", "toNode": "t2_02", "toSide": "top", "label": "패키징 병목"},
        {"id": "e2_5", "fromNode": "top_asic", "fromSide": "bottom", "toNode": "t2_08", "toSide": "top", "label": "DSP 생태계"},
        {"id": "e2_6", "fromNode": "t2_01", "fromSide": "bottom", "toNode": "c_hynix", "toSide": "top", "label": "HBM 선두"},
        {"id": "e2_7", "fromNode": "t2_01", "fromSide": "bottom", "toNode": "c_samsung", "toSide": "top", "label": "HBM3E/4 수주전"},
        {"id": "e2_8", "fromNode": "t2_02", "fromSide": "bottom", "toNode": "c_tsmc", "toSide": "top", "label": "CoWoS 독점"},
        {"id": "e2_9", "fromNode": "t2_11", "fromSide": "bottom", "toNode": "c_nvda", "toSide": "top", "label": "GPU 독점 견제/대체"},
    ]
    return {"nodes": nodes, "edges": edges}


def create_canvas_03():
    """3. T3: 초고속 네트워킹 & 시스템 플랫폼 캔버스 (젠슨 황 3단)"""
    nodes = [
        {"id": "h3", "x": -450, "y": -350, "width": 2200, "height": 100, "type": "text", "text": "# 🌐 [Sector 3] 초고속 네트워킹 & 분산 시스템 플랫폼 맵 (젠슨 황 3단)\n> 800G/1.6T 광트랜시버 & AEC ➔ NVLink 랙스케일 패브릭 ➔ PCIe Gen6/7 리타이머 ➔ CPO 실리콘 포토닉스 ➔ UEC vs IB ➔ 장거리 DCI"},
        
        {"id": "top_cpo", "x": -450, "y": -180, "width": 320, "height": 200, "type": "file", "file": p_topic("Topic-실리콘포토닉스.md")},
        {"id": "top_net", "x": -50, "y": -180, "width": 320, "height": 200, "type": "file", "file": p_topic("Topic-초고속네트워킹.md")},
        
        {"id": "t3_04", "x": -450, "y": 80, "width": 320, "height": 240, "type": "file", "file": p_thesis("T3-04-800G·1.6T-광트랜시버와-AEC·LPO-초고속-인터커넥트-혁신.md")},
        {"id": "t3_10", "x": -50, "y": 80, "width": 320, "height": 240, "type": "file", "file": p_thesis("T3-10-NVLink-Switch-랙스케일-패브릭과-대규모-구리-백플레인.md")},
        {"id": "t3_09", "x": 350, "y": 80, "width": 320, "height": 240, "type": "file", "file": p_thesis("T3-09-PCIe-Gen6·Gen7-전환과-초고속-신호-리타이머-병목.md")},
        {"id": "t3_02", "x": 750, "y": 80, "width": 320, "height": 240, "type": "file", "file": p_thesis("T3-02-초고속-AI-네트워킹-UEC-vs-인피니밴드.md")},
        {"id": "t3_01", "x": 1150, "y": 80, "width": 320, "height": 240, "type": "file", "file": p_thesis("T3-01-실리콘-포토닉스와-CPO의-상용화.md")},
        
        {"id": "t3_06", "x": -450, "y": 380, "width": 320, "height": 240, "type": "file", "file": p_thesis("T3-06-초고다층-기판-MLB와-초저손실-CCL-병목.md")},
        {"id": "t3_07", "x": -50, "y": 380, "width": 320, "height": 240, "type": "file", "file": p_thesis("T3-07-데이터센터-간-초장거리-인터커넥트-DCI.md")},
        {"id": "t3_08", "x": 350, "y": 380, "width": 320, "height": 240, "type": "file", "file": p_thesis("T3-08-AI-클러스터-OS와-MFU-가동률-최적화-SW.md")},
        {"id": "t3_03", "x": 750, "y": 380, "width": 320, "height": 240, "type": "file", "file": p_thesis("T3-03-전력-포화와-분산형-AI-데이터센터-코로케이션.md")},
        
        {"id": "c_innolight", "x": -450, "y": 680, "width": 240, "height": 160, "type": "file", "file": p_comp("Company-Innolight.md")},
        {"id": "c_coherent", "x": -180, "y": 680, "width": 240, "height": 160, "type": "file", "file": p_comp("Company-Coherent.md")},
        {"id": "c_lumentum", "x": 90, "y": 680, "width": 240, "height": 160, "type": "file", "file": p_comp("Company-Lumentum.md")},
        {"id": "c_credo", "x": 360, "y": 680, "width": 240, "height": 160, "type": "file", "file": p_comp("Company-Credo.md")},
        {"id": "c_amphenol", "x": 630, "y": 680, "width": 240, "height": 160, "type": "file", "file": p_comp("Company-Amphenol.md")},
        {"id": "c_astera", "x": 900, "y": 680, "width": 240, "height": 160, "type": "file", "file": p_comp("Company-Astera Labs.md")},
        {"id": "c_broadcom", "x": 1170, "y": 680, "width": 240, "height": 160, "type": "file", "file": p_comp("Company-Broadcom.md")},
        {"id": "c_arista", "x": 1440, "y": 680, "width": 240, "height": 160, "type": "file", "file": p_comp("Company-Arista.md")},
    ]
    
    edges = [
        {"id": "e3_1", "fromNode": "top_cpo", "fromSide": "right", "toNode": "top_net", "toSide": "left", "label": "광인터커넥트 전환"},
        {"id": "e3_2", "fromNode": "top_net", "fromSide": "bottom", "toNode": "t3_04", "toSide": "top", "label": "1.6T 광모듈 전환"},
        {"id": "e3_3", "fromNode": "t3_04", "fromSide": "bottom", "toNode": "c_innolight", "toSide": "top", "label": "광트랜시버 1위"},
        {"id": "e3_4", "fromNode": "t3_04", "fromSide": "bottom", "toNode": "c_lumentum", "toSide": "top", "label": "200G EML 레이저"},
        {"id": "e3_5", "fromNode": "t3_10", "fromSide": "bottom", "toNode": "c_amphenol", "toSide": "top", "label": "구리 백플레인"},
        {"id": "e3_6", "fromNode": "t3_09", "fromSide": "bottom", "toNode": "c_astera", "toSide": "top", "label": "리타이머 독점"},
        {"id": "e3_7", "fromNode": "t3_01", "fromSide": "bottom", "toNode": "c_broadcom", "toSide": "top", "label": "CPO 스위치 ASIC"},
        {"id": "e3_8", "fromNode": "t3_02", "fromSide": "bottom", "toNode": "c_arista", "toSide": "top", "label": "UEC 이더넷 연합"},
    ]
    return {"nodes": nodes, "edges": edges}


def create_canvas_04():
    """4. T4: 파운데이션 모델 & 엔터프라이즈 SW 캔버스 (젠슨 황 4단)"""
    nodes = [
        {"id": "h4", "x": -450, "y": -350, "width": 2200, "height": 100, "type": "text", "text": "# 💻 [Sector 4] 파운데이션 모델 & 엔터프라이즈 SW 맵 (젠슨 황 4단)\n> GPT-6 아스트라 AGI ➔ 앤트로픽 해석가능성/신뢰 AI ➔ o1/o3 추론 ➔ DeepSeek/Qwen 가격 파괴 ➔ Computer Use ➔ xAI 그록 ➔ 사설 AI & SaaS 과점화"},
        
        {"id": "top_frontier", "x": -450, "y": -180, "width": 320, "height": 200, "type": "file", "file": p_topic("Topic-프론티어모델.md")},
        {"id": "top_agent", "x": -50, "y": -180, "width": 320, "height": 200, "type": "file", "file": p_topic("Topic-AI에이전트.md")},
        {"id": "top_ondevice", "x": 350, "y": -180, "width": 320, "height": 200, "type": "file", "file": p_topic("Topic-온디바이스AI.md")},
        
        {"id": "t4_06", "x": -450, "y": 80, "width": 320, "height": 240, "type": "file", "file": p_thesis("T4-06-GPT-6-아스트라와-자율형-AGI-엔지니어링-에이전트.md")},
        {"id": "t4_09", "x": -100, "y": 80, "width": 320, "height": 240, "type": "file", "file": p_thesis("T4-09-앤트로픽-클로드의-해석가능성-기술과-엔터프라이즈-AI-시장-독점.md")},
        {"id": "t4_03", "x": 250, "y": 80, "width": 320, "height": 240, "type": "file", "file": p_thesis("T4-03-추론-시간-연산과-시스템2-추론-모델의-부상.md")},
        {"id": "t4_08", "x": 600, "y": 80, "width": 320, "height": 240, "type": "file", "file": p_thesis("T4-08-중국-AI-모델-급부상과-오픈AI·앤트로픽-과점-위협.md")},
        {"id": "t4_04", "x": 950, "y": 80, "width": 320, "height": 240, "type": "file", "file": p_thesis("T4-04-자율형-에이전트와-컴퓨터-제어-엔터프라이즈-침투.md")},
        {"id": "t4_07", "x": 1300, "y": 80, "width": 320, "height": 240, "type": "file", "file": p_thesis("T4-07-xAI-그록과-실시간-데이터-파이어호스-인텔리전스.md")},
        
        {"id": "t4_05", "x": -450, "y": 380, "width": 320, "height": 240, "type": "file", "file": p_thesis("T4-05-프론티어-LLM-멀티모달-네이티브화와-실시간-옴니-인텔리전스.md")},
        {"id": "t4_01", "x": -100, "y": 380, "width": 320, "height": 240, "type": "file", "file": p_thesis("T4-01-오픈소스-모델-고도화와-온프레미스-사설-AI.md")},
        {"id": "t4_02", "x": 250, "y": 380, "width": 320, "height": 240, "type": "file", "file": p_thesis("T4-02-AI-소프트웨어-레이어의-과점화.md")},
        
        {"id": "c_openai", "x": -450, "y": 680, "width": 240, "height": 160, "type": "file", "file": p_comp("Company-OpenAI.md")},
        {"id": "c_anthropic", "x": -180, "y": 680, "width": 240, "height": 160, "type": "file", "file": p_comp("Company-Anthropic.md")},
        {"id": "c_deepseek", "x": 90, "y": 680, "width": 240, "height": 160, "type": "file", "file": p_comp("Company-DeepSeek.md")},
        {"id": "c_alibaba", "x": 360, "y": 680, "width": 240, "height": 160, "type": "file", "file": p_comp("Company-Alibaba.md")},
        {"id": "c_xai", "x": 630, "y": 680, "width": 240, "height": 160, "type": "file", "file": p_comp("Company-xAI.md")},
        {"id": "c_msft", "x": 900, "y": 680, "width": 240, "height": 160, "type": "file", "file": p_comp("Company-Microsoft.md")},
        {"id": "c_meta", "x": 1170, "y": 680, "width": 240, "height": 160, "type": "file", "file": p_comp("Company-Meta.md")},
    ]
    
    edges = [
        {"id": "e4_1", "fromNode": "top_frontier", "fromSide": "bottom", "toNode": "t4_06", "toSide": "top", "label": "GPT-6 Astra"},
        {"id": "e4_2", "fromNode": "t4_03", "fromSide": "left", "toNode": "t4_06", "toSide": "right", "label": "시스템 2 추론 결합"},
        {"id": "e4_3", "fromNode": "top_agent", "fromSide": "bottom", "toNode": "t4_04", "toSide": "top", "label": "Computer Use"},
        {"id": "e4_4", "fromNode": "t4_06", "fromSide": "bottom", "toNode": "c_openai", "toSide": "top", "label": "AGI 엔지니어링 리더"},
        {"id": "e4_5", "fromNode": "t4_09", "fromSide": "bottom", "toNode": "c_anthropic", "toSide": "top", "label": "해석가능성 & Claude 3.7"},
        {"id": "e4_6", "fromNode": "t4_09", "fromSide": "right", "toNode": "t4_04", "toSide": "left", "label": "Computer Use 워크플로우"},
        {"id": "e4_7", "fromNode": "top_frontier", "fromSide": "right", "toNode": "t4_07", "toSide": "top", "label": "Grok 3.5 / 4"},
        {"id": "e4_8", "fromNode": "t4_07", "fromSide": "bottom", "toNode": "c_xai", "toSide": "top", "label": "Colossus 200k 클러스터"},
        {"id": "e4_9", "fromNode": "t4_02", "fromSide": "bottom", "toNode": "c_msft", "toSide": "top", "label": "Copilot Studio"},
        {"id": "e4_10", "fromNode": "t4_01", "fromSide": "bottom", "toNode": "c_meta", "toSide": "top", "label": "Llama 3/4 사설화"},
        {"id": "e4_11", "fromNode": "t4_08", "fromSide": "bottom", "toNode": "c_deepseek", "toSide": "top", "label": "MLA/MoE 극저가 API"},
        {"id": "e4_12", "fromNode": "t4_08", "fromSide": "bottom", "toNode": "c_alibaba", "toSide": "top", "label": "Qwen 2.5 오픈소스"},
        {"id": "e4_13", "fromNode": "t4_08", "fromSide": "left", "toNode": "t4_09", "toSide": "right", "label": "가격 공세 vs 신뢰/안전 수성"},
    ]
    return {"nodes": nodes, "edges": edges}


def create_canvas_05():
    """5. T5: 피지컬 AI & 로보틱스 캔버스 (젠슨 황 5단)"""
    nodes = [
        {"id": "h5", "x": -400, "y": -300, "width": 1200, "height": 100, "type": "text", "text": "# 🤖 [Sector 5] 피지컬 AI · 자율주행 · 로보틱스 맵 (젠슨 황 5단)\n> 공간지능 기반 VLA 파운데이션 모델 ➔ E2E 자율주행 & 로보택시 ➔ 휴머노이드 액추에이터 ➔ 온디바이스 AI"},
        
        {"id": "top_physical", "x": -350, "y": -100, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-피지컬AI.md")},
        {"id": "top_fsd", "x": 50, "y": -100, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-자율주행.md")},
        {"id": "top_ondevice", "x": 450, "y": -100, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-온디바이스AI.md")},
        
        {"id": "t5_06", "x": -350, "y": 200, "width": 320, "height": 240, "type": "file", "file": p_thesis("T5-06-휴머노이드-로봇과-액추에이터-공급망.md")},
        {"id": "t5_05", "x": 50, "y": 200, "width": 320, "height": 240, "type": "file", "file": p_thesis("T5-05-End-to-End-AI-자율주행과-로보택시.md")},
        {"id": "t5_07", "x": 450, "y": 200, "width": 320, "height": 240, "type": "file", "file": p_thesis("T5-07-피지컬-AI와-공간지능-반도체.md")},
        
        {"id": "c_tesla", "x": -200, "y": 550, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-Tesla.md")},
        {"id": "c_apple", "x": 100, "y": 550, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-Apple.md")},
        {"id": "c_qualcomm", "x": 400, "y": 550, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-Qualcomm.md")},
    ]
    
    edges = [
        {"id": "e5_1", "fromNode": "top_physical", "fromSide": "right", "toNode": "top_fsd", "toSide": "left", "label": "공간지능 이식"},
        {"id": "e5_2", "fromNode": "top_fsd", "fromSide": "right", "toNode": "top_ondevice", "toSide": "left", "label": "엣지 NPU 처리"},
        {"id": "e5_3", "fromNode": "top_physical", "fromSide": "bottom", "toNode": "t5_06", "toSide": "top", "label": "하드웨어 구동부"},
        {"id": "e5_4", "fromNode": "top_fsd", "fromSide": "bottom", "toNode": "t5_05", "toSide": "top", "label": "신경망 운전"},
        {"id": "e5_5", "fromNode": "t5_05", "fromSide": "bottom", "toNode": "c_tesla", "toSide": "top", "label": "FSD V12 / Cybercab"},
        {"id": "e5_6", "fromNode": "top_ondevice", "fromSide": "bottom", "toNode": "c_apple", "toSide": "top", "label": "Apple Intelligence"},
    ]
    return {"nodes": nodes, "edges": edges}


def create_canvas_06():
    """6. T6: 매크로 자본시장, 금리 & 지정학 안보 캔버스 (거시 환경)"""
    nodes = [
        {"id": "h6", "x": -400, "y": -300, "width": 1400, "height": 100, "type": "text", "text": "# 📊 [Sector 6] 매크로 자본시장 · 밸류에이션 · 지정학 안보 맵\n> 빅테크 CAPEX ROI($500B 갭) ➔ GPU 금융 & 금리 리스크 ➔ AI 버블론 ➔ 소버린 AI & 미중 패권"},
        
        {"id": "t6_05", "x": -350, "y": -100, "width": 320, "height": 240, "type": "file", "file": p_thesis("T6-05-오픈AI·앤트로픽의-5000억달러-매출-갭과-데이터센터-ROI-딜레마.md")},
        {"id": "t6_03", "x": 50, "y": -100, "width": 320, "height": 240, "type": "file", "file": p_thesis("T6-03-AI-버블-가능성.md")},
        {"id": "t6_04", "x": 450, "y": -100, "width": 320, "height": 240, "type": "file", "file": p_thesis("T6-04-10년금리-5%-재진입-가능성.md")},
        
        {"id": "t6_01", "x": -350, "y": 200, "width": 320, "height": 240, "type": "file", "file": p_thesis("T6-01-금리와-데이터센터.md")},
        {"id": "t6_02", "x": 50, "y": 200, "width": 320, "height": 240, "type": "file", "file": p_thesis("T6-02-엔비디아와-GPU-금융.md")},
        {"id": "t6_09", "x": 450, "y": 200, "width": 320, "height": 240, "type": "file", "file": p_thesis("T6-09-엔비디아와-네오클라우드.md")},
        {"id": "t6_06", "x": 850, "y": 200, "width": 320, "height": 240, "type": "file", "file": p_thesis("T6-06-소버린-AI와-국가-단위-컴퓨트-인프라.md")},
        
        {"id": "c_coreweave", "x": -350, "y": 550, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-CoreWeave.md")},
        {"id": "c_nvda", "x": -50, "y": 550, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-NVIDIA.md")},
        {"id": "c_msft", "x": 250, "y": 550, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-Microsoft.md")},
        {"id": "c_ust", "x": 550, "y": 550, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-US_Treasury.md")},
    ]
    
    edges = [
        {"id": "e6_1", "fromNode": "t6_05", "fromSide": "right", "toNode": "t6_03", "toSide": "left", "label": "매출 갭 해소 실패 시 버블"},
        {"id": "e6_2", "fromNode": "t6_01", "fromSide": "right", "toNode": "t6_02", "toSide": "left", "label": "대안 파이낸싱"},
        {"id": "e6_3", "fromNode": "t6_02", "fromSide": "right", "toNode": "t6_09", "toSide": "left", "label": "GPU 담보 레버리지"},
        {"id": "e6_4", "fromNode": "t6_09", "fromSide": "bottom", "toNode": "c_coreweave", "toSide": "top", "label": "우선 할당"},
        {"id": "e6_5", "fromNode": "t6_04", "fromSide": "bottom", "toNode": "c_ust", "toSide": "top", "label": "국채 금리 부담"},
    ]
    return {"nodes": nodes, "edges": edges}


def generate_and_sync_canvases():
    print("\n🎨 [Canvas] 6대 섹터 인터랙티브 옵시디언 캔버스(.canvas) 생성 및 동기화 시작")
    print("═" * 70)
    
    canvases = [
        ("01-에너지-전력-냉각-인프라.canvas", create_canvas_01()),
        ("02-AI컴퓨트-메모리-선단반도체.canvas", create_canvas_02()),
        ("03-초고속네트워킹-시스템플랫폼.canvas", create_canvas_03()),
        ("04-파운데이션모델-엔터프라이즈SW.canvas", create_canvas_04()),
        ("05-피지컬AI-자율주행-로보틱스.canvas", create_canvas_05()),
        ("06-매크로-밸류에이션-지정학안보.canvas", create_canvas_06()),
    ]
    
    target_vaults = []
    if config.OBSIDIAN_PATH and config.OBSIDIAN_PATH.exists():
        target_vaults.append(config.OBSIDIAN_PATH)
    
    for filename, data in canvases:
        # 1. 로컬 thesis 디렉토리에 저장
        local_p = THESIS_DIR / filename
        local_p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  ✅ 로컬 생성: {local_p.name}")
        
        # 2. 옵시디언 볼트 동기화
        for vault in target_vaults:
            c_dir = vault / "argus" / "Canvas"
            c_dir.mkdir(parents=True, exist_ok=True)
            dest1 = c_dir / filename
            shutil.copy2(local_p, dest1)
            
            dest2 = vault / "argus" / filename
            shutil.copy2(local_p, dest2)
            
            print(f"     ➔ 볼트 동기화: {vault.name}/argus/Canvas/{filename}")

    print("═" * 70)
    print("✨ [완료] 6대 섹터 옵시디언 캔버스 파일 볼트 배치 완료!\n")


if __name__ == "__main__":
    generate_and_sync_canvases()
