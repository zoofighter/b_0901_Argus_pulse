"""
scripts/generate_sector_canvases.py — 4대 섹터 인터랙티브 옵시디언 캔버스(.canvas) 생성기
"""

import json
import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
THESIS_DIR = ROOT_DIR / "thesis"


def create_canvas_01():
    """1. 반도체 & 컴퓨트 생태계 캔버스"""
    nodes = [
        # 그룹 1: 헤더
        {"id": "h1", "x": -400, "y": -300, "width": 1200, "height": 100, "type": "text", "text": "# ⚡ [Sector 1] 반도체 & 컴퓨팅 밸류체인 맵\n> 미세화 한계 돌파 ➔ 첨단 패키징(CoWoS/유리기판) ➔ 커스텀 ASIC 및 고속 통신 생태계"},
        
        # 핵심 토픽 노드
        {"id": "top_hbm", "x": -350, "y": -100, "width": 320, "height": 200, "type": "file", "file": "thesis/Topic-HBM.md"},
        {"id": "top_cowos", "x": 50, "y": -100, "width": 320, "height": 200, "type": "file", "file": "thesis/Topic-CoWoS.md"},
        {"id": "top_glass", "x": 450, "y": -100, "width": 320, "height": 200, "type": "file", "file": "thesis/Topic-유리기판.md"},
        
        {"id": "top_asic", "x": -350, "y": 200, "width": 320, "height": 200, "type": "file", "file": "thesis/Topic-ASIC.md"},
        {"id": "top_gaa", "x": 50, "y": 200, "width": 320, "height": 200, "type": "file", "file": "thesis/Topic-2nm-GAA.md"},
        {"id": "top_cpo", "x": 450, "y": 200, "width": 320, "height": 200, "type": "file", "file": "thesis/Topic-실리콘포토닉스.md"},
        
        # 핵심 테제 노드
        {"id": "t1_01", "x": -350, "y": 500, "width": 320, "height": 220, "type": "file", "file": "thesis/T1-01-메모리-산업의-변화.md"},
        {"id": "t1_04", "x": 50, "y": 500, "width": 320, "height": 220, "type": "file", "file": "thesis/T1-04-첨단-패키징과-CoWoS의-병목.md"},
        {"id": "t1_05", "x": 450, "y": 500, "width": 320, "height": 220, "type": "file", "file": "thesis/T1-05-유리기판의-차세대-패키징-침투.md"},
        
        # 기업 노드
        {"id": "c_hynix", "x": -350, "y": 800, "width": 260, "height": 140, "type": "file", "file": "thesis/Company-SK하이닉스.md"},
        {"id": "c_samsung", "x": -50, "y": 800, "width": 260, "height": 140, "type": "file", "file": "thesis/Company-삼성전자.md"},
        {"id": "c_tsmc", "x": 250, "y": 800, "width": 260, "height": 140, "type": "file", "file": "thesis/Company-TSMC.md"},
        {"id": "c_nvda", "x": 550, "y": 800, "width": 260, "height": 140, "type": "file", "file": "thesis/Company-NVIDIA.md"},
    ]
    
    edges = [
        {"id": "e1", "fromNode": "top_hbm", "fromSide": "right", "toNode": "top_cowos", "toSide": "left", "label": "2.5D 통합"},
        {"id": "e2", "fromNode": "top_cowos", "fromSide": "right", "toNode": "top_glass", "toSide": "left", "label": "대면적 기판 혁신"},
        {"id": "e3", "fromNode": "top_hbm", "fromSide": "bottom", "toNode": "t1_01", "toSide": "top", "label": "HBM4 커스텀화"},
        {"id": "e4", "fromNode": "top_cowos", "fromSide": "bottom", "toNode": "t1_04", "toSide": "top", "label": "패키징 병목"},
        {"id": "e5", "fromNode": "top_glass", "fromSide": "bottom", "toNode": "t1_05", "toSide": "top", "label": "유리기판 침투"},
        {"id": "e6", "fromNode": "t1_01", "fromSide": "bottom", "toNode": "c_hynix", "toSide": "top", "label": "HBM 선두"},
        {"id": "e7", "fromNode": "t1_01", "fromSide": "bottom", "toNode": "c_samsung", "toSide": "top", "label": "HBM3E 추격"},
        {"id": "e8", "fromNode": "t1_04", "fromSide": "bottom", "toNode": "c_tsmc", "toSide": "top", "label": "CoWoS 독점"},
        {"id": "e9", "fromNode": "top_asic", "fromSide": "bottom", "toNode": "c_nvda", "toSide": "top", "label": "GPU 독점 견제"},
    ]
    return {"nodes": nodes, "edges": edges}


def create_canvas_02():
    """2. 인프라 & 전력 & 냉각 캔버스"""
    nodes = [
        {"id": "h2", "x": -400, "y": -300, "width": 1200, "height": 100, "type": "text", "text": "# 🔌 [Sector 2] 데이터센터 전력 & 액체냉각 인프라 맵\n> 전력 밀도 폭증 ➔ 수랭식 냉각 전환 ➔ 초고압 변압기 쇼티지 ➔ 무탄소 SMR & 대용량 ESS"},
        
        {"id": "top_liquid", "x": -350, "y": -100, "width": 320, "height": 200, "type": "file", "file": "thesis/Topic-액체냉각.md"},
        {"id": "top_grid", "x": 50, "y": -100, "width": 320, "height": 200, "type": "file", "file": "thesis/Topic-전력그리드.md"},
        {"id": "top_smr", "x": 450, "y": -100, "width": 320, "height": 200, "type": "file", "file": "thesis/Topic-SMR.md"},
        
        {"id": "t2_01", "x": -350, "y": 200, "width": 320, "height": 220, "type": "file", "file": "thesis/T2-01-데이터센터의-변화.md"},
        {"id": "t2_02", "x": 50, "y": 200, "width": 320, "height": 220, "type": "file", "file": "thesis/T2-02-데이터센터-액체냉각의-표준화.md"},
        {"id": "t2_05", "x": 450, "y": 200, "width": 320, "height": 220, "type": "file", "file": "thesis/T2-05-변압기-초고압-그리드-쇼티지-장기화.md"},
        
        {"id": "t2_04", "x": -350, "y": 500, "width": 320, "height": 220, "type": "file", "file": "thesis/T2-04-AI-전력망용-대용량-ESS와-LFP-공급망.md"},
        {"id": "t2_07", "x": 50, "y": 500, "width": 320, "height": 220, "type": "file", "file": "thesis/T2-07-800V-48V-HVDC-전력-아키텍처-혁신.md"},
        {"id": "top_ess", "x": 450, "y": 500, "width": 320, "height": 200, "type": "file", "file": "thesis/Topic-ESS.md"},
        
        {"id": "c_vertiv", "x": -350, "y": 800, "width": 260, "height": 140, "type": "file", "file": "thesis/Company-Vertiv.md"},
        {"id": "c_hd", "x": -50, "y": 800, "width": 260, "height": 140, "type": "file", "file": "thesis/Company-HD현대일렉트릭.md"},
        {"id": "c_ls", "x": 250, "y": 800, "width": 260, "height": 140, "type": "file", "file": "thesis/Company-LS-ELECTRIC.md"},
        {"id": "c_ge", "x": 550, "y": 800, "width": 260, "height": 140, "type": "file", "file": "thesis/Company-GE-Vernova.md"},
    ]
    
    edges = [
        {"id": "e2_1", "fromNode": "top_liquid", "fromSide": "right", "toNode": "top_grid", "toSide": "left", "label": "냉각 전력 소모"},
        {"id": "e2_2", "fromNode": "top_grid", "fromSide": "right", "toNode": "top_smr", "toSide": "left", "label": "기저부하 확보"},
        {"id": "e2_3", "fromNode": "top_liquid", "fromSide": "bottom", "toNode": "t2_02", "toSide": "top", "label": "DLC 표준화"},
        {"id": "e2_4", "fromNode": "top_grid", "fromSide": "bottom", "toNode": "t2_05", "toSide": "top", "label": "리드타임 4년+"},
        {"id": "e2_5", "fromNode": "t2_02", "fromSide": "bottom", "toNode": "c_vertiv", "toSide": "top", "label": "CDU 독점 공급"},
        {"id": "e2_6", "fromNode": "t2_05", "fromSide": "bottom", "toNode": "c_hd", "toSide": "top", "label": "초고압 변압기 수혜"},
        {"id": "e2_7", "fromNode": "t2_05", "fromSide": "bottom", "toNode": "c_ls", "toSide": "top", "label": "배전/스위치기어"},
    ]
    return {"nodes": nodes, "edges": edges}


def create_canvas_03():
    """3. 피지컬 AI & 로보틱스 캔버스"""
    nodes = [
        {"id": "h3", "x": -400, "y": -300, "width": 1200, "height": 100, "type": "text", "text": "# 🤖 [Sector 3] 피지컬 AI · 자율주행 · 로보틱스 맵\n> 공간지능 기반 VLA 파운데이션 모델 ➔ E2E 자율주행 & 로보택시 ➔ 휴머노이드 액추에이터 ➔ 온디바이스 AI"},
        
        {"id": "top_physical", "x": -350, "y": -100, "width": 320, "height": 200, "type": "file", "file": "thesis/Topic-피지컬AI.md"},
        {"id": "top_fsd", "x": 50, "y": -100, "width": 320, "height": 200, "type": "file", "file": "thesis/Topic-자율주행.md"},
        {"id": "top_ondevice", "x": 450, "y": -100, "width": 320, "height": 200, "type": "file", "file": "thesis/Topic-온디바이스AI.md"},
        
        {"id": "t3_03", "x": -350, "y": 200, "width": 320, "height": 220, "type": "file", "file": "thesis/T3-03-휴머노이드-로봇과-액추에이터-공급망.md"},
        {"id": "t3_04", "x": 50, "y": 200, "width": 320, "height": 220, "type": "file", "file": "thesis/T3-04-End-to-End-AI-자율주행과-로보택시.md"},
        {"id": "t3_05", "x": 450, "y": 200, "width": 320, "height": 220, "type": "file", "file": "thesis/T3-05-피지컬-AI와-공간지능-반도체.md"},
        
        {"id": "c_tesla", "x": -200, "y": 550, "width": 260, "height": 140, "type": "file", "file": "thesis/Company-Tesla.md"},
        {"id": "c_apple", "x": 100, "y": 550, "width": 260, "height": 140, "type": "file", "file": "thesis/Company-Apple.md"},
        {"id": "c_qualcomm", "x": 400, "y": 550, "width": 260, "height": 140, "type": "file", "file": "thesis/Company-Qualcomm.md"},
    ]
    
    edges = [
        {"id": "e3_1", "fromNode": "top_physical", "fromSide": "right", "toNode": "top_fsd", "toSide": "left", "label": "공간지능 이식"},
        {"id": "e3_2", "fromNode": "top_fsd", "fromSide": "right", "toNode": "top_ondevice", "toSide": "left", "label": "엣지 NPU 처리"},
        {"id": "e3_3", "fromNode": "top_physical", "fromSide": "bottom", "toNode": "t3_03", "toSide": "top", "label": "하드웨어 구동부"},
        {"id": "e3_4", "fromNode": "top_fsd", "fromSide": "bottom", "toNode": "t3_04", "toSide": "top", "label": "신경망 운전"},
        {"id": "e3_5", "fromNode": "t3_04", "fromSide": "bottom", "toNode": "c_tesla", "toSide": "top", "label": "FSD V12 / Cybercab"},
        {"id": "e3_6", "fromNode": "top_ondevice", "fromSide": "bottom", "toNode": "c_apple", "toSide": "top", "label": "Apple Intelligence"},
    ]
    return {"nodes": nodes, "edges": edges}


def create_canvas_04():
    """4. 매크로 & 밸류에이션 & 빅테크 ROI 캔버스"""
    nodes = [
        {"id": "h4", "x": -400, "y": -300, "width": 1200, "height": 100, "type": "text", "text": "# 📊 [Sector 4] 매크로 · 밸류에이션 · 빅테크 ROI 딜레마\n> 고금리 장기화(5%) ➔ 빅테크 CAPEX ROI 회수 압박 ➔ GPU 담보 금융 및 네오클라우드 리스크 ➔ 버블 vs 실적 차별화"},
        
        {"id": "t4_01", "x": -350, "y": -100, "width": 320, "height": 220, "type": "file", "file": "thesis/T4-01-금리와-데이터센터.md"},
        {"id": "t4_04", "x": 50, "y": -100, "width": 320, "height": 220, "type": "file", "file": "thesis/T4-04-AI-버블-가능성.md"},
        {"id": "t4_06", "x": 450, "y": -100, "width": 320, "height": 220, "type": "file", "file": "thesis/T4-06-오픈AI·앤트로픽의-5000억달러-매출-갭과-데이터센터-ROI-딜레마.md"},
        
        {"id": "t4_02", "x": -350, "y": 200, "width": 320, "height": 220, "type": "file", "file": "thesis/T4-02-엔비디아와-네오클라우드.md"},
        {"id": "t4_03", "x": 50, "y": 200, "width": 320, "height": 220, "type": "file", "file": "thesis/T4-03-엔비디아와-GPU-금융.md"},
        {"id": "t4_05", "x": 450, "y": 200, "width": 320, "height": 220, "type": "file", "file": "thesis/T4-05-10년금리-5%-재진입-가능성.md"},
        
        {"id": "c_coreweave", "x": -350, "y": 550, "width": 260, "height": 140, "type": "file", "file": "thesis/Company-CoreWeave.md"},
        {"id": "c_msft", "x": -50, "y": 550, "width": 260, "height": 140, "type": "file", "file": "thesis/Company-Microsoft.md"},
        {"id": "c_openai", "x": 250, "y": 550, "width": 260, "height": 140, "type": "file", "file": "thesis/Company-OpenAI.md"},
        {"id": "c_anthropic", "x": 550, "y": 550, "width": 260, "height": 140, "type": "file", "file": "thesis/Company-Anthropic.md"},
    ]
    
    edges = [
        {"id": "e4_1", "fromNode": "t4_01", "fromSide": "right", "toNode": "t4_04", "toSide": "left", "label": "할인율 상승 압박"},
        {"id": "e4_2", "fromNode": "t4_04", "fromSide": "right", "toNode": "t4_06", "toSide": "left", "label": "$500B 매출 갭"},
        {"id": "e4_3", "fromNode": "t4_01", "fromSide": "bottom", "toNode": "t4_02", "toSide": "top", "label": "대안 인프라"},
        {"id": "e4_4", "fromNode": "t4_02", "fromSide": "right", "toNode": "t4_03", "toSide": "left", "label": "GPU 담보 차입"},
        {"id": "e4_5", "fromNode": "t4_02", "fromSide": "bottom", "toNode": "c_coreweave", "toSide": "top", "label": "네오클라우드 허브"},
        {"id": "e4_6", "fromNode": "t4_06", "fromSide": "bottom", "toNode": "c_openai", "toSide": "top", "label": "수익화 모델 검증"},
    ]
    return {"nodes": nodes, "edges": edges}


def generate_all_canvases():
    print("\n🎨 [Canvas] 4대 섹터 인터랙티브 옵시디언 캔버스(.canvas) 생성 시작")
    print("═" * 70)
    
    canvases = [
        ("01-반도체-컴퓨트-생태계.canvas", create_canvas_01()),
        ("02-인프라-전력-냉각-생태계.canvas", create_canvas_02()),
        ("03-피지컬AI-자율주행-로보틱스.canvas", create_canvas_03()),
        ("04-매크로-밸류에이션-빅테크ROI.canvas", create_canvas_04()),
    ]
    
    for filename, data in canvases:
        target_path = THESIS_DIR / filename
        target_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  ✅ 생성 완료: {target_path.name} (노드 {len(data['nodes'])}개, 엣지 {len(data['edges'])}개)")
        
        # 옵시디언 볼트로 동기화
        try:
            from obsidian_sync import sync_file
            sync_file(target_path, "theses")
        except Exception:
            pass

    print("═" * 70)
    print("✨ [완료] 4대 섹터 Visual Canvas 파일 구축 및 옵시디언 동기화 완료!\n")


if __name__ == "__main__":
    generate_all_canvases()
