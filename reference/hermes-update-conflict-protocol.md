# Hermes Update Conflict Protocol

## When it happens
`hermes update` pulls from upstream (NousResearch/Hermes-Agent). If we have local
modifications to tracked files, the update autostashes them and may produce merge
conflicts on pop.

## Files that commonly conflict

- `cli.py` - we maintain a Windows-to-WSL path fix in `_resolve_attachment_path()`
- `agent/model_metadata.py` - we maintain vision model detection functions at the bottom
- `package-lock.json` - we maintain `@askjo/camofox-browser` as a local dependency

## Resolution steps

1. After `hermes update` reports conflicts, stash ref is shown (e.g. `5e83a3366`)
2. Conflicts are in the hermes-agent repo at `/home/click/.hermes/hermes-agent`
3. Pop the stash: `git stash pop` (or it may already be mid-merge)
4. For `cli.py`: conflicts are usually in unrelated sections - keep both (upstream new
   commands + our stashed changes). The WSL path fix lives in `_resolve_attachment_path()`
   around line 1146. Upstream typically does not touch this function.
5. For `package-lock.json`: additive only - keep both upstream entries and our
   camoufox entry. Use `git checkout -- package-lock.json` then manually re-add our
   dependency, or accept upstream and patch it back in.
6. For `model_metadata.py`: our additions are appended at the bottom after
   `estimate_request_tokens_rough()`. Upstream rarely touches the end of this file.
   Keep everything.
7. `git add package-lock.json cli.py` then `git commit` to finish the merge.

## Our local additions to preserve

### cli.py - `_resolve_attachment_path()` (~line 1146)
```python
import re

# Convert Windows paths to WSL paths (e.g. C:\Users\... -> /mnt/c/Users/...)
if re.match(r"^[A-Za-z]:[/\\]", expanded):
    drive = expanded[0].lower()
    expanded = f"/mnt/{drive}" + expanded[2:].replace("\\", "/")
```

### agent/model_metadata.py - appended at end of file
- `VISION_CAPABLE_MODEL_PREFIXES` frozenset
- `model_supports_vision(model_name)` function
- `encode_image_as_base64(image_path)` function

### package.json / package-lock.json
- `@askjo/camofox-browser` v1.5.2 (bug bounty stealth browser tooling)

## Backup
Before any hermes update, `cli.py.bak_olympus_YYYYMMDD` is written to the repo root.
That is the reference copy of our local state if the stash gets mangled.
