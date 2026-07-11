#!/usr/bin/env python3
"""Generate Google OAuth URL and verifier for gog."""
import json, secrets, base64, hashlib, urllib.parse

CREDS = "/Users/georgemalenclaw/.openclaw/workspace/google/oauth/client_secret.json"
with open(CREDS) as f:
    creds = json.load(f)

client_id = creds["installed"]["client_id"]
REDIRECT = "http://localhost"

state = secrets.token_urlsafe(16)
verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().rstrip("=")
challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")

scopes = " ".join([
    "openid", "email",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/contacts",
    "https://www.googleapis.com/auth/spreadsheets",
])

url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
    "client_id": client_id,
    "redirect_uri": REDIRECT,
    "response_type": "code",
    "scope": scopes,
    "access_type": "offline",
    "prompt": "consent",
    "code_challenge": challenge,
    "code_challenge_method": "S256",
    "state": state,
})

print("=== STEP 1: Open this URL in your browser ===")
print(url)
print()
print("=== STEP 2: After sign-in, copy the 'code' parameter from the redirect URL ===")
print()
print("=== STEP 3: Save this code verifier for token exchange ===")
print(f"CODE_VERIFIER={verifier}")
