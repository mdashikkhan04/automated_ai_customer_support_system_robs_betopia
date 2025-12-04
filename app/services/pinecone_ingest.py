"""
Push KB & scraping data to Pinecone index
"""
import os
import sys
import json
from dotenv import load_dotenv

# Fix Python path for direct script execution
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Load .env FIRST before importing services that need it
load_dotenv()

from app.services.pinecone_client import pinecone_index
from app.services.openai_service import get_embedding

KB_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kb", "data")

# Helper: Load all KB & scraping data

def load_all_kb_items():
    items = []
    for filename in ["complete_kb.json", "faqs_comprehensive.json", "products_comprehensive.json", "faqs.json", "products.json"]:
        path = os.path.join(KB_DATA_DIR, filename)
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            items.extend(data)
    return items

def load_scraping_data():
    scraping_path = os.path.join(os.path.dirname(KB_DATA_DIR), "cache", "scraped_data.json")
    if not os.path.exists(scraping_path):
        return []
    with open(scraping_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = []
    for section in ["products", "faqs", "policies"]:
        for entry in data.get(section, []):
            items.append(entry)
    return items

def upsert_to_pinecone(items, namespace="kb"):
    batch = []
    for i, item in enumerate(items):
        text = item.get("content") or item.get("answer") or item.get("title") or ""
        if not text:
            continue
        emb = get_embedding(text)
        # Filter metadata: only allow strings, numbers, booleans, and lists of strings
        # Skip complex objects, null values, and nested dicts/lists
        meta = {}
        for k, v in item.items():
            if k == "embedding" or v is None:
                continue
            if isinstance(v, (str, int, float, bool)):
                meta[k] = v
            elif isinstance(v, list) and all(isinstance(x, str) for x in v):
                # Convert list of strings to comma-separated string for metadata
                meta[k] = ",".join(v)
        batch.append((f"{namespace}-{i}", emb, meta))
        if len(batch) == 100:
            pinecone_index.upsert(batch, namespace=namespace)
            batch = []
    if batch:
        pinecone_index.upsert(batch, namespace=namespace)

if __name__ == "__main__":
    print("Loading KB items...")
    kb_items = load_all_kb_items()
    print(f"Loaded {len(kb_items)} KB items")
    print("Loading scraping data...")
    scraping_items = load_scraping_data()
    print(f"Loaded {len(scraping_items)} scraping items")
    print("Upserting KB to Pinecone...")
    upsert_to_pinecone(kb_items, namespace="kb")
    print("Upserting scraping data to Pinecone...")
    upsert_to_pinecone(scraping_items, namespace="scraping")
    print("[SUCCESS] Pinecone upsert complete!")
    print(f"Indexed {len(kb_items)} KB items + {len(scraping_items)} scraping items")
