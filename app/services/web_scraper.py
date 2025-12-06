# File: app/services/web_scraper.py

import requests
import os
from bs4 import BeautifulSoup
import json
import time
from typing import List, Dict, Optional
from app.logger import logger


class WebScraper:
    """
    Scrapes website content for HardChews knowledge base.
    Extracts product info, policies, FAQs from website pages.
    """

    def __init__(self, base_url: str = "https://hardchews.shop"):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.session = requests.Session()

    def _get_page(self, path: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a page."""
        try:
            # Allow passing full URLs (starting with http) or relative paths
            if path.startswith("http://") or path.startswith("https://"):
                url = path
            else:
                url = f"{self.base_url}/{path.lstrip('/')}"
            logger.info(f"Scraping: {url}")
            resp = self.session.get(url, headers=self.headers, timeout=10)
            resp.raise_for_status()
            return BeautifulSoup(resp.content, "html.parser")
        except Exception as e:
            logger.error(f"Error scraping {path}: {e}")
            return None

    def scrape_product_pages(self) -> List[Dict]:
        """Scrape all product pages and extract structured data."""
        products = []
        
        # Try scraping /products, /shop, /products/hardchews etc.
        for product_path in ["products", "shop", "products/hardchews-male-performance"]:
            soup = self._get_page(product_path)
            if not soup:
                continue

            # Extract product title, description, benefits, ingredients
            try:
                # Adjust selectors based on actual website structure
                title_elem = soup.find(["h1", "h2"], class_=["product-title", "title"])
                desc_elem = soup.find(["div", "p"], class_=["product-description", "description"])
                benefits_elem = soup.find(["ul", "div"], class_=["benefits", "features"])
                ingredients_elem = soup.find(["ul", "div"], class_=["ingredients", "composition"])

                if title_elem:
                    product = {
                        "title": title_elem.get_text(strip=True),
                        "description": desc_elem.get_text(strip=True) if desc_elem else "",
                        "benefits": [],
                        "ingredients": [],
                        "source_url": f"{self.base_url}/{product_path}",
                    }

                    if benefits_elem:
                        for li in benefits_elem.find_all("li"):
                            benefit = li.get_text(strip=True)
                            if benefit:
                                product["benefits"].append(benefit)

                    if ingredients_elem:
                        for li in ingredients_elem.find_all("li"):
                            ingredient = li.get_text(strip=True)
                            if ingredient:
                                product["ingredients"].append(ingredient)

                    products.append(product)
                    logger.info(f"Successfully scraped product: {product['title']}")
            except Exception as e:
                logger.warning(f"Error parsing product page: {e}")

            time.sleep(1)  # Rate limiting

        return products

    def scrape_faq_page(self) -> List[Dict]:
        """Scrape FAQ/Help center pages."""
        faqs = []

        for faq_path in ["faq", "help", "support/faqs", "help-center"]:
            soup = self._get_page(faq_path)
            if not soup:
                continue

            try:
                # Look for FAQ items (usually divs or sections with question/answer pairs)
                faq_items = soup.find_all(["div", "section"], class_=["faq-item", "question-answer", "accordion-item"])

                for item in faq_items:
                    question_elem = item.find(["h3", "h4", "span"], class_=["question", "title", "faq-question"])
                    answer_elem = item.find(["div", "p", "span"], class_=["answer", "content", "faq-answer"])

                    if question_elem and answer_elem:
                        faq = {
                            "question": question_elem.get_text(strip=True),
                            "answer": answer_elem.get_text(strip=True),
                            "source_url": f"{self.base_url}/{faq_path}",
                        }
                        faqs.append(faq)
                        logger.info(f"Scraped FAQ: {faq['question'][:50]}...")

            except Exception as e:
                logger.warning(f"Error parsing FAQ page: {e}")

            time.sleep(1)

        return faqs

    def scrape_policy_pages(self) -> List[Dict]:
        """Scrape shipping, refund, privacy, terms pages."""
        policies = []

        policy_paths = {
            "shipping": ["shipping", "shipping-policy", "shipping-info"],
            "refund": ["refund", "refund-policy", "returns"],
            "privacy": ["privacy", "privacy-policy"],
            "terms": ["terms", "terms-of-service", "tos"],
            "contact": ["contact", "contact-us", "support"],
        }

        for policy_type, paths in policy_paths.items():
            for path in paths:
                soup = self._get_page(path)
                if not soup:
                    continue

                try:
                    # Extract main content
                    content_elem = soup.find(["main", "article", "div"], class_=["content", "page-content", "main-content"])
                    if not content_elem:
                        content_elem = soup.find(["div", "section"])

                    if content_elem:
                        text = content_elem.get_text(strip=True)
                        if len(text) > 100:  # Only if substantial content
                            policy = {
                                "type": policy_type,
                                "title": f"{policy_type.title()} Policy",
                                "content": text[:2000],  # First 2000 chars
                                "source_url": f"{self.base_url}/{path}",
                            }
                            policies.append(policy)
                            logger.info(f"Scraped {policy_type} policy from /{path}")
                            break
                except Exception as e:
                    logger.warning(f"Error parsing policy page: {e}")

                time.sleep(1)

        return policies

    def export_scraped_data(self, output_file: str = None):
        """
        Scrape all data and export as JSON for manual review.
        """
        logger.info("Starting comprehensive web scrape...")

        data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "products": self.scrape_product_pages(),
            "faqs": self.scrape_faq_page(),
            "policies": self.scrape_policy_pages(),
        }

        # Default export path used by the ingestion script
        output_file = output_file or "app/kb/cache/scraped_data.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Scraped data exported to {output_file}")
        except Exception as e:
            logger.error(f"Error exporting scraped data: {e}")

        return data


# Utility function for manual scraping
def scrape_hardchews_website(website_url: str = "https://hardchews.shop"):
    """
    Quick function to scrape HardChews website and export data.
    Usage: Call this from management command or CLI.
    """
    scraper = WebScraper(base_url=website_url)
    return scraper.export_scraped_data()

def scrape_urls(urls: List[str], output_file: str = None):
    """
    Scrape an explicit list of full URLs and export data.
    Useful for scraping product pages, clickbank order links, and policy pages.
    """
    scraper = WebScraper()
    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "pages": []
    }

    for url in urls:
        try:
            soup = scraper._get_page(url)
            if not soup:
                continue

            title = soup.title.string.strip() if soup.title else url
            # collect paragraphs and headings
            paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]
            headings = [h.get_text(strip=True) for h in soup.find_all(['h1','h2','h3','h4']) if h.get_text(strip=True)]

            page = {
                "url": url,
                "title": title,
                "headings": headings,
                "paragraphs": paragraphs,
            }
            results["pages"].append(page)
            time.sleep(1)
        except Exception as e:
            logger.warning(f"Failed scraping {url}: {e}")

    output_file = output_file or "app/kb/cache/scraped_data.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    logger.info(f"Scraped {len(results['pages'])} pages and saved to {output_file}")
    return results
