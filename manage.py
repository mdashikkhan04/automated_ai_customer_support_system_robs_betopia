#!/usr/bin/env python
# File: manage.py
"""
Management script for HardChews AI Chatbot.
Usage: python manage.py [command]
"""

import sys
import json
import os
from datetime import datetime


def scrape_website():
    """Scrape hardchews.shop for KB data."""
    from app.services.web_scraper import scrape_hardchews_website
    print("🕷️  Starting website scrape...")
    data = scrape_hardchews_website("https://hardchews.shop")
    print(f"✅ Scraped {len(data['products'])} products, {len(data['faqs'])} FAQs, {len(data['policies'])} policies")
    print(f"📁 Data saved to: app/kb/data/scraped_website_data.json")


def test_kb():
    """Test knowledge base loading and embedding."""
    from app.services.kb_service import kb_service
    print("📚 Testing Knowledge Base...")
    print(f"✅ Loaded {len(kb_service.items)} KB items")
    print(f"✅ Generated embeddings for {len(kb_service.embeddings)} items")
    
    # Test search
    results = kb_service.search("What is HardChews?", top_k=3)
    print(f"✅ Search works! Found {len(results)} results for sample query")


def test_openai():
    """Test OpenAI connection."""
    from app.config import get_settings
    import openai
    settings = get_settings()
    
    if not settings.OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY not set in .env")
        return
    
    print("🔌 Testing OpenAI connection...")
    try:
        openai.api_key = settings.OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'Hello from HardChews'"}],
            max_tokens=20
        )
        print(f"✅ OpenAI connected! Response: {response['choices'][0]['message']['content']}")
    except Exception as e:
        print(f"❌ Error: {e}")


def cleanup_conversations(days: int = 1):
    """Clean up old conversations."""
    from app.services.conversation_manager import get_conversation_manager
    manager = get_conversation_manager()
    count = manager.cleanup_expired(hours=days*24)
    print(f"🧹 Cleaned up {count} conversations older than {days} day(s)")


def load_sample_data():
    """Load sample test data."""
    print("📝 Loading sample test data...")
    sample_convs = [
        ("Hello!", "greeting"),
        ("What is HardChews?", "product_info"),
        ("How much does it cost?", "pricing"),
        ("Where is my order?", "order_status"),
        ("I want a refund", "refund"),
    ]
    
    for i, (msg, intent) in enumerate(sample_convs, 1):
        print(f"  {i}. {msg}")
    
    print(f"✅ {len(sample_convs)} sample conversations ready for testing")


def health_check():
    """Check if all systems are operational."""
    print("🏥 Performing system health check...\n")
    
    checks = []
    
    # Check .env
    if os.path.exists(".env"):
        print("✅ .env file found")
        checks.append(True)
    else:
        print("❌ .env file NOT found - Copy .env.example to .env")
        checks.append(False)
    
    # Check OpenAI key
    from app.config import get_settings
    settings = get_settings()
    if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.startswith("sk-"):
        print("✅ OpenAI API key configured")
        checks.append(True)
    else:
        print("❌ OpenAI API key NOT configured - Add OPENAI_API_KEY to .env")
        checks.append(False)
    
    # Check KB files
    kb_files = ["app/kb/data/faqs_comprehensive.json", "app/kb/data/products_comprehensive.json"]
    kb_exists = all(os.path.exists(f) for f in kb_files)
    if kb_exists:
        print(f"✅ KB files found ({len(kb_files)} files)")
        checks.append(True)
    else:
        print(f"❌ KB files NOT found")
        checks.append(False)
    
    # Check requirements
    try:
        import fastapi
        import openai
        import pydantic
        print("✅ All required packages installed")
        checks.append(True)
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        checks.append(False)
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Health Check: {sum(checks)}/{len(checks)} systems operational")
    if all(checks):
        print("🟢 All systems GO! Ready to run: uvicorn app.main:app --reload")
    else:
        print("🔴 Some issues detected. Fix above errors before starting.")
    print(f"{'='*50}\n")


def help_command():
    """Show available commands."""
    print("""
HardChews AI Chatbot - Management Commands

Usage: python manage.py [command]

Available Commands:

  help              Show this help message
  health            Perform system health check
  test-kb           Test knowledge base loading
  test-openai       Test OpenAI API connection
  scrape-website    Scrape hardchews.shop for KB data
  cleanup-convs     Clean up old conversations
  load-samples      Show sample test conversations

Examples:

  python manage.py health              # Check if everything is set up
  python manage.py test-openai         # Verify OpenAI connection
  python manage.py scrape-website      # Update KB from website

Run 'uvicorn app.main:app --reload' to start the bot.
Run 'python app/tests/test_conversations.py' to run full test suite.
    """.strip())


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        help_command()
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        "help": help_command,
        "health": health_check,
        "test-kb": test_kb,
        "test-openai": test_openai,
        "scrape-website": scrape_website,
        "cleanup-convs": lambda: cleanup_conversations(int(sys.argv[2]) if len(sys.argv) > 2 else 1),
        "load-samples": load_sample_data,
    }
    
    if command in commands:
        try:
            commands[command]()
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"❌ Unknown command: {command}")
        print(f"Run 'python manage.py help' for available commands")


if __name__ == "__main__":
    main()
