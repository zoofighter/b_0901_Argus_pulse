"""
scripts/generate_sector_canvases.py — 젠슨 황 5단 케이크 + 거시 환경 6대 섹터 인터랙티브 옵시디언 캔버스(.canvas) 생성기
"""

import json
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
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
        {"id": "h2", "x": -400, "y": -300, "width": 1200, "height": 100, "type": "text", "text": "# 💾 [Sector 2] AI 컴퓨트 · 메모리 · 선단 반도체 밸류체인 맵 (젠슨 황 2단)\n> HBM4 커스텀화 ➔ 첨단 패키징(CoWoS/유리기판) ➔ 2nm GAA ➔ 빅테크 커스텀 ASIC 생태계"},
        
        {"id": "top_hbm", "x": -350, "y": -100, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-HBM.md")},
        {"id": "top_cowos", "x": 50, "y": -100, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-CoWoS.md")},
        {"id": "top_glass", "x": 450, "y": -100, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-유리기판.md")},
        
        {"id": "top_asic", "x": -350, "y": 200, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-ASIC.md")},
        {"id": "top_gaa", "x": 50, "y": 200, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-2nm-GAA.md")},
        {"id": "top_cxl", "x": 450, "y": 200, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-CXL.md")},
        
        {"id": "t2_01", "x": -350, "y": 500, "width": 320, "height": 240, "type": "file", "file": p_thesis("T2-01-메모리-산업의-변화.md")},
        {"id": "t2_02", "x": 50, "y": 500, "width": 320, "height": 240, "type": "file", "file": p_thesis("T2-02-첨단-패키징과-CoWoS의-병목.md")},
        {"id": "t2_03", "x": 450, "y": 500, "width": 320, "height": 240, "type": "file", "file": p_thesis("T2-03-유리기판의-차세대-패키징-침투.md")},
        
        {"id": "c_hynix", "x": -350, "y": 820, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-SK하이닉스.md")},
        {"id": "c_samsung", "x": -50, "y": 820, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-삼성전자.md")},
        {"id": "c_tsmc", "x": 250, "y": 820, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-TSMC.md")},
        {"id": "c_nvda", "x": 550, "y": 820, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-NVIDIA.md")},
    ]
    
    edges = [
        {"id": "e2_1", "fromNode": "top_hbm", "fromSide": "right", "toNode": "top_cowos", "toSide": "left", "label": "2.5D 통합"},
        {"id": "e2_2", "fromNode": "top_cowos", "fromSide": "right", "toNode": "top_glass", "toSide": "left", "label": "대면적 기판 혁신"},
        {"id": "e2_3", "fromNode": "top_hbm", "fromSide": "bottom", "toNode": "t2_01", "toSide": "top", "label": "HBM4 커스텀화"},
        {"id": "e2_4", "fromNode": "top_cowos", "fromSide": "bottom", "toNode": "t2_02", "toSide": "top", "label": "패키징 병목"},
        {"id": "e2_5", "fromNode": "top_glass", "fromSide": "bottom", "toNode": "t2_03", "toSide": "top", "label": "유리기판 침투"},
        {"id": "e2_6", "fromNode": "t2_01", "fromSide": "bottom", "toNode": "c_hynix", "toSide": "top", "label": "HBM 선두"},
        {"id": "e2_7", "fromNode": "t2_01", "fromSide": "bottom", "toNode": "c_samsung", "toSide": "top", "label": "HBM3E/4 수주전"},
        {"id": "e2_8", "fromNode": "t2_02", "fromSide": "bottom", "toNode": "c_tsmc", "toSide": "top", "label": "CoWoS 독점"},
        {"id": "e2_9", "fromNode": "top_asic", "fromSide": "bottom", "toNode": "c_nvda", "toSide": "top", "label": "GPU 독점 견제"},
    ]
    return {"nodes": nodes, "edges": edges}


def create_canvas_03():
    """3. T3: 초고속 네트워킹 & 시스템 플랫폼 캔버스 (젠슨 황 3단)"""
    nodes = [
        {"id": "h3", "x": -400, "y": -300, "width": 1200, "height": 100, "type": "text", "text": "# 🌐 [Sector 3] 초고속 네트워킹 & 분산 시스템 플랫폼 맵 (젠슨 황 3단)\n> CPO 실리콘 포토닉스 ➔ UEC vs 인피니밴드 통신 패브릭 ➔ 분산 데이터센터 코로케이션 ➔ 네오클라우드"},
        
        {"id": "top_cpo", "x": -350, "y": -100, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-실리콘포토닉스.md")},
        {"id": "top_net", "x": 50, "y": -100, "width": 320, "height": 220, "type": "file", "file": p_topic("Topic-초고속네트워킹.md")},
        
        {"id": "t3_01", "x": -350, "y": 200, "width": 320, "height": 240, "type": "file", "file": p_thesis("T3-01-실리콘-포토닉스와-CPO의-상용화.md")},
        {"id": "t3_02", "x": 50, "y": 200, "width": 320, "height": 240, "type": "file", "file": p_thesis("T3-02-초고속-AI-네트워킹-UEC-vs-인피니밴드.md")},
        {"id": "t3_03", "x": 450, "y": 200, "width": 320, "height": 240, "type": "file", "file": p_thesis("T3-03-전력-포화와-분산형-AI-데이터센터-코로케이션.md")},
        {"id": "t3_04", "x": 850, "y": 200, "width": 320, "height": 240, "type": "file", "file": p_thesis("T3-04-엔비디아와-네오클라우드.md")},
        
        {"id": "c_arista", "x": -350, "y": 550, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-Broadcom.md")},
        {"id": "c_coreweave", "x": 50, "y": 550, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-CoreWeave.md")},
        {"id": "c_equinix", "x": 450, "y": 550, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-Equinix.md")},
    ]
    
    edges = [
        {"id": "e3_1", "fromNode": "top_cpo", "fromSide": "right", "toNode": "top_net", "toSide": "left", "label": "광인터커넥트 전환"},
        {"id": "e3_2", "fromNode": "top_cpo", "fromSide": "bottom", "toNode": "t3_01", "toSide": "top", "label": "스케일아웃 통신"},
        {"id": "e3_3", "fromNode": "top_net", "fromSide": "bottom", "toNode": "t3_02", "toSide": "top", "label": "표준 연합 대결"},
        {"id": "e3_4", "fromNode": "t3_04", "fromSide": "bottom", "toNode": "c_coreweave", "toSide": "top", "label": "클러스터 대여"},
    ]
    return {"nodes": nodes, "edges": edges}


def create_canvas_04():
    """4. T4: 파운데이션 모델 & 엔터프라이즈 SW 캔버스 (젠슨 황 4단)"""
    nodes = [
        {"id": "h4", "x": -400, "y": -300, "width": 1200, "height": 100, "type": "text", "text": "# 💻 [Sector 4] 파운데이션 모델 & 엔터프라이즈 SW 맵 (젠슨 황 4단)\n> 오픈소스 LLM 고도화 ➔ 온프레미스 사설 AI ➔ 빅테크 SW 플랫폼 과점화 ➔ 버티컬 바이오 AI"},
        
        {"id": "t4_01", "x": -350, "y": -100, "width": 320, "height": 240, "type": "file", "file": p_thesis("T4-01-오픈소스-모델-고도화와-온프레미스-사설-AI.md")},
        {"id": "t4_02", "x": 50, "y": -100, "width": 320, "height": 240, "type": "file", "file": p_thesis("T4-02-AI-소프트웨어-레이어의-과점화.md")},
        {"id": "t4_03", "x": 450, "y": -100, "width": 320, "height": 240, "type": "file", "file": p_thesis("T4-03-바이오AI와-신약개발-가속.md")},
        {"id": "t4_04", "x": 850, "y": -100, "width": 320, "height": 240, "type": "file", "file": p_thesis("T4-04-TPU-증가와-GPU-수요-둔화.md")},
        
        {"id": "c_msft", "x": -350, "y": 250, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-Microsoft.md")},
        {"id": "c_meta", "x": 50, "y": 250, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-Meta.md")},
        {"id": "c_alphabet", "x": 450, "y": 250, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-Alphabet.md")},
    ]
    
    edges = [
        {"id": "e4_1", "fromNode": "t4_01", "fromSide": "right", "toNode": "t4_02", "toSide": "left", "label": "SW 통합 플랫폼"},
        {"id": "e4_2", "fromNode": "t4_01", "fromSide": "bottom", "toNode": "c_meta", "toSide": "top", "label": "Llama 오픈소스"},
        {"id": "e4_3", "fromNode": "t4_02", "fromSide": "bottom", "toNode": "c_msft", "toSide": "top", "label": "Copilot 생태계"},
        {"id": "e4_4", "fromNode": "t4_04", "fromSide": "bottom", "toNode": "c_alphabet", "toSide": "top", "label": "자체 TPU 최적화"},
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
        {"id": "h6", "x": -400, "y": -300, "width": 1200, "height": 100, "type": "text", "text": "# 📊 [Sector 6] 매크로 자본시장 · 밸류에이션 · 지정학 안보 맵\n> 고금리 장기화(5%) ➔ 빅테크 CAPEX ROI 회수 압박 ➔ GPU 금융 리스크 ➔ 소버린 AI & 미중 패권"},
        
        {"id": "t6_01", "x": -350, "y": -100, "width": 320, "height": 240, "type": "file", "file": p_thesis("T6-01-금리와-데이터센터.md")},
        {"id": "t6_03", "x": 50, "y": -100, "width": 320, "height": 240, "type": "file", "file": p_thesis("T6-03-AI-버블-가능성.md")},
        {"id": "t6_05", "x": 450, "y": -100, "width": 320, "height": 240, "type": "file", "file": p_thesis("T6-05-오픈AI·앤트로픽의-5000억달러-매출-갭과-데이터센터-ROI-딜레마.md")},
        
        {"id": "t6_02", "x": -350, "y": 200, "width": 320, "height": 240, "type": "file", "file": p_thesis("T6-02-엔비디아와-GPU-금융.md")},
        {"id": "t6_06", "x": 50, "y": 200, "width": 320, "height": 240, "type": "file", "file": p_thesis("T6-06-소버린-AI와-국가-단위-컴퓨트-인프라.md")},
        {"id": "t6_07", "x": 450, "y": 200, "width": 320, "height": 240, "type": "file", "file": p_thesis("T6-07-중국반도체의-HBM-생산가능성.md")},
        
        {"id": "c_coreweave", "x": -350, "y": 550, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-CoreWeave.md")},
        {"id": "c_msft", "x": -50, "y": 550, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-Microsoft.md")},
        {"id": "c_openai", "x": 250, "y": 550, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-OpenAI.md")},
        {"id": "c_anthropic", "x": 550, "y": 550, "width": 260, "height": 160, "type": "file", "file": p_comp("Company-Anthropic.md")},
    ]
    
    edges = [
        {"id": "e6_1", "fromNode": "t6_01", "fromSide": "right", "toNode": "t6_03", "toSide": "left", "label": "할인율 상승 압박"},
        {"id": "e6_2", "fromNode": "t6_03", "fromSide": "right", "toNode": "t6_05", "toSide": "left", "label": "$500B 매출 갭"},
        {"id": "e6_3", "fromNode": "t6_01", "fromSide": "bottom", "toNode": "t6_02", "toSide": "top", "label": "대안 파이낸싱"},
        {"id": "e6_4", "fromNode": "t6_02", "fromSide": "bottom", "toNode": "c_coreweave", "toSide": "top", "label": "부채 레버리지"},
        {"id": "e6_5", "fromNode": "t6_05", "fromSide": "bottom", "toNode": "c_openai", "toSide": "top", "label": "수익화 모델 검증"},
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
    
    target_vaults = [
        Path("/Users/boon/Library/Mobile Documents/iCloud~md~obsidian/Documents/obs_argus"),
        Path("/Users/boon/Library/Mobile Documents/iCloud~md~obsidian/Documents/agent_vault"),
    ]
    
    # Clean up old legacy canvas names if they exist
    old_canvas_names = [
        "01-반도체-컴퓨트-생태계.canvas",
        "02-인프라-전력-냉각-생태계.canvas",
        "03-피지컬AI-자율주행-로보틱스.canvas",
        "04-매크로-밸류에이션-빅테크ROI.canvas",
    ]
    
    for old_name in old_canvas_names:
        (THESIS_DIR / old_name).unlink(missing_ok=True)
        for vault in target_vaults:
            (vault / "argus" / "Canvas" / old_name).unlink(missing_ok=True)
            (vault / "argus" / old_name).unlink(missing_ok=True)
    
    for filename, data in canvases:
        # 1. 로컬 thesis 디렉토리에 저장
        local_p = THESIS_DIR / filename
        local_p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  ✅ 로컬 생성: {local_p.name}")
        
        # 2. 각 옵시디언 볼트의 argus/Canvas/ 및 argus/ 루트에 저장
        for vault in target_vaults:
            if not vault.exists():
                continue
            
            # argus/Canvas/
            c_dir = vault / "argus" / "Canvas"
            c_dir.mkdir(parents=True, exist_ok=True)
            dest1 = c_dir / filename
            shutil.copy2(local_p, dest1)
            
            # argus/ (루트에서도 바로 보이도록)
            dest2 = vault / "argus" / filename
            shutil.copy2(local_p, dest2)
            
            print(f"     ➔ 볼트 동기화: {vault.name}/argus/Canvas/{filename}")

    print("═" * 70)
    print("✨ [완료] 6대 섹터 옵시디언 캔버스 파일 볼트 배치 완료!\n")


if __name__ == "__main__":
    generate_and_sync_canvases()
