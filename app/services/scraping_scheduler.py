# File: app/services/scraping_scheduler.py
"""
Background Scheduler for Periodic Web Scraping
Refreshes website data at regular intervals
"""

import asyncio
import threading
from datetime import datetime, timedelta
from typing import Optional

from app.services.enhanced_web_scraper import web_scraper
from app.logger import logger


class ScrapingScheduler:
    """
    Manages background web scraping tasks.
    Periodically refreshes data from website.
    """

    def __init__(self, interval_hours: int = 6):
        """
        Initialize scheduler.
        
        Args:
            interval_hours: How often to refresh scraped data (default: 6 hours)
        """
        self.interval_seconds = interval_hours * 3600
        self.is_running = False
        self.last_scrape_time: Optional[datetime] = None
        self.scheduler_thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Start the background scheduler."""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return
        
        self.is_running = True
        self.scheduler_thread = threading.Thread(
            target=self._scheduler_loop,
            daemon=True,
            name="ScrapingScheduler"
        )
        self.scheduler_thread.start()
        logger.info(f"✅ Scraping scheduler started (interval: {self.interval_seconds//3600}h)")

    def stop(self) -> None:
        """Stop the background scheduler."""
        self.is_running = False
        logger.info("Scraping scheduler stopped")

    def _scheduler_loop(self) -> None:
        """Main scheduler loop (runs in background thread)."""
        while self.is_running:
            try:
                # Calculate time until next scrape
                if self.last_scrape_time:
                    time_since_scrape = (datetime.now() - self.last_scrape_time).total_seconds()
                    time_until_next = self.interval_seconds - time_since_scrape
                    
                    if time_until_next > 0:
                        logger.debug(f"Next scrape in {time_until_next//60:.0f} minutes")
                        # Sleep in small chunks so we can check is_running frequently
                        asyncio.run(asyncio.sleep(min(60, time_until_next)))
                        continue
                
                # Time to scrape
                logger.info("🔄 Scheduled web scraping starting...")
                self.last_scrape_time = datetime.now()
                
                try:
                    data = web_scraper.scrape_all(force_refresh=True)
                    logger.info(f"✅ Scheduled scraping completed: "
                              f"{len(data.get('products', []))} products, "
                              f"{len(data.get('faqs', []))} FAQs, "
                              f"{len(data.get('policies', []))} policies")
                except Exception as e:
                    logger.error(f"Error during scheduled scraping: {e}")
                
                # Small sleep before checking again
                asyncio.run(asyncio.sleep(1))
                
            except Exception as e:
                logger.error(f"Scheduler loop error: {e}")
                asyncio.run(asyncio.sleep(5))

    def get_status(self) -> dict:
        """Get scheduler status."""
        return {
            "is_running": self.is_running,
            "interval_hours": self.interval_seconds // 3600,
            "last_scrape_time": self.last_scrape_time.isoformat() if self.last_scrape_time else None,
            "next_scrape_in_seconds": (
                self.interval_seconds - (datetime.now() - self.last_scrape_time).total_seconds()
                if self.last_scrape_time else self.interval_seconds
            )
        }


# Singleton instance (will be started on app startup)
scraping_scheduler = ScrapingScheduler(interval_hours=6)
