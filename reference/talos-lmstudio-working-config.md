# Talos - LM Studio Working Config
# Confirmed working: 2026-04-17

## Model
- File: Qwen3.5-9B-Q4_K_M.gguf
- Quantization: Q4_K_M
- Size on disk: 6.55 GB
- API identifier: qwen/qwen3.5-9b
- Endpoint: http://10.0.0.25:1234

## Load Tab
- Context Length: 102400
- GPU Offload: 32 (max)
- CPU Thread Pool Size: 8
- Evaluation Batch Size: 512
- Max Concurrent Predictions: 4 (experimental)
- Unified KV Cache: ON (experimental)
- RoPE Frequency Base: Auto
- RoPE Frequency Scale: Auto
- Offload KV Cache to GPU Memory: ON
- Keep Model in Memory: ON
- Try mmap(): ON
- Seed: Random
- Flash Attention: ON
- K Cache Quantization Type: OFF
- V Cache Quantization Type: OFF
- TTL Auto-Unload: 1 hour

## Inference Tab
- Context Overflow: Truncate Middle  *** NOT Rolling Window - breaks Talos SOUL loading ***
- CPU Threads: 8
- Enable Thinking: OFF
- Temperature: 0.4
- Limit Response Length: OFF
- Top K Sampling: 20
- Presence Penalty: 1.5 (ON)
- Top P Sampling: 0.95 (ON)
- Min P Sampling: OFF
- Structured Output: OFF

## VRAM Usage
- At 102400 context: ~10.77 GB (of 12 GB on RTX 4070 Ti)
- Headroom: ~1.4 GB

## Known Bad Settings
- Rolling Window overflow: causes Talos to respond without using tools, appears braindead
- Context 131072: only 350MB headroom, orphan process causes step-down to 64K
- CPU Threads 6: underutilizes 7800X3D, 8 matches physical core count
