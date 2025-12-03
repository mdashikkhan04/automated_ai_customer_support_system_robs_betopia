# File: app/services/kb_service.py

import json
import os
from typing import List, Tuple

import numpy as np
import openai

from app.config import get_settings
from app.models.schemas import KBItem

settings = get_settings()
openai.api_key = settings.OPENAI_API_KEY

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB_DATA_DIR = os.path.join(BASE_DIR, "kb", "data")


class KBService:
    def __init__(self):
        self.items: List[KBItem] = []
        self.embeddings: np.ndarray | None = None
        self._load_kb()

    def _load_kb(self):
        """Load KB JSON files and precompute embeddings (simple in-memory store)."""
        items: List[KBItem] = []

        for filename in ["faqs.json", "products.json"]:
            path = os.path.join(KB_DATA_DIR, filename)
            if not os.path.exists(path):
                continue
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for raw in data:
                    items.append(KBItem(**raw))

        self.items = items

        if not items:
            self.embeddings = None
            return

        texts = [self._item_to_text(item) for item in items]
        resp = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=texts,
        )
        vectors = [d["embedding"] for d in resp["data"]]
        self.embeddings = np.array(vectors)

    @staticmethod
    def _item_to_text(item: KBItem) -> str:
        parts = [
            f"Title: {item.title}",
            f"Type: {item.type}",
        ]
        if item.question:
            parts.append(f"Q: {item.question}")
        parts.append(f"A: {item.answer}")
        return "\n".join(parts)

    def search(self, query: str, top_k: int = 5) -> List[Tuple[KBItem, float]]:
        """Return top_k KB items with similarity score."""
        if not self.items or self.embeddings is None:
            return []

        q_resp = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=[query],
        )
        q_vec = np.array(q_resp["data"][0]["embedding"])

        # cosine similarity
        scores = self.embeddings @ q_vec / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(q_vec) + 1e-10
        )
        idx_sorted = np.argsort(scores)[::-1][:top_k]

        results: List[Tuple[KBItem, float]] = []
        for idx in idx_sorted:
            results.append((self.items[int(idx)], float(scores[int(idx)])))
        return results

    def build_context(self, query: str, top_k: int = 5) -> str:
        results = self.search(query, top_k=top_k)
        if not results:
            return ""

        blocks = []
        for item, score in results:
            block = f"[{item.type.upper()}] {item.title}\n"
            if item.question:
                block += f"Q: {item.question}\n"
            block += f"A: {item.answer}\n"
            blocks.append(block)

        return "\n\n---\n\n".join(blocks)


kb_service = KBService()
