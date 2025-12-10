# scripts/scrape_and_ingest.py
from dotenv import load_dotenv
import os
import time

load_dotenv()

from app.services.web_scraper import scrape_urls
from app.services.pinecone_ingest import upsert_to_pinecone, load_scraping_data

URLS = [
    "https://www.hardchews.me/f/wtgpxj/",
    "https://www.hardchews.me/f/6dbq9s/",
    "https://www.hardchews.me/f/6dbq9s/?bottles=263",
    "https://www.hardchews.help/",
    "https://hardchews.shop/",
    "https://www.hardchews.me/support",
]

def main():
    print("Starting scraping of provided URLs...")
    scraped = scrape_urls(URLS)
    print(f"Scraped {len(scraped.get('pages', []))} pages. Waiting 2s before ingestion...")
    time.sleep(2)

    print("Loading scraping data and upserting to Pinecone...")
    scraping_items = load_scraping_data()
    print(f"Loaded {len(scraping_items)} scraping items")
    if scraping_items:
        upsert_to_pinecone(scraping_items, namespace="scraping")
        print("Upsert complete.")
    else:
        print("No scraping items found to upsert.")


if __name__ == "__main__":
    main()
