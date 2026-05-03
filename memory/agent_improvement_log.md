# Agent Improvement Log - 2026-04-06

Owner: Jeff (ClickWell)
Focus: Efficiency, Accuracy, Deliverable-First Mindset

1. EFFICIENCY IMPROVEMENTS
- MCP-First: Verify `claude mcp list` before custom builds.
- Delta-Only: Ship exact edit blocks first, narrate only if necessary.
- Landed-Only: Only report finished work, no "attempted" or "scaffolded" fluff.

2. AVOIDANCE OF MISTAKES
- Source of Truth: Trust screenshots/API over assumptions. If not visible, it doesn't exist.
- Hard Constraints: Hypothesis fields in Notion are locked. Do not edit.
- KPI Alignment: Primary KPI = RPV (Section 7.1) across all briefs.

3. OPTIMIZING INPUT
- Screenshots are mandatory for UI verification.
- Direct constraints/Golden Rules ("Don't touch X") are the best input.
