"""
Push latest KB & scraping data to Pinecone index.

Usage (from project root, venv active):
    $env:PYTHONPATH="."
    python .\app\services\pinecone_ingest.py
"""
import os
import sys
import json
from dotenv import load_dotenv

# Fix Python path for direct script execution
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT_DIR)

load_dotenv()

from app.services.pinecone_client import pinecone_index
from app.services.openai_service import get_embedding

KB_DATA_DIR = os.path.join(ROOT_DIR, "app", "kb", "data")
KB_FILE = os.path.join(KB_DATA_DIR, "complete_kb.json")
SCRAPING_CACHE = os.path.join(ROOT_DIR, "app", "kb", "cache", "scraped_data.json")


def load_all_kb_items():
    """Load KB items from the new consolidated complete_kb.json only."""
    if not os.path.exists(KB_FILE):
        print(f"⚠️ KB file not found: {KB_FILE}")
        return []

    try:
        with open(KB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"[OK] Loaded {len(data)} KB items from complete_kb.json")
        return data
    except Exception as e:
        print(f"⚠️ Failed to load KB file: {e}")
        return []


def load_scraping_data():
    """Load scraped pages (products/FAQ/policies/pages) from cache."""
    if not os.path.exists(SCRAPING_CACHE):
        print(f"ℹ️ No scraping cache found at {SCRAPING_CACHE}")
        return []

    with open(SCRAPING_CACHE, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = []

    # Old structured format
    for section in ["products", "faqs", "policies"]:
        for entry in data.get(section, []):
            items.append(entry)

    # New generic "pages" format
    for page in data.get("pages", []):
        content_parts = []
        if page.get("title"):
            content_parts.append(page["title"])
        if page.get("headings"):
            content_parts.extend(page["headings"])
        if page.get("paragraphs"):
            content_parts.extend(page["paragraphs"])

        content = "\n\n".join(content_parts)
        items.append(
            {
                "title": page.get("title") or page.get("url"),
                "content": content,
                "source_url": page.get("url"),
            }
        )

    print(f"[OK] Loaded {len(items)} scraping items from cache")
    return items


def upsert_to_pinecone(items, namespace="kb"):
    """Upsert list of items into Pinecone under a given namespace."""
    batch = []
    for i, item in enumerate(items):
        text = (
            item.get("content")
            or item.get("answer")
            or item.get("title")
            or ""
        )
        if not text:
            continue

        emb = get_embedding(text)

        # Clean metadata
        meta = {}
        for k, v in item.items():
            if k == "embedding" or v is None:
                continue
            if isinstance(v, (str, int, float, bool)):
                meta[k] = v
            elif isinstance(v, list) and all(isinstance(x, str) for x in v):
                meta[k] = ",".join(v)

        batch.append((f"{namespace}-{i}", emb, meta))

        if len(batch) == 100:
            pinecone_index.upsert(batch, namespace=namespace)
            batch = []

    if batch:
        pinecone_index.upsert(batch, namespace=namespace)


def clear_namespace(namespace: str):
    """Delete all vectors in a namespace (fresh start)."""
    print(f"🔁 Clearing namespace '{namespace}' ...")
    pinecone_index.delete(namespace=namespace, delete_all=True)
    print(f"[OK] Namespace '{namespace}' cleared")


if __name__ == "__main__":
    print("=== Pinecone ingestion (Hard Chews) ===")

    kb_items = load_all_kb_items()
    scraping_items = load_scraping_data()

    # 1) fresh clean
    clear_namespace("kb")
    clear_namespace("scraping")

    # 2) upsert KB
    if kb_items:
        print(f"Upserting {len(kb_items)} KB items to namespace 'kb'...")
        upsert_to_pinecone(kb_items, namespace="kb")
    else:
        print("⚠️ No KB items to upsert")

    # 3) upsert scraping
    if scraping_items:
        print(f"Upserting {len(scraping_items)} scraping items to namespace 'scraping'...")
        upsert_to_pinecone(scraping_items, namespace="scraping")
    else:
        print("ℹ️ No scraping items to upsert")

    print("[SUCCESS] Pinecone upsert complete.")
