"""Simple script to verify Chatwoot integration.

Usage (PowerShell):
  $env:PYTHONPATH="."
  python .\scripts\test_chatwoot_integration.py

Or create a `.env` file with those variables and run from the repo root.
"""

import os
from dotenv import load_dotenv

load_dotenv()

from app.services.chatwoot_service import chatwoot_client


def main():
    if not chatwoot_client.enabled:
        print(
            "Chatwoot client not configured.\n"
            "Please set CHATWOOT_API_TOKEN (or CHATWOOT_API_KEY as fallback) "
            "and CHATWOOT_ACCOUNT_ID in .env or environment."
        )
        return

    # Optional overrides for testing
    test_email = os.environ.get("TEST_CHATWOOT_EMAIL", "test+local@example.com")
    test_name = os.environ.get("TEST_CHATWOOT_NAME", "Local Integration Test")
    test_msg = os.environ.get(
        "TEST_CHATWOOT_MESSAGE",
        "Automated test: please log this conversation from local project."
    )

    try:
        print("Sending test conversation to Chatwoot...")
        resp = chatwoot_client.create_conversation(
            contact_email=test_email,
            contact_name=test_name,
            message=test_msg,
        )

        conv_id = None
        if isinstance(resp, dict):
            conv_id = resp.get("id") or resp.get("meta", {}).get("conversation_id")

        print("Chatwoot response (truncated):")
        if conv_id:
            print(f"  ✅ Conversation created successfully. ID: {conv_id}")
        else:
            print(resp)

        print(
            "✅ Done — check Chatwoot dashboard → Conversations "
            "and search for test+local@example.com"
        )

    except Exception as e:
        print("❌ Error while sending test to Chatwoot:", repr(e))
        print("If this is an auth error, re-check CHATWOOT_API_TOKEN and CHATWOOT_ACCOUNT_ID.")
        print("If this is a connection error, it may be a local firewall/ISP issue.")


if __name__ == "__main__":
    main()
