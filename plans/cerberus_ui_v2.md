# Cerberus UI - Next Session Work Order [COMPLETED 2026-04-01]

Written by Olympus, 2026-04-01. Hand this to the next agent.

---

## Context

Cerberus is Jeff's offline AI guardian running on Ollama (gemma3:27b).
The web UI is live and working at http://localhost:8765, served by cerberus_server.py.

Files:
- Server: `D:\Olympus\scripts\cerberus_server.py`
- UI: `D:\Cerberus\ui\index.html`
- Launcher: `C:\Users\click\Desktop\Cerberus.bat`

The UI is functional. What follows are improvements Jeff requested.

---

## Issues to Fix

### 1. Streaming - render all at once, not word by word

**Problem:** Responses currently stream word-by-word into the DOM (`body.textContent = raw` on every token). This looks like typing. Jeff wants the full response to appear at once when it's done - no word-by-word effect.

**Fix:** In `index.html`, inside the `stream()` function, accumulate tokens in `raw` but do NOT update the DOM on each token. Only update when `o.done` fires:

```javascript
if (o.t) {
  if (first) {
    rmThinking(); // hide dots when first token arrives (so there's no delay)
    // create the message element but leave it empty
    const wrap = addMsg('cerb', ''); body = wrap.querySelector('.body'); first = false;
  }
  raw += o.t;  // accumulate silently
}
if (o.done && body) {
  body.innerHTML = md(raw);  // render all at once
  scrollEnd();
}
```

Keep the thinking dots visible the entire time tokens are streaming. Remove them when `done` fires, then show the message. This is cleaner and avoids the typewriter effect.

Actually - better approach: keep showing thinking dots until `done`, then reveal the full rendered message. That way Jeff sees "thinking" state clearly and the response appears complete.

---

### 2. Timer on thinking animation

**Problem:** Cerberus takes a while to respond (gemma3:27b is slow). Jeff wants to know how long it's been thinking.

**Fix:** Add a second counter next to the "cerberus thinking" label. Start counting when the thinking indicator appears, stop and clear when it's removed.

In the `addThinking()` function, start a `setInterval` that increments a counter every second and updates the label text:
- Shows: `cerberus thinking  0:12`
- Format: `M:SS` (so 0:05, 1:23, etc.)

Store the interval ID on the element so `rmThinking()` can clear it.

```javascript
function addThinking() {
  const d = document.createElement('div'); d.className = 'thinking'; d.id = 'thinker';
  d.innerHTML = '...dots... <span class="thinking-lbl">cerberus thinking</span><span class="thinking-timer" id="think-timer">0:00</span>';
  $('msgs').appendChild(d); scrollEnd();
  let secs = 0;
  d._timer = setInterval(() => {
    secs++;
    const m = Math.floor(secs/60), s = String(secs%60).padStart(2,'0');
    const el = $('think-timer'); if (el) el.textContent = `${m}:${s}`;
  }, 1000);
}

function rmThinking() {
  const e = $('thinker');
  if (e) { clearInterval(e._timer); e.remove(); }
}
```

Style `.thinking-timer` as: same size as the label, slightly dimmer, monospace, left margin ~8px.

---

### 3. Favicon

**Problem:** No favicon, browser tab shows generic icon.

**Fix:** Add an inline SVG favicon. A simple three-dot icon in red works well for Cerberus (three heads). No external files needed - embed as a data URI in the `<head>`:

```html
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><circle cx='8' cy='20' r='5' fill='%23f08080'/><circle cx='16' cy='14' r='6' fill='%23f06060'/><circle cx='24' cy='20' r='5' fill='%23f08080'/></svg>">
```

Three red circles of slightly different sizes - representing the three heads. Simple, recognizable at 16px favicon size.

---

### 4. Text readability

**Problem:** Text is too dim, hard to read across the UI. Several elements are close to invisible.

**Issues identified:**
- Main text `--text: #c2d4e2` is readable but on the dim side
- `--dim: #364f62` is far too dark - used for muted labels and secondary text, nearly invisible
- Card topic text `.hd-topic` color `#5a7a90` is too dark against the card background
- Memory tags `.tag` text `#3a5568` is nearly invisible
- Command buttons `.cb` color `var(--dim)` - too dark
- The "online - cerberus memory..." status message at the bottom is barely visible

**Fix - color adjustments:**
```css
--text:    #d0e2ee;   /* brighter - up from #c2d4e2 */
--dim:     #5a7a90;   /* brighter - was #364f62, now readable */
```

And specifically:
- `.hd-topic` color: `#7a9db5` (up from `#5a7a90`)
- `.tag` color: `#5a7a90` (up from `#3a5568`), `.tag.on` color: `#90b0c8`
- `.msg-s` (system messages) color: `var(--dim)` which after the above fix will be `#5a7a90` - still dim but visible

---

### 5. Input area - accessibility and prominence

**Problem:** The input bar is cramped against the bottom of the browser window. It's small, the textarea is thin, and users have to be precise to click it. Jeff referenced ChatGPT and Claude.ai as better examples.

**What good AI UIs do:**
- The input area has significant visual weight - it's a clear focal point
- Taller default input (not just one line, more like 2-3 lines minimum)
- More padding inside the input container
- The input container itself has a clear border that lights up on focus
- Command buttons are typically above or integrated, not fighting for space with the input
- More breathing room below the input (padding at the bottom of the bar)

**Specific changes:**
1. Increase `.irow` padding: `padding: 12px 14px` (up from `9px 11px`)
2. Increase `#msg` default height: change `rows="2"` in HTML (or min-height in CSS: `min-height: 44px`)
3. Increase `.bar` bottom padding: `padding: 12px 16px 18px` (more air at the bottom)
4. Make the input border more visible by default: `border: 1px solid rgba(255,255,255,0.12)` (up from `0.06`)
5. Make the send button bigger: `padding: 10px 20px` (up from `6px 14px`)
6. Consider putting the command buttons INSIDE or ABOVE the input more visually - or floating them at the top of the bar with a clear separator

---

## Design Direction Question for Subagent

Jeff noted the UI feels "a little retro" from the monospace font and dark color scheme. Before making big design changes, consider asking a subagent:

> "Here is a screenshot of a dark-mode AI chat UI with a monospace font and deep navy/near-black color scheme. The three-panel 'heads' section at the top shows team member status. What 3-5 specific changes would make this feel more modern without losing the identity? Consider: typography, spacing, card design, and input area."

Feed it the current screenshot and get specific CSS-level recommendations before implementing.

The retro feel isn't necessarily bad - it fits Cerberus's guardian/terminal character. Jeff wants to see the next agent's take.

---

## What is Working Well (Do Not Break)

- Three heads panel with live last-session topics
- Streaming from Ollama via Flask SSE
- /search, /clear, /note, /memory commands
- Image attachment support
- Model selector
- Save session button
- Memory tag indicators (lit up when loaded)
- Server syntax is clean, Flask routes all functional

---

## Files - Current State

All three files were written this session and are in good shape:

```
D:\Olympus\scripts\cerberus_server.py   - Flask server, all routes working
D:\Cerberus\ui\index.html               - Chat UI, functional
C:\Users\click\Desktop\Cerberus.bat     - Launcher (plain cmd, no WT profile needed)
```

The Windows Terminal "Cerberus" profile with red tab still exists but the bat no longer requires it. That profile can be removed at Jeff's discretion.
