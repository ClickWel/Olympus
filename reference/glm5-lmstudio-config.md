# GLM5.1 Distill - LM Studio Config
# Added: 2026-04-21

## Model
- File: Qwen3.5-9B-GLM5.1-Distill-v1-Q4_K_M.gguf
- Full name: Qwen3.5-9B-GLM5.1-Distill-v1
- Quantization: Q4_K_M
- Location: C:/Users/click/.lmstudio/models/Qwen3.5-9B-GLM5.1-Distill-v1-GGUF/
- Endpoint: http://10.0.0.25:1234 (when loaded)

## Load Settings
- Context Length: 140501 tokens
- VRAM Usage: ~10.5 GB (of 12 GB on RTX 4070 Ti)
- Headroom: ~1.5 GB

## Notes
- GLM5.1 distilled onto Qwen3.5 9B base
- Known issue: GLM4 outputs raw JSON instead of calling tools - verify GLM5.1 behavior before using as a worker

## Status
- Moved to D:/Models/huggingface/lmstudio-community/Qwen3.5-9B-GLM5.1-Distill-v1-GGUF/: 2026-04-21
- Not yet added to Talos - pending load test and config
