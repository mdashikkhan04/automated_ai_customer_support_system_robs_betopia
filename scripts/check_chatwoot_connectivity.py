"""Check Chatwoot connectivity and optionally send a test conversation.

This script does:
 - Loads `.env`
 - Performs a GET to `/api/v1/accounts/{ACCOUNT_ID}` to validate connectivity + auth
 - If GET succeeds, optionally creates a test conversation

Run (PowerShell example):
  $env:PYTHONPATH = "."; python .\scripts\check_chatwoot_connectivity.py
"""
import os
import textwrap
from dotenv import load_dotenv

load_dotenv()

import requests
from app.services.chatwoot_service import chatwoot_client


def masked(s: str | None) -> str:
    if not s:
        return "(not set)"
    if len(s) <= 8:
        return "*" * len(s)
    return s[:4] + "..." + s[-4:]


def main():
    # Prefer CHATWOOT_BASE_URL; fallback CHATWOOT_URL for backward compatibility
    base_url = os.environ.get("CHATWOOT_BASE_URL") or os.environ.get("CHATWOOT_URL")
    # Prefer CHATWOOT_API_TOKEN; fallback CHATWOOT_API_KEY for backward compatibility
    api_key = os.environ.get("CHATWOOT_API_TOKEN") or os.environ.get("CHATWOOT_API_KEY")
    account_id = os.environ.get("CHATWOOT_ACCOUNT_ID")

    print("Chatwoot connectivity check")
    print("- Base URL:", base_url)
    print("- Account ID:", account_id)
    print("- API Key:", masked(api_key))

    if not base_url or not api_key or not account_id:
        print(
            "Missing required env vars. Please set "
            "CHATWOOT_BASE_URL and CHATWOOT_API_TOKEN "
            "(or CHATWOOT_URL and CHATWOOT_API_KEY) and CHATWOOT_ACCOUNT_ID."
        )
        return

    # Use Chatwoot's api_access_token header format
    headers = {
        "Content-Type": "application/json",
        "api_access_token": api_key,
        "User-Agent": "HardChews-Chatwoot-Integration/1.0",
    }
    account_endpoint = f"{base_url.rstrip('/')}/api/v1/accounts/{account_id}"

    print("\n1) GET account info ->", account_endpoint)
    try:
        resp = requests.get(account_endpoint, headers=headers, timeout=60)
        print(f"GET status: {resp.status_code}")
        try:
            print("Response JSON:")
            print(textwrap.indent(str(resp.json()), "  "))
        except Exception:
            print("Response text:")
            print(textwrap.indent(resp.text[:1000], "  "))
    except requests.exceptions.RequestException as e:
        print("GET request failed:", repr(e))
        print(
            "Possible causes: network egress blocked, DNS issue, wrong base URL, or Chatwoot down."
        )
        return

    # If GET succeeded (200), try creating a small conversation
    if resp.status_code == 200:
        print("\n2) Creating a test conversation (will appear in Conversations) ...")
        if not chatwoot_client.enabled:
            print(
                "chatwoot_client is not enabled (missing env vars). "
                "Ensure CHATWOOT_API_TOKEN/CHATWOOT_API_KEY and CHATWOOT_ACCOUNT_ID are set."
            )
            return

        try:
            create_resp = chatwoot_client.create_conversation(
                contact_email="test+integration@example.com",
                contact_name="Integration Test",
                message="Automated connectivity test from local project.",
            )
            print("Create response:")
            print(textwrap.indent(str(create_resp), "  "))
            print(
                "Done — if successful, check Chatwoot Dashboard → Conversations "
                "and search for test+integration@example.com"
            )
        except Exception as e:
            print("Create conversation failed:", repr(e))
            print(
                "If this is an auth error, check the API token and account id. "
                "If timeout, check network/firewall."
            )
    else:
        print("Account endpoint returned non-200 status. Inspect response above.")


if __name__ == "__main__":
    main()
