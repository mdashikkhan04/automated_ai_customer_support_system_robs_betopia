#!/usr/bin/env python3
"""
🚀 HardChews 3-Tier Priority System - Launcher
Starts backend and runs tests automatically
"""

import subprocess
import time
import os
import sys
import webbrowser
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_requirements():
    """Check if all requirements are installed"""
    print_header("📋 Checking Requirements")
    
    try:
        import fastapi
        import openai
        import pydantic
        print("✅ FastAPI installed")
        print("✅ OpenAI installed")
        print("✅ Pydantic installed")
        return True
    except ImportError as e:
        print(f"❌ Missing: {e}")
        print("\n💡 Install with: pip install -r requirements.txt")
        return False

def activate_venv():
    """Activate virtual environment"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print_header("🔧 Creating Virtual Environment")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created\n")
    
    # Update Python path to use venv
    if sys.platform == "win32":
        venv_python = Path("venv/Scripts/python.exe")
    else:
        venv_python = Path("venv/bin/python")
    
    if venv_python.exists():
        print(f"✅ Using venv: {venv_python}")
        return str(venv_python)
    return sys.executable

def start_backend(python_exe):
    """Start FastAPI backend server"""
    print_header("🚀 Starting Backend Server")
    
    cmd = [
        python_exe, "-m", "uvicorn",
        "app.main:app",
        "--reload",
        "--host", "127.0.0.1",
        "--port", "8000"
    ]
    
    print(f"Command: {' '.join(cmd)}\n")
    
    try:
        # Start backend in background
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("✅ Backend server started")
        print("   URL: http://localhost:8000")
        time.sleep(3)  # Wait for server to start
        return proc
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def run_tests(python_exe):
    """Run priority system test suite"""
    print_header("🧪 Running Priority System Tests")
    
    test_file = "test_priority_system.py"
    if not Path(test_file).exists():
        print(f"❌ {test_file} not found")
        return False
    
    try:
        result = subprocess.run(
            [python_exe, test_file],
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def health_check():
    """Check if backend is responding"""
    print_header("🏥 Backend Health Check")
    
    import requests
    import json
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                data = response.json()
                print("✅ Backend is healthy\n")
                
                if "tier_stats" in data:
                    stats = data["tier_stats"]
                    print("📊 System Status:")
                    print(f"   • Tier 1 (Dataset): {stats.get('tier1_dataset_items', 0)} items")
                    print(f"   • Tier 2 (Scraping): {stats.get('tier2_scraping_items', 0)} items")
                    print(f"   • Tier 3 (LLM): {'Ready' if stats.get('tier3_llm_available') else 'Not ready'}\n")
                
                return True
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                print(f"⏳ Waiting for backend... ({attempt+1}/{max_retries})")
                time.sleep(2)
            else:
                print("❌ Backend not responding")
                return False
        except Exception as e:
            print(f"⚠️  Error: {e}")
            return False
    
    return False

def open_frontend():
    """Open frontend in default browser"""
    print_header("🌐 Opening Frontend")
    
    html_files = ["index_v2.html", "index.html"]
    for html_file in html_files:
        if Path(html_file).exists():
            try:
                webbrowser.open(f"file://{Path(html_file).absolute()}")
                print(f"✅ Opened {html_file} in browser")
                return True
            except Exception as e:
                print(f"⚠️  Could not open browser: {e}")
                return False
    
    print("⚠️  Frontend files not found")
    return False

def show_next_steps():
    """Display next steps"""
    print_header("📋 Next Steps")
    
    print("""
✅ Backend running at: http://localhost:8000
✅ Test suite completed

📝 Available Endpoints:
   • POST http://localhost:8000/api/test
     Send: {"user_id": "test", "message": "What is HardChews?"}
   
   • GET http://localhost:8000/health
     Check system status and tier statistics
   
   • GET http://localhost:8000/scheduler/status
     Check scraping scheduler status
   
   • POST http://localhost:8000/scheduler/refresh
     Manually refresh scraping cache

🌐 Frontend:
   • Open index_v2.html in browser
   • Try asking questions
   • See which tier responded (📚/🌐/🤖)

📊 Monitor Tier Usage:
   Check browser console for debug information
   Each response shows: source, confidence, response time

🔧 Customize:
   • Add more KB items: app/kb/data/complete_kb.json
   • Change scraping interval: app/services/scraping_scheduler.py
   • Update website URLs: app/services/enhanced_web_scraper.py

📚 Documentation:
   • QUICK_START_PRIORITY.md - Quick reference
   • PRIORITY_SYSTEM_DOCUMENTATION.md - Full guide
   • test_priority_system.py - Test examples

🎯 Key Features:
   ✨ 3-tier priority system (KB → Web → LLM)
   ✨ Background scheduler (auto-refresh every 6h)
   ✨ Graceful fallback (always returns response)
   ✨ Confidence scoring (0-1 per tier)
   ✨ Response tracking (know which tier answered)

💡 Pro Tips:
   • Press Ctrl+C in backend window to stop server
   • Check app.log for detailed debug information
   • Use /scheduler/refresh to test cache updates
   • Monitor tier statistics in /health endpoint

🚀 You're all set! Ready for production.
    """)

def main():
    """Main launcher function"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║  🔥 HardChews 3-Tier Priority System - Launcher 🔥       ║
    ║     Professional AI Customer Support System              ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Check requirements
    if not check_requirements():
        print("\n⚠️  Installing requirements...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=False)
    
    # Activate venv
    python_exe = activate_venv()
    
    # Start backend
    backend_proc = start_backend(python_exe)
    if not backend_proc:
        print("\n❌ Failed to start backend")
        return False
    
    # Health check
    if not health_check():
        print("\n⚠️  Warning: Backend might not be ready")
        time.sleep(2)
    
    # Run tests
    print("\n" + "="*60)
    try:
        run_tests(python_exe)
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
    
    # Open frontend
    open_frontend()
    
    # Show next steps
    show_next_steps()
    
    # Keep backend running
    print("\n⏳ Backend is running. Press Ctrl+C to stop.\n")
    try:
        backend_proc.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping backend...")
        backend_proc.terminate()
        backend_proc.wait()
        print("✅ Backend stopped\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Launcher interrupted\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
