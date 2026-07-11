# Google Setup — Run When You Have Terminal Access

```bash
export GOG_KEYRING_BACKEND=file

gog auth credentials /Users/georgemalenclaw/.openclaw/workspace/google/oauth/client_secret.json

gog auth add mcharlesantoine@gmail.com --services gmail,calendar,drive,contacts,sheets

# Sign in + allow access when browser opens

gog auth list  # Should show mcharlesantoine@gmail.com
```

Once done, I'll be able to:
- Check Gmail (unread, search, send, drafts)
- View/create calendar events
- Search Drive files
- Access contacts
- Read/edit Google Sheets
