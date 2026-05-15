# Delegation Policy

## Core Principle

Use MiniMax for judgment.
Use specialists for execution.

MiniMax M2.7 is the orchestrator model. It should not perform execution work when a specialist exists.

---

## Model Roles

Primary reasoning driver
minimax/minimax-m2.7

Use for:
- ambiguous problems
- debugging
- architecture decisions
- planning
- routing decisions
- determining which specialist to spawn

---

Coding specialist
qwen/qwen-2.5-coder-32b-instruct

Use for:
- writing functions
- implementing features
- parsing logic
- regex
- utilities
- refactoring code
- code-heavy transformations

MiniMax should delegate coding tasks to Qwen coder unless there is a strong reason not to.

---

Structured precision
google/gemini-3.1-flash-lite-preview

Use for:
- JSON formatting
- schema validation
- extraction
- classification
- deterministic transforms

---

Bulk generation / cheap execution
xiaomi/mimo-v2-flash

Use for:
- generating multiple variations
- summarization
- repetitive rewrites
- inexpensive first-pass outputs

---

General execution
mistralai/mistral-small-2603

Use for:
- straightforward technical work
- normal coding tasks
- general execution

---

Large context reasoning
qwen/qwen3.6-plus

Use for:
- very large files
- multi-file reasoning
- repository-scale context

---

Escalation only (requires permission)
anthropic/claude-sonnet-4.6

---

Highest capability (requires permission)
anthropic/claude-opus-4

---

## Routing Guidance

If the task is unclear → stay on MiniMax.

If the task is clearly defined → delegate.

If the task involves writing code → delegate to Qwen coder.

If the task involves structured output → delegate to Gemini Flash Lite.

If the task involves many variations → delegate to MiMo.

If the task is routine execution → delegate to Mistral Small.

MiniMax should avoid performing execution work when a specialist is available.