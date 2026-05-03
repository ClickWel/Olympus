# Active Plan — CC Terminal BB Workers + HermesDesktop

## BB Worker Pipeline (as of 2026-05-02)

BB Loop cancelled. Replaced with CC terminals as workers on free tiers (Hy3, Laguna), coached by Codex (OpenAI desktop agent).

### Setup
- Workers: CC terminals running free-tier models (Hy3, Laguna)
- Coach: Codex (OpenAI desktop agent)
- No account creation needed, no flaky loops

### Status
- Pending initial deployment and testing

---

## HermesDesktop Status (as of 2026-04-29)

/collab bugs deployed. All prior tab fixes still coded and ready. Ghost process fixed, TaskPanel live, FileBrowser labels fixed.

### Remaining HermesDesktop Work
1. STT / voice input (F9) -- not started
2. Three-way collab test -- not done
3. "Hermes Desktop" sidebar label hardcoded -- quick fix
4. Thinking streams inline -- not started
5. Talos flashing terminal -- cosmetic, low priority

## What's Coded and Ready to Deploy

- FileBrowserPanel blank labels -- FIXED (Content.Name / Content.Icon binding)
- TaskPanel live updates -- FIXED (TaskManager.TaskChanged event wired to TaskPanel.Refresh)
- TodoWriteTool -> InMemoryTodoStore singleton -- Tasks tab mirrors agent todo_write list live
- Ghost process on close -- FIXED (Environment.Exit(0) on window Closed)
- Agent panel Souls tab -- "Apply This Soul" removed, "Merge to Editor" replaces it
- Merge to Editor -- appends template below current soul with separator for cherry-picking
- Reset button -- restores session-start snapshot of real soul, not generic template
- Hermes context window -- 204800 set in profile config (live already, no publish needed)
- Talos todo_write instruction -- added to SOUL.md (live already)
- Talos narration rule -- removed from SOUL.md (live already)

## Remaining Work

1. STT / voice input (F9) -- not started
2. Three-way collab test -- not done
3. "Hermes Desktop" sidebar label hardcoded -- quick fix
4. Thinking streams inline (feed step 4) -- not started
5. Talos flashing terminal -- cosmetic, low priority
