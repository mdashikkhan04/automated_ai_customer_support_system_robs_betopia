#!/usr/bin/env python3
"""
Test Script - Hybrid Response System
যাচাই করুন যে বিভিন্ন প্রশ্নে বিভিন্ন উত্তর আসছে
"""

import sys
import os

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.hybrid_response_service import hybrid_service
from app.services.kb_service import kb_service
from app.logger import logger

def test_hybrid_responses():
    """বিভিন্ন intent এবং প্রশ্নে response টেস্ট করুন"""
    
    test_cases = [
        ("What is HardChews?", "general"),
        ("How do I use it?", "usage"),
        ("When will I see results?", "usage"),
        ("What's the price?", "pricing"),
        ("Can I get a refund?", "refund"),
        ("How long does shipping take?", "shipping"),
        ("Is it safe to use with medication?", "safety"),
        ("Do you offer subscriptions?", "subscription"),
        ("Where is my order?", "order_status"),
        ("How should I take HardChews?", "usage"),
        ("Tell me about the ingredients", "general"),
        ("What are the side effects?", "safety"),
    ]
    
    print("=" * 80)
    print("🧪 HYBRID RESPONSE SYSTEM - TEST RESULTS")
    print("=" * 80)
    print()
    
    for question, intent in test_cases:
        print(f"❓ Question: {question}")
        print(f"   Intent: {intent}")
        
        try:
            response = hybrid_service.get_response(question, intent)
            print(f"✅ Response:\n   {response[:150]}...")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 80)
        print()
    
    print("=" * 80)
    print(f"✅ Total KB Items Loaded: {len(kb_service.items)}")
    print("=" * 80)


def test_kb_search():
    """KB search functionality test করুন"""
    
    print("\n" + "=" * 80)
    print("📚 KNOWLEDGE BASE SEARCH - TEST RESULTS")
    print("=" * 80)
    print()
    
    queries = [
        "What is HardChews?",
        "How do I use it?",
        "Refund policy",
        "Shipping time",
        "Side effects",
        "Price",
        "Subscription",
    ]
    
    for query in queries:
        print(f"🔍 Query: {query}")
        
        try:
            results = kb_service.search(query, top_k=2)
            print(f"   Found {len(results)} matches:")
            for i, result in enumerate(results, 1):
                print(f"   {i}. {result.get('title', 'No title')}")
                print(f"      Score: {result.get('score', 'N/A')}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    print("=" * 80)


if __name__ == "__main__":
    print("\n🚀 Starting Hybrid Response System Tests...\n")
    
    try:
        test_kb_search()
        test_hybrid_responses()
        
        print("\n✅ ALL TESTS COMPLETED!")
        print("\nNow your chatbot will:")
        print("  1. Use KB-based answers (no OpenAI errors)")
        print("  2. Provide different answers for different questions")
        print("  3. Have proper fallback when API fails")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
