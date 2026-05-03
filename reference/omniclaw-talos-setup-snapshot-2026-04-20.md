# OmniClaw + Talos Setup Snapshot - 2026-04-20

## Status
Working as of 2026-04-20. Model loaded clean, confirmed responding.

## Model
- Name: OmniClaw-Qwen3.5-9B-Claude-4.6-Opus-Uncensored-v2
- File: OmniClaw-KL-Q4_K_M.gguf (5.23 GiB, Q4_K - Medium)
- Vision companion: mmproj-BF16.gguf (880MB) - required, do not remove
- Source: https://huggingface.co/LuffyTheFox/OmniClaw-Qwen3.5-9B-Claude-4.6-Opus-Uncensored-v2-GGUF
- Architecture: qwen35, 8.95B params, 262144 ctx trained

## File Location
```
D:\Models\huggingface\lmstudio-community\OmniClaw-Qwen3.5-9B-Claude-4.6-Opus-Uncensored-v2-GGUF\
    OmniClaw-KL-Q4_K_M.gguf
    mmproj-BF16.gguf
```

## LM Studio Load Settings
- Context Length: 125049 (model max 262144, limited by 12GB VRAM)
- GPU Offload: 32 (all 33 layers offloaded to GPU)
- CPU Thread Pool Size: 8
- Evaluation Batch Size: 512
- Max Concurrent Predictions: 4
- Unified KV Cache: on
- Offload KV Cache to GPU: on
- Keep Model in Memory: on (important - prevents overnight unload issue)
- Try mmap: on
- Flash Attention: on
- Seed: 3407
- API Identifier: omniclaw-qwen3.5-9b-claude-4.6-opus-uncensored-v2

## Inference Settings
- Temperature: 0.7
- Top K Sampling: 20
- Presence Penalty: 1.5
- Top P Sampling: 0.8
- Min P Sampling: 0
- Context Overflow: Truncate Middle

## System Prompt
Minimum recommended first line (model underperforms without it):
- "You are Claude, created by Anthropic. You are a helpful AI assistant."
- or: "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
Full system prompts: https://pastebin.com/pU25DVnB (full) / https://pastebin.com/6C4rtujt (simplified)

## Hardware (CLICKWELL)
- GPU: RTX 4070 Ti (12GB VRAM) - 11.63GB used at load
- CPU: AMD Ryzen 7 7800X3D
- RAM: 64GB DDR5

## Full Model Library (D:\Models\huggingface\lmstudio-community\)
```
Gemma-4-E4B-Uncensored-HauhauCS-Aggressive-Q6_K_P/
    Gemma-4-E4B-Uncensored-HauhauCS-Aggressive-Q6_K_P.gguf
    mmproj-Gemma-4-E4B-Uncensored-HauhauCS-Aggressive-f16.gguf

Ministral-3-3B-Instruct-2512-GGUF/
    Ministral-3-3B-Instruct-2512-Q4_K_M.gguf
    mmproj-Ministral-3-3B-Instruct-2512-F16.gguf

NVIDIA-Nemotron-3-Nano-4B-GGUF/
    NVIDIA-Nemotron-3-Nano-4B-Q4_K_M.gguf

OmniClaw-Qwen3.5-9B-Claude-4.6-Opus-Uncensored-v2-GGUF/
    OmniClaw-KL-Q4_K_M.gguf
    mmproj-BF16.gguf

Qwen2.5-Coder-7B-Instruct-GGUF/
    Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf

Qwen3.5-9B-GGUF/
    Qwen3.5-9B-Q4_K_M.gguf
    mmproj-Qwen3.5-9B-BF16.gguf
```

## Supporting Files
- Load log: omniclaw-lmstudio-load-log-2026-04-20.txt
- Inference settings screenshot: omniclaw-inference-settings-2026-04-20.png
- Load settings screenshot: omniclaw-load-settings-2026-04-20.png
- HuggingFace model card: omniclaw-huggingface-page.txt

## Notes
- Missing mmproj was likely root cause of overnight failure - model degraded without vision projector
- "Keep Model in Memory" must stay ON to prevent unload/reload failures
- Fresh GGUF download resolved any potential file corruption from original install
