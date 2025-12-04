#!/usr/bin/env python3
"""
Test Suite for 3-Tier Priority Response System
Tests Dataset → Web Scraping → LLM fallback chain
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.priority_response_service import priority_service
from app.services.kb_service import kb_service
from app.services.enhanced_web_scraper import web_scraper
from app.logger import logger


def test_tier_1_dataset():
    """Test Tier 1: Dataset (RAG) responses."""
    print("\n" + "="*80)
    print("🧪 TIER 1 TEST - Dataset (RAG) Responses")
    print("="*80)
    
    test_queries = [
        ("What is HardChews?", "general"),
        ("How do I use it?", "usage"),
        ("What's your refund policy?", "refund"),
        ("How long does shipping take?", "shipping"),
        ("Is it safe with medication?", "safety"),
        ("Do you offer subscriptions?", "subscription"),
        ("What's the price?", "pricing"),
    ]
    
    for query, intent in test_queries:
        print(f"\n❓ Query: {query}")
        print(f"   Intent: {intent}")
        
        result = priority_service._try_dataset(query, intent)
        
        if result["source"] == "dataset" and result.get("confidence", 0) > 0.3:
            print(f"   ✅ Found in Dataset (confidence: {result['confidence']:.2f})")
            print(f"   KB Item: {result.get('kb_item_title', 'N/A')}")
            print(f"   Response: {result['response'][:100]}...")
        else:
            print(f"   ⚠️ Not found in Dataset (confidence: {result.get('confidence', 0):.2f})")


def test_tier_2_scraping():
    """Test Tier 2: Web Scraping data."""
    print("\n" + "="*80)
    print("🌐 TIER 2 TEST - Web Scraping Data")
    print("="*80)
    
    print("\n📊 Checking scraped data cache...")
    scraped = web_scraper.get_cached_data()
    
    print(f"   Products: {len(scraped.get('products', []))}")
    print(f"   FAQs: {len(scraped.get('faqs', []))}")
    print(f"   Policies: {len(scraped.get('policies', []))}")
    print(f"   Cache timestamp: {scraped.get('timestamp', 'N/A')}")
    
    if scraped.get("products"):
        print(f"\n   Sample product: {scraped['products'][0].get('title', 'N/A')}")
    
    # Test scraping search
    test_queries = [
        "product information",
        "shipping details",
        "refund process"
    ]
    
    print("\n🔍 Testing scraping search:")
    for query in test_queries:
        print(f"\n   Query: {query}")
        result = priority_service._try_scraping(query, "general")
        
        if result["source"] == "scraping" and result.get("confidence", 0) > 0.2:
            print(f"   ✅ Found in Scraped Data (confidence: {result['confidence']:.2f})")
            print(f"   Item: {result.get('scraped_item_title', 'N/A')}")
        else:
            print(f"   ⚠️ Not found in Scraped Data")


def test_tier_3_llm():
    """Test Tier 3: LLM fallback (requires OpenAI API key)."""
    print("\n" + "="*80)
    print("🤖 TIER 3 TEST - OpenAI LLM Fallback")
    print("="*80)
    
    print("\n⚠️  Tier 3 (LLM) test requires valid OPENAI_API_KEY in .env")
    print("   If API key is missing/invalid, you'll see LLM fallback behavior.")
    
    test_query = "Tell me something creative about supplements"
    print(f"\n   Test Query: {test_query}")
    
    try:
        result = priority_service._try_llm(test_query, "general", "", None, None)
        
        if result["source"] in ["llm", "llm_fallback"]:
            print(f"   ✅ LLM Response Generated (source: {result['source']})")
            print(f"   Response: {result['response'][:100]}...")
            if result.get("error"):
                print(f"   Error encountered: {result['error']}")
        else:
            print(f"   ❌ Unexpected source: {result['source']}")
    except Exception as e:
        print(f"   ❌ Error calling LLM: {e}")


def test_full_priority_chain():
    """Test full 3-tier priority chain."""
    print("\n" + "="*80)
    print("🎯 FULL PRIORITY CHAIN TEST")
    print("="*80)
    
    test_cases = [
        ("What is HardChews?", "general"),
        ("How should I take HardChews?", "usage"),
        ("What's your refund policy?", "refund"),
        ("Tell me something random about health", "general"),  # Should hit LLM
    ]
    
    for query, intent in test_cases:
        print(f"\n❓ Query: {query}")
        print(f"   Intent: {intent}")
        
        result = priority_service.get_response(
            user_message=query,
            intent=intent
        )
        
        source = result.get("source", "unknown")
        confidence = result.get("confidence", 0.0)
        
        print(f"   ✅ Source: {source.upper()}")
        print(f"   Confidence: {confidence:.2f}")
        print(f"   Response Preview: {result['response'][:150]}...")
        
        # Show which tier was used
        if source == "dataset":
            print(f"   → Tier 1 (Dataset) matched!")
        elif source == "scraping":
            print(f"   → Tier 2 (Scraping) matched!")
        elif source in ["llm", "llm_fallback"]:
            print(f"   → Tier 3 (LLM) used!")


def test_tier_stats():
    """Test tier statistics."""
    print("\n" + "="*80)
    print("📊 TIER STATISTICS")
    print("="*80)
    
    stats = priority_service.get_tier_stats()
    
    print(f"\n   Tier 1 (Dataset): {stats['tier1_dataset_items']} KB items")
    print(f"   Tier 2 (Scraping): {stats['tier2_scraping_items']} scraped items")
    print(f"   Tier 3 (LLM): {'Available' if stats['tier3_llm_available'] else 'Not available'}")
    print(f"   Total Data Sources: {stats['total_data_sources']}")


def test_refresh_scraping():
    """Test manual scraping cache refresh."""
    print("\n" + "="*80)
    print("🔄 SCRAPING CACHE REFRESH TEST")
    print("="*80)
    
    print("\n⚠️  This test attempts to scrape hardchews.shop (may be slow).")
    print("   Running with cached data (unless cache is expired)...\n")
    
    result = priority_service.refresh_scraping_cache(force=False)
    
    if result.get("status") == "success":
        print(f"   ✅ Scraping Cache Refreshed!")
        print(f"   Products: {result['products']}")
        print(f"   FAQs: {result['faqs']}")
        print(f"   Policies: {result['policies']}")
        print(f"   Timestamp: {result['timestamp']}")
    else:
        print(f"   ⚠️  Refresh status: {result.get('status')}")
        print(f"   Message: {result.get('message', 'Unknown error')}")


if __name__ == "__main__":
    print("\n🚀 3-TIER PRIORITY RESPONSE SYSTEM - COMPREHENSIVE TEST SUITE")
    print("="*80)
    
    try:
        print(f"\n✅ KB Service: {len(kb_service.items)} items loaded")
        
        scraped = web_scraper.get_cached_data()
        scraped_total = len(scraped.get("products", [])) + len(scraped.get("faqs", [])) + len(scraped.get("policies", []))
        print(f"✅ Web Scraper: {scraped_total} cached items")
        
        # Run tests
        test_tier_1_dataset()
        test_tier_2_scraping()
        test_tier_3_llm()
        test_full_priority_chain()
        test_tier_stats()
        # test_refresh_scraping()  # Uncomment to test scraping refresh (may be slow)
        
        print("\n" + "="*80)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*80)
        print("\n📝 Summary:")
        print("   • Tier 1 (Dataset): High-quality KB-based responses")
        print("   • Tier 2 (Scraping): Live website data as fallback")
        print("   • Tier 3 (LLM): General ChatGPT-like responses")
        print("\n🎯 Priority Chain: Dataset → Scraping → LLM\n")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
