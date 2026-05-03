# Microsoft Todo - Auth Fix Reference

## The Problem
`azure-identity` `DeviceCodeCredential` and raw MSAL `acquire_token_by_device_flow` both hang
when run inside a subprocess. The device code URL/code is never shown and the call blocks forever.
Token cache is never written. This bit Argus on Apr 13, 17, and 18 2026.

## The Fix
Separate auth into a one-time blocking step. All other commands use cached tokens only.

**Script:** `D:/Clawdbot/skills/microsoft-todo/scripts/simple_todo_manager.py`
**Cache:** `C:/Users/click/.cache/msal/todo_cache.json`

## One-Time Auth
```
python "D:/Clawdbot/skills/microsoft-todo/scripts/simple_todo_manager.py" auth
```
Visit https://www.microsoft.com/link and enter the printed code. Done.

## Daily Usage
```
python "D:/Clawdbot/skills/microsoft-todo/scripts/simple_todo_manager.py" list
python "D:/Clawdbot/skills/microsoft-todo/scripts/simple_todo_manager.py" add "task title"
python "D:/Clawdbot/skills/microsoft-todo/scripts/simple_todo_manager.py" done "partial title or number"
```

## If It Breaks Again
1. Check cache exists: `C:/Users/click/.cache/msal/todo_cache.json`
2. If missing or empty: re-run `auth`
3. Refresh tokens expire after 90 days of inactivity
4. Never use `azure-identity` `DeviceCodeCredential` - it swallows the device code prompt silently
5. Use `msal.PublicClientApplication` with `msal.SerializableTokenCache` directly
6. `authority="https://login.microsoftonline.com/consumers"` is correct for personal MS accounts

## Key Code Pattern
```python
cache = msal.SerializableTokenCache()
if CACHE_PATH.exists():
    cache.deserialize(CACHE_PATH.read_text(encoding='utf-8'))
app = msal.PublicClientApplication(client_id=..., authority=..., token_cache=cache)
# For auth: initiate_device_flow -> print message -> acquire_token_by_device_flow -> save cache
# For use: get_accounts -> acquire_token_silent -> save cache if changed
```
