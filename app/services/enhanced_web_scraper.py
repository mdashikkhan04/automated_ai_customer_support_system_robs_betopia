# File: app/services/enhanced_web_scraper.py
"""
Enhanced Web Scraper Service with Caching & Scheduling
Fetches live product, policy, and FAQ data from hardchews.shop
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import time

import requests
from bs4 import BeautifulSoup

from app.logger import logger

# Cache configuration
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

SCRAPED_DATA_CACHE = os.path.join(CACHE_DIR, "scraped_data.json")
CACHE_TTL = 24 * 60 * 60  # 24 hours in seconds


class EnhancedWebScraper:
    """
    Scrapes live data from website, caches locally, and updates periodically.
    Prevents duplicate scrapes and provides fallback to cached data.
    """

    def __init__(self, base_url: str = "https://www.hardchews.me"):
        self.base_url = base_url
        self.support_url = "https://www.hardchews.me/hc-support"
        self.faq_url = "https://www.hardchews.me/hc-support/faq"
        self.shipping_url = "https://www.hardchews.me/hc-support/shipping"
        self.cache_file = SCRAPED_DATA_CACHE
        self.cache_ttl = CACHE_TTL
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.scraped_data = self._load_cache()

    def _load_cache(self) -> Dict[str, Any]:
        """Load cached data from disk, if valid and not expired."""
        if not os.path.exists(self.cache_file):
            logger.info("No scraping cache found, starting fresh")
            return {"products": [], "faqs": [], "policies": [], "timestamp": None}

        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                cached = json.load(f)
            
            # Check if cache is expired
            if cached.get("timestamp"):
                cached_time = datetime.fromisoformat(cached["timestamp"])
                age = (datetime.now() - cached_time).total_seconds()
                if age < self.cache_ttl:
                    logger.info(f"✅ Loaded cached scraped data (age: {int(age/60)} min)")
                    return cached
                else:
                    logger.info(f"Cache expired ({int(age/3600)}h old), will refresh on next scrape")
            
            return cached
        except Exception as e:
            logger.warning(f"Could not load cache: {e}, starting fresh")
            return {"products": [], "faqs": [], "policies": [], "timestamp": None}

    def _save_cache(self, data: Dict[str, Any]) -> None:
        """Save scraped data to disk cache."""
        try:
            data["timestamp"] = datetime.now().isoformat()
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"✅ Cached scraped data ({len(data.get('products', []))} products, "
                       f"{len(data.get('faqs', []))} FAQs, {len(data.get('policies', []))} policies)")
        except Exception as e:
            logger.error(f"Failed to save cache: {e}")

    def scrape_products(self) -> List[Dict[str, Any]]:
        """Scrape product listings from /products or /shop endpoint."""
        try:
            logger.info("🔍 Scraping products from website...")
            url = f"{self.base_url}/products"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            products = []
            
            # Generic selectors (customize based on actual site structure)
            product_items = soup.find_all("div", class_=["product-card", "product-item"])
            
            for item in product_items:
                try:
                    title_elem = item.find(["h2", "h3", "a"], class_=["product-title", "product-name"])
                    desc_elem = item.find(["p", "div"], class_=["product-description", "product-desc"])
                    price_elem = item.find(["span", "div"], class_=["price", "product-price"])
                    
                    if title_elem:
                        product = {
                            "id": f"scraped_prod_{len(products) + 1}",
                            "type": "product",
                            "title": title_elem.get_text(strip=True),
                            "content": desc_elem.get_text(strip=True) if desc_elem else "No description",
                            "price": price_elem.get_text(strip=True) if price_elem else "Contact for price",
                            "source": "web_scrape",
                            "scraped_at": datetime.now().isoformat(),
                            "tags": ["product", "scraped"]
                        }
                        products.append(product)
                except Exception as e:
                    logger.warning(f"Error parsing product item: {e}")
                    continue
            
            logger.info(f"✅ Scraped {len(products)} products")
            return products
        except Exception as e:
            logger.error(f"Error scraping products: {e}")
            return self.scraped_data.get("products", [])

    def scrape_faqs(self) -> List[Dict[str, Any]]:
        """Scrape FAQ section from /faq or /support endpoint."""
        try:
            logger.info("🔍 Scraping FAQs from website...")
            url = f"{self.base_url}/faq"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            faqs = []
            
            # Generic selectors (customize based on actual site structure)
            faq_items = soup.find_all(["div", "li"], class_=["faq-item", "faq-question", "accordion-item"])
            
            for item in faq_items:
                try:
                    q_elem = item.find(["h3", "h4", "button", "a"], class_=["question", "faq-question", "faq-title"])
                    a_elem = item.find(["p", "div"], class_=["answer", "faq-answer", "faq-content"])
                    
                    if q_elem and a_elem:
                        faq = {
                            "id": f"scraped_faq_{len(faqs) + 1}",
                            "type": "faq",
                            "title": q_elem.get_text(strip=True),
                            "question": q_elem.get_text(strip=True),
                            "content": a_elem.get_text(strip=True),
                            "source": "web_scrape",
                            "scraped_at": datetime.now().isoformat(),
                            "tags": ["faq", "scraped"]
                        }
                        faqs.append(faq)
                except Exception as e:
                    logger.warning(f"Error parsing FAQ item: {e}")
                    continue
            
            logger.info(f"✅ Scraped {len(faqs)} FAQs")
            return faqs
        except Exception as e:
            logger.error(f"Error scraping FAQs: {e}")
            return self.scraped_data.get("faqs", [])

    def scrape_policies(self) -> List[Dict[str, Any]]:
        """Scrape policies from /about, /policies, /shipping, /returns endpoints."""
        try:
            logger.info("🔍 Scraping policies from website...")
            policies = []
            
            policy_urls = {
                "shipping": f"{self.base_url}/shipping",
                "returns": f"{self.base_url}/returns",
                "refund": f"{self.base_url}/refund",
                "about": f"{self.base_url}/about"
            }
            
            for policy_type, url in policy_urls.items():
                try:
                    response = requests.get(url, headers=self.headers, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, "html.parser")
                    
                    # Find main content
                    content_elem = soup.find(["main", "article", "div"], class_=["content", "page-content", "main-content"])
                    if not content_elem:
                        content_elem = soup.find(["body"])
                    
                    if content_elem:
                        content_text = content_elem.get_text(strip=True)[:1000]  # First 1000 chars
                        
                        policy = {
                            "id": f"scraped_policy_{policy_type}",
                            "type": "policy",
                            "title": f"{policy_type.title()} Policy",
                            "content": content_text,
                            "source": "web_scrape",
                            "scraped_at": datetime.now().isoformat(),
                            "tags": ["policy", policy_type, "scraped"]
                        }
                        policies.append(policy)
                        logger.info(f"  ✓ Scraped {policy_type} policy")
                except Exception as e:
                    logger.warning(f"Could not scrape {policy_type} policy: {e}")
            
            logger.info(f"✅ Scraped {len(policies)} policies")
            return policies
        except Exception as e:
            logger.error(f"Error scraping policies: {e}")
            return self.scraped_data.get("policies", [])

    def scrape_all(self, force_refresh: bool = False) -> Dict[str, List[Dict[str, Any]]]:
        """
        Scrape all data (products, FAQs, policies).
        If cache is fresh and not forced, return cached data.
        """
        # Check cache validity
        if not force_refresh and self.scraped_data.get("timestamp"):
            cached_time = datetime.fromisoformat(self.scraped_data["timestamp"])
            age = (datetime.now() - cached_time).total_seconds()
            if age < self.cache_ttl:
                logger.info("✅ Using cached scraped data (cache still fresh)")
                return self.scraped_data
        
        logger.info("🔄 Refreshing scraped data...")
        products = self.scrape_products()
        faqs = self.scrape_faqs()
        policies = self.scrape_policies()
        
        # Update in-memory cache
        self.scraped_data = {
            "products": products,
            "faqs": faqs,
            "policies": policies,
            "timestamp": datetime.now().isoformat()
        }
        
        # Persist to disk
        self._save_cache(self.scraped_data)
        
        return self.scraped_data

    def get_cached_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Return currently cached scraped data (no network call)."""
        return self.scraped_data

    def clear_cache(self) -> None:
        """Clear the scraped data cache."""
        try:
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)
            self.scraped_data = {"products": [], "faqs": [], "policies": [], "timestamp": None}
            logger.info("✅ Cleared scraped data cache")
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")


# Singleton instance
web_scraper = EnhancedWebScraper()
