#!/usr/bin/env python3
"""
⚡ Speed Optimization Test
Test the new quick response system
"""

import time
import asyncio
from app.services.priority_response_service import priority_service

# Sample test queries
TEST_QUERIES = [
    "What is HardChews?",
    "How should I take it?",
    "Tell me about your products",
    "What's the price?",
    "How do I order?",
    "Do you have refunds?",
    "What are the benefits?",
]

def benchmark_response(query: str, num_runs: int = 3) -> dict:
    """Benchmark a single query"""
    times = []
    results = []
    
    for i in range(num_runs):
        start = time.time()
        result = priority_service.get_response(
            user_message=query,
            intent="general",
            quick_mode=True
        )
        elapsed = time.time() - start
        times.append(elapsed)
        results.append(result)
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    return {
        "query": query,
        "avg_time_ms": avg_time * 1000,
        "min_time_ms": min_time * 1000,
        "max_time_ms": max_time * 1000,
        "source": results[0].get("source"),
        "confidence": results[0].get("confidence"),
    }

def main():
    print("\n" + "="*70)
    print("⚡ SPEED OPTIMIZATION TEST - Quick Response System")
    print("="*70 + "\n")
    
    print("Testing responses with QUICK MODE enabled...\n")
    
    results = []
    total_time = 0
    
    for query in TEST_QUERIES:
        print(f"🧪 Testing: {query}")
        result = benchmark_response(query, num_runs=3)
        results.append(result)
        total_time += result["avg_time_ms"]
        
        source_icon = {"dataset": "📚", "scraping": "🌐", "llm": "🤖"}.get(result["source"], "?")
        print(f"   {source_icon} Source: {result['source']}")
        print(f"   ⏱️  Avg: {result['avg_time_ms']:.0f}ms | Min: {result['min_time_ms']:.0f}ms | Max: {result['max_time_ms']:.0f}ms")
        print(f"   📊 Confidence: {result['confidence']:.2f}\n")
    
    # Summary
    print("\n" + "="*70)
    print("📊 SUMMARY")
    print("="*70 + "\n")
    
    avg_response_time = total_time / len(TEST_QUERIES)
    
    print(f"Total queries tested: {len(TEST_QUERIES)}")
    print(f"Average response time: {avg_response_time:.0f}ms")
    print(f"Total time: {total_time:.0f}ms\n")
    
    # Breakdown by source
    by_source = {}
    for result in results:
        source = result["source"]
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(result["avg_time_ms"])
    
    print("📈 Breakdown by source:\n")
    for source, times in by_source.items():
        source_icon = {"dataset": "📚", "scraping": "🌐", "llm": "🤖"}.get(source, "?")
        avg = sum(times) / len(times)
        count = len(times)
        print(f"  {source_icon} {source.upper()}: {avg:.0f}ms avg ({count} queries)")
    
    print("\n✨ Quick mode features activated:")
    print("  ✅ Keyword-based search (no OpenAI API calls)")
    print("  ✅ Fast KB lookup (50-100ms typical)")
    print("  ✅ Skip LLM if moderate confidence in Tier 2")
    print("  ✅ Return early on high confidence matches")
    
    if avg_response_time < 500:
        print(f"\n🚀 EXCELLENT! Average response time: {avg_response_time:.0f}ms (< 500ms) ✅")
    elif avg_response_time < 1000:
        print(f"\n✅ GOOD! Average response time: {avg_response_time:.0f}ms (< 1000ms)")
    else:
        print(f"\n⚠️  Response time: {avg_response_time:.0f}ms - Still optimizing...")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
