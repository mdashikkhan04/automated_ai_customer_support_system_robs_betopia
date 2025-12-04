"""
Pinecone vector DB client utility
Usage:
    from app.services.pinecone_client import pinecone_index
    pinecone_index.upsert(...)
    pinecone_index.query(...)
"""
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Load .env file
load_dotenv()

def get_pinecone_config():
    return {
        "api_key": os.getenv("PINECONE_API_KEY"),
        "index_name": os.getenv("PINECONE_INDEX", "hardchews-support-index"),
        "dimension": int(os.getenv("PINECONE_DIM", "1536")),  # OpenAI embedding dim
        "metric": os.getenv("PINECONE_METRIC", "cosine")
    }

def ensure_pinecone_index():
    cfg = get_pinecone_config()
    pc = Pinecone(api_key=cfg["api_key"])
    
    # Create index if it doesn't exist
    if cfg["index_name"] not in pc.list_indexes().names():
        pc.create_index(
            name=cfg["index_name"],
            dimension=cfg["dimension"],
            metric=cfg["metric"],
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
    return pc.Index(cfg["index_name"])

# Main Pinecone index object for all usage
pinecone_index = ensure_pinecone_index()
