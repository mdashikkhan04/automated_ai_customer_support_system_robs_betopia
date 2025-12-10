# app/services/kb_service.py
import json
import os
from typing import List, Tuple

import numpy as np
from openai import OpenAI

from app.config import get_settings
from app.models.schemas import KBItem

settings = get_settings()

# OpenAI client
_openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB_DATA_DIR = os.path.join(BASE_DIR, "kb", "data")


class KBService:
    """
    Lightweight in-memory KB service.

    ✅ এখন থেকে শুধু `complete_kb.json` ব্যবহার করবে
       – এই ফাইলটা তুমি নতুন Google Docs dataset থেকে বানাবে।
    """

    def __init__(self):
        self.items: List[KBItem] = []
        self.embeddings: np.ndarray | None = None
        self._load_kb()

    def _load_kb(self):
        """Load KB JSON file and precompute embeddings."""
        items: List[KBItem] = []

        filename = "complete_kb.json"
        path = os.path.join(KB_DATA_DIR, filename)
        if not os.path.exists(path):
            print(f"⚠️ KB file not found: {path}")
            self.items = []
            self.embeddings = None
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for raw in data:
                    items.append(KBItem(**raw))
        except Exception as e:
            print(f"⚠️ Could not load {filename}: {e}")
            self.items = []
            self.embeddings = None
            return

        self.items = items
        print(f"[OK] KB Service loaded {len(items)} items from {filename}")

        if not items:
            self.embeddings = None
            return

        texts = [self._item_to_text(item) for item in items]

        try:
            resp = _openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=texts,
            )
            vectors = [d.embedding for d in resp.data]
            self.embeddings = np.array(vectors)
            print(f"[OK] Embeddings generated for {len(items)} KB items")
        except Exception as e:
            print(f"⚠️ Could not generate embeddings: {e}")
            print("Fallback: using keyword search only.")
            self.embeddings = None

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

    def search(
        self,
        query: str,
        top_k: int = 5,
        use_keyword_fallback: bool = True,
    ) -> List[Tuple[KBItem, float]]:
        """Return top_k KB items with a similarity score."""
        if not self.items:
            return []

        # Fast keyword search first
        if use_keyword_fallback:
            keyword_results = self._keyword_search(query, top_k=top_k)
            if keyword_results:
                return keyword_results

        # Semantic search if embeddings are ready
        if self.embeddings is None:
            return []

        try:
            q_resp = _openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=[query],
            )
            q_vec = np.array(q_resp.data[0].embedding)

            # cosine similarity
            scores = self.embeddings @ q_vec / (
                np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(q_vec) + 1e-10
            )
            idx_sorted = np.argsort(scores)[::-1][:top_k]

            results: List[Tuple[KBItem, float]] = []
            for idx in idx_sorted:
                results.append((self.items[int(idx)], float(scores[int(idx)])))
            return results
        except Exception as e:
            print(f"⚠️ Semantic search failed: {e}, using keyword search")
            return self._keyword_search(query, top_k=top_k)

    def _keyword_search(self, query: str, top_k: int = 5) -> List[Tuple[KBItem, float]]:
        """Fast keyword-based search (no API calls)."""
        query_words = set(query.lower().split())
        results = []

        for item in self.items:
            text = f"{item.title} {item.question} {item.answer}".lower()
            matches = sum(1 for w in query_words if w in text)

            if matches > 0:
                title_matches = sum(
                    1 for w in query_words if w in item.title.lower()
                )
                confidence = (matches + title_matches * 2) / (len(query_words) + 1)
                results.append((item, min(confidence, 0.95)))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def build_context(self, query: str, top_k: int = 5) -> str:
        """Return a context block for the LLM prompt."""
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
