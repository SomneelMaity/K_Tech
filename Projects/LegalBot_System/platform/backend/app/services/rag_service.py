import os
import re
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

from ..config import settings

_client: chromadb.ClientAPI | None = None
_collection = None


def _get_collection():
    global _client, _collection
    if _collection is not None:
        return _collection

    os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
    _client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)

    # DefaultEmbeddingFunction uses all-MiniLM-L6-v2 via onnxruntime (no torch needed)
    _collection = _client.get_or_create_collection(
        name="legalbot_kb",
        embedding_function=DefaultEmbeddingFunction(),
        metadata={"hnsw:space": "cosine"},
    )

    # Re-index whenever KB files on disk outnumber indexed entries
    kb_dir = Path(settings.KB_DIR)
    kb_count = sum(
        1 for f in kb_dir.rglob("*.md")
        if f.name not in ("SCHEMA.md", "README.md", "SEGMENT_README_TEMPLATE.md")
    ) if kb_dir.exists() else 0
    if _collection.count() < kb_count:
        _index_kb(_collection)

    return _collection


def _parse_entry(filepath: Path) -> dict | None:
    text = filepath.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None

    front: dict = {}
    for line in parts[1].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            front[k.strip()] = v.strip().strip('"')

    body = parts[2].strip()
    # Remove markdown headings and strip extra whitespace for embedding
    body_clean = re.sub(r"^#+\s+", "", body, flags=re.MULTILINE).strip()

    return {
        "entry_id": front.get("entry_id", filepath.stem),
        "segment": front.get("segment", ""),
        "title": front.get("title", ""),
        "act": front.get("act", ""),
        "section": front.get("section", ""),
        "state": front.get("state", "all"),
        "language": front.get("language", "en"),
        "source_url": front.get("source_url", ""),
        "content": body_clean,
    }


def _index_kb(collection) -> None:
    kb_dir = Path(settings.KB_DIR)
    if not kb_dir.exists():
        return

    docs, metas, ids = [], [], []
    for md_file in kb_dir.rglob("*.md"):
        if md_file.name in ("SCHEMA.md", "README.md"):
            continue
        entry = _parse_entry(md_file)
        if entry and entry["content"]:
            ids.append(entry["entry_id"])
            docs.append(entry["content"])
            metas.append({
                k: v for k, v in entry.items()
                if k != "content" and isinstance(v, str)
            })

    if docs:
        collection.upsert(documents=docs, metadatas=metas, ids=ids)


def retrieve(
    query: str,
    segment: str | None = None,
    state: str | None = None,
    top_k: int = 5,
) -> list[dict]:
    collection = _get_collection()
    if collection.count() == 0:
        return []

    where: dict = {}
    if segment:
        where["segment"] = segment

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count()),
        where=where if where else None,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({**meta, "content": doc, "score": round(1 - dist, 4)})

    return chunks

