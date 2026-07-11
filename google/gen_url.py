#!/usr/bin/env python3
"""Generate OAuth URL for gog auth."""
import json, secrets, base64, hashlib, urllib.parse

CREDS = "/Users/georgemalenclaw/.openclaw/workspace/google/oauth/client_secret.json"
with open(CREDS) as f:
    creds = json.load(f)

client_id = creds["installed"]["client_id"]
REDIRECT = "http://localhost"
state = secrets.token_urlsafe(16)
code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().rstrip("=")
code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).decode().rstrip("=")

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
    "code_challenge": code_challenge,
    "code_challenge_method": "S256",
    "state": state,
})

print("OPEN THIS URL:")
print(url)
print()
print("SAVE THIS CODE VERIFIER (needed for token exchange):")
print(code_verifier)
