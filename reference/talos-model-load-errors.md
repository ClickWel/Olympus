# Talos Model Load Errors - Diagnosis Guide

_Written 2026-04-07 after resolving gemma4-26b-talos tool failure_

---

## Error 1: "does not support tools" (400)

**Example:**
```
API Error: 400 {"type":"error","error":{"type":"invalid_request_error",
"message":"registry.ollama.ai/library/devstral-talos:latest does not support tools"}}
```

**Cause:** CC is routing to the Ollama cloud registry instead of local Ollama. It checks tool support against the registry, which doesn't know about local custom model names, and rejects them.

**Fix:** Set env vars in `launch-talos.ps1` before the `ollama launch claude` call:
```powershell
$env:ANTHROPIC_BASE_URL = "http://localhost:11434"
$env:ANTHROPIC_MODEL = $Model
```
This is already applied as of 2026-04-07. If this error reappears, check that `launch-talos.ps1` still has these lines.

---

## Error 2: "unable to load model" (500)

**Example:**
```
500 {"type":"error","error":{"type":"api_error",
"message":"unable to load model: D:\OllamaModels\blobs\sha256-84963bde..."}}
```

**Cause:** One of two things. Check Ollama server log to find out which:
```
C:\Users\click\AppData\Local\Ollama\server.log
```

### Cause A: Unknown model architecture

Log line: `error loading model architecture: unknown model architecture: 'gemma4'`

Ollama's bundled llama.cpp doesn't support the model architecture yet. Happens with newly released model families (e.g. Gemma 4 wasn't supported until after Ollama 0.20.3).

**Fix:**
1. Check if the Ollama registry has its own build: `ollama pull modelname:tag`
2. If the registry pull works (loads cleanly), rebuild the talos variant from the registry base instead of the LM Studio GGUF:
   - Edit the Modelfile at `D:\Talos\[model-dir]\modelfiles\[model]-talos.Modelfile`
   - Change `FROM D:\Models\huggingface\...` to `FROM registrymodel:tag`
   - Run `ollama create [model]-talos -f [modelfile path]`
3. If the registry also fails, Ollama doesn't support it yet. Wait for an Ollama update or use LM Studio directly.

**Do NOT:** Try to fix this by re-pulling the LM Studio GGUF. The GGUF is fine. The problem is Ollama's llama.cpp version.

### Cause B: VRAM full

Log line: model loads but OOM / process killed

`launch-talos.ps1` already flushes all loaded models before launch as of 2026-04-07. If this still happens, another process (LM Studio, a second Talos window) is holding VRAM. Close it and retry.

---

## Error 3: Tool calls not working (model responds in text instead of calling tools)

**Cause (historical, pre-2026-04-07):** Custom TEMPLATE in Modelfile overriding Ollama's native tool call conversion. The custom template outputs `<tool_call>` XML, CC expects JSON tool_use format.

**Status:** This was investigated but turned out NOT to be the real issue. The Ollama API layer converts correctly regardless of custom TEMPLATE. The actual problems were errors 1 and 2 above.

**If this resurfaces:** Check Ollama server log for conversion errors. Test the model directly via API:
```
curl.exe -s http://localhost:11434/api/chat -d "{\"model\":\"modelname\",\"messages\":[{\"role\":\"user\",\"content\":\"Use the calculator tool to add 2+2.\"}],\"tools\":[{\"type\":\"function\",\"function\":{\"name\":\"calculator\",\"description\":\"Math\",\"parameters\":{\"type\":\"object\",\"properties\":{\"expression\":{\"type\":\"string\"}},\"required\":[\"expression\"]}}}],\"stream\":false}"
```
If `tool_calls` appears in the response with `id` and `arguments`, Ollama is fine and the problem is elsewhere.

---

## Quick Diagnosis Flow

```
Tool error in Talos CC?
  |
  +-- 400 error? --> ANTHROPIC_BASE_URL not set. Check launch-talos.ps1.
  |
  +-- 500 "unable to load"? --> Check server.log
        |
        +-- "unknown model architecture" --> Ollama doesn't support it.
        |     Pull from registry. If registry works, rebuild Modelfile from registry base.
        |
        +-- OOM / killed --> VRAM issue. Close other model windows, retry.
  |
  +-- Model loads but won't call tools? --> Test via API directly (see above).
        If API works, problem is in CC config, not the model.
```

---

## Script Paths in Role Files - Use Forward Slashes and Quotes

When writing script paths in Talos role files, always use forward slashes and wrap in quotes:

```
# WRONG - backslashes cause path concatenation bugs
python D:\Clawdbot\skills\trello_snapshot\trello_snapshot.py

# RIGHT - quoted forward slashes work reliably
python "D:/Clawdbot/skills/trello_snapshot/trello_snapshot.py"
```

**Why:** Local models running from a working directory (e.g. `D:\Talos\gemma4-26b`) treat unquoted backslash paths as relative. The result is a mangled path like `D:\\Talos\\gemma4-26b\\clawdbotskillstrello_snapshottrello_snapshot.py`. Forward slashes with quotes are unambiguous regardless of working directory.

---

## Files Changed During This Fix (2026-04-07)

- `D:\Talos\launch-talos.ps1` - added ANTHROPIC_BASE_URL + ANTHROPIC_MODEL env vars, added VRAM flush before launch
- `D:\Talos\gemma4-26b\modelfiles\gemma4-26b-talos.Modelfile` - rebuilt from `gemma4:26b` registry base (LM Studio GGUF unusable until Ollama adds gemma4 arch support)
- `D:\Talos\daily-driver\modelfiles\glm46v-native.Modelfile` - created as template-free GLM build (investigation artifact, not in active use)
