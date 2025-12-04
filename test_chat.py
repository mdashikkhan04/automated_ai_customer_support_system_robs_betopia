#!/usr/bin/env python
"""
Simple test script for HardChews chatbot
Run this while server is running: python test_chat.py
"""

import requests
import json
from time import sleep

BASE_URL = "http://localhost:8000"

# Colors for output
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

def test_health():
    """Test health endpoint"""
    print(f"{GREEN}[STEP 1] Testing Health Endpoint...{RESET}")
    try:
        resp = requests.get(f"{BASE_URL}/health")
        print(f"{GREEN}Status: {resp.status_code}{RESET}")
        print(f"{YELLOW}{json.dumps(resp.json(), indent=2)}{RESET}\n")
        return resp.status_code == 200
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}\n")
        return False

def test_chat(question, expected_tier=1):
    """Test chat endpoint"""
    print(f"{GREEN}[TEST] Question: {question}{RESET}")
    try:
        resp = requests.post(
            f"{BASE_URL}/chat",
            json={"user_message": question},
            timeout=30
        )
        data = resp.json()
        
        print(f"{GREEN}Tier: {data['tier']} | Confidence: {data['confidence']:.2f}{RESET}")
        print(f"{CYAN}Reply:{RESET}\n{data['reply']}\n")
        
        # Print raw response for debugging
        if data['tier'] == 0:
            print(f"{RED}DEBUG - Full Response: {json.dumps(data, indent=2)}{RESET}\n")
        
        return data
    except Exception as e:
        print(f"{RED}Error: {e}{RESET}\n")
        print(f"{RED}DEBUG - Full Exception:{RESET}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print(f"\n{GREEN}{'='*60}")
    print(f"HardChews Chatbot Test Suite")
    print(f"{'='*60}{RESET}\n")
    
    # Test 1: Health check
    if not test_health():
        print(f"{RED}Server is not running! Start it with:{RESET}")
        print(f"{YELLOW}python -m uvicorn app.main:app --host 127.0.0.1 --port 8000{RESET}\n")
        exit(1)
    
    sleep(1)
    
    # Test 2: Refund policy question
    test_chat("What is your refund policy?")
    sleep(1)
    
    # Test 3: Support location question
    test_chat("Where is your support center located?")
    sleep(1)
    
    # Test 4: Shipping question
    test_chat("What is your shipping policy? Do you offer free shipping?")
    sleep(1)
    
    # Test 5: Generic question
    test_chat("Tell me about your company")
    sleep(1)
    
    print(f"{GREEN}{'='*60}")
    print(f"All tests completed!")
    print(f"{'='*60}{RESET}\n")
