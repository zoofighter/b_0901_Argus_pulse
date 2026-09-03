"""
rag_engine.py — ChromaDB 기반 RAG 벡터 검색 엔진

구성:
  - 영속 저장소: db/chromadb/
  - 2대 컬렉션:
    1. argus_knowledge: 증권사 리포트(PDF), 웹 자료, 99.raw 파싱본
    2. argus_reports  : Argus Pulse 생성물(블로그, 스레드, 다이제스트, 리뷰)
  - 임베딩: ChromaDB 내장 ONNX 임베딩 (all-MiniLM-L6-v2, 고속 로컬 실행)
  - 청킹: 1,000자 단위, 200자 오버랩
"""

import hashlib
from pathlib import Path
from typing import Optional
import chromadb
from chromadb.config import Settings

import config

COLLECTION_KNOWLEDGE = "argus_knowledge"
COLLECTION_REPORTS   = "argus_reports"


def get_chroma_client() -> chromadb.PersistentClient:
    """ChromaDB Persistent Client 반환"""
    config.CHROMA_DB_PATH.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(
        path=str(config.CHROMA_DB_PATH),
        settings=Settings(anonymized_telemetry=False)
    )


def get_collection(name: str = COLLECTION_KNOWLEDGE):
    """컬렉션 가져오기 (없으면 자동 생성)"""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=name,
        metadata={"description": "Argus Pulse Intelligence Engine"}
    )


def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> list[str]:
    """텍스트를 chunk_size 단위로 분할 (overlap 적용)"""
    chunk_size = chunk_size or config.RAG_CHUNK_SIZE
    overlap    = overlap    or config.RAG_CHUNK_OVERLAP

    if len(text) <= chunk_size:
        return [text] if text.strip() else []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        start += (chunk_size - overlap)

    return chunks


def make_doc_id(source_path: str, chunk_idx: int) -> str:
    """고유 문서 청크 ID 생성 (SHA256 기반)"""
    raw = f"{source_path}#{chunk_idx}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def ingest_document(
    doc_text: str,
    metadata: dict,
    collection_name: str = COLLECTION_KNOWLEDGE
) -> int:
    """
    단일 문서를 청킹하여 ChromaDB에 인제스트
    Returns:
        저장된 청크 수
    """
    if not doc_text.strip():
        return 0

    col = get_collection(collection_name)
    chunks = chunk_text(doc_text)
    if not chunks:
        return 0

    ids = []
    documents = []
    metadatas = []

    source_key = metadata.get("filepath", metadata.get("filename", "unknown"))

    for idx, chunk in enumerate(chunks):
        chunk_id = make_doc_id(source_key, idx)
        ids.append(chunk_id)
        documents.append(chunk)
        meta_entry = {
            **metadata,
            "chunk_idx": idx,
            "total_chunks": len(chunks)
        }
        # ChromaDB 메타데이터는 bool, int, float, str 만 허용
        sanitized_meta = {
            k: str(v) if isinstance(v, (list, dict)) else v
            for k, v in meta_entry.items()
            if v is not None
        }
        metadatas.append(sanitized_meta)

    # 일괄 upsert (중복 시 덮어쓰기)
    col.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    return len(chunks)


def search(
    query: str,
    n_results: int = None,
    collection_name: Optional[str] = None,
    company_filter: Optional[str] = None
) -> list[dict]:
    """
    RAG 벡터 검색
    - collection_name 미지정 시 knowledge와 reports 양쪽 모두 검색하여 유사도 순 병합
    """
    n_results = n_results or config.RAG_TOP_K
    client = get_chroma_client()

    cols_to_search = []
    if collection_name:
        cols_to_search = [get_collection(collection_name)]
    else:
        # 양쪽 모두 검색
        try:
            cols_to_search.append(get_collection(COLLECTION_KNOWLEDGE))
        except Exception:
            pass
        try:
            cols_to_search.append(get_collection(COLLECTION_REPORTS))
        except Exception:
            pass

    where_clause = {"company": company_filter} if company_filter else None

    all_hits = []
    for col in cols_to_search:
        count = col.count()
        if count == 0:
            continue

        actual_n = min(n_results, count)
        try:
            results = col.query(
                query_texts=[query],
                n_results=actual_n,
                where=where_clause
            )
        except Exception as e:
            print(f"  ⚠️ ChromaDB 검색 오류 ({col.name}): {e}")
            continue

        if results and results.get("documents") and results["documents"][0]:
            docs = results["documents"][0]
            metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
            dists = results["distances"][0] if results.get("distances") else [0.0] * len(docs)

            for d, m, dist in zip(docs, metas, dists):
                all_hits.append({
                    "text": d,
                    "metadata": m,
                    "distance": dist,
                    "collection": col.name
                })

    # 거리(distance) 오름차순 정렬 (코사인 거리 기준 낮을수록 유사)
    all_hits.sort(key=lambda x: x["distance"])
    return all_hits[:n_results]


def format_rag_context(chunks: list[dict], max_chars: int = 2500) -> str:
    """LLM 프롬프트에 주입할 마크다운 컨텍스트 블록 생성"""
    if not chunks:
        return ""

    lines = [
        "────────────────────────────────────────────────────────────",
        "📚 [Argus 지식 DB — 증권사 리포트 및 심층 데이터 참조]",
        "아래 리포트의 구체적 수치, 추정치, 분석 논리를 본문에 적극 인용하세요.",
        "────────────────────────────────────────────────────────────"
    ]

    total_len = 0
    for idx, c in enumerate(chunks, 1):
        m = c.get("metadata", {})
        header_parts = []
        if m.get("company"):
            header_parts.append(m["company"])
        if m.get("broker"):
            header_parts.append(m["broker"])
        if m.get("date"):
            header_parts.append(m["date"])
        if m.get("title"):
            header_parts.append(m["title"][:30])

        header = " | ".join(header_parts) or m.get("filename", f"문헌 {idx}")
        chunk_text = c["text"].strip()

        block = f"\n[출처 {idx}: {header}]\n{chunk_text}\n"
        if total_len + len(block) > max_chars:
            # 남은 길이만큼 잘라서 넣고 종료
            remaining = max_chars - total_len
            if remaining > 100:
                lines.append(block[:remaining] + "\n...(중략)")
            break

        lines.append(block)
        total_len += len(block)

    return "\n".join(lines)


def get_db_status() -> dict:
    """ChromaDB 컬렉션 현황 반환"""
    client = get_chroma_client()
    status = {}
    for name in [COLLECTION_KNOWLEDGE, COLLECTION_REPORTS]:
        try:
            col = client.get_collection(name)
            status[name] = col.count()
        except Exception:
            status[name] = 0
    return status


if __name__ == "__main__":
    print("=== ChromaDB RAG 엔진 상태 점검 ===")
    stat = get_db_status()
    for k, v in stat.items():
        print(f"  - {k}: {v:,}개 청크")
