# Session Start Brief - Bug Bounty (FoE + Bullish)
_Written at 56k token wall. Read this before doing anything._

---

## The Mission

Two active targets. One has a confirmed partial finding waiting on credentials. One has a confirmed EUR 140 finding in triage and we are mid-recon on IDOR. The goal in both cases is the same: complete PoC with screenshot, then file. Nothing gets filed without that.

---

## Target 1: Bullish (simnext.bullish-test.com) - Bugcrowd

### What We Have
- **e9e1b89e** (P2) - JWT no-signature-verification on CoinDesk SSO endpoint
  - POST /api/v1/social/coindesk/users/login accepts forged JWTs regardless of signature
  - Three-tier proof: valid JWT (8407), wrong-secret JWT (8407), garbage "aaaa" sig (8407) - all identical
  - This is airtight. The blocker is we need a `sub` for a CoinDesk user with a linked Bullish account to get a 200 response
  - Without that, we can't complete the PoC

### The Credential Wall
- register/finalize returns HTTP 500 universally - no accounts can be created
- Recovery email never arrives (email field never written because finalize 500s)
- Browser registration geo-blocked (Netherlands proxy confirmed working but still blocked)
- Login page has no CoinDesk SSO button
- Bugcrowdninja email tried - same 500, no whitelist
- Bugcrowd triager was contacted 2026-04-02 ~10:44 requesting test credentials

### First Action This Session
Check Bugcrowd inbox. If triager responded with credentials - go straight to IDOR on /trading-api/v1/orders/{orderId}. That is the $25k ceiling finding.

If no response - Bullish is parked. Do not burn tokens on it until credentials arrive.

### Attack Plan (Once Credentialed)
1. IDOR on /trading-api/v1/orders/{orderId} - account 2 JWT targeting account 1 order IDs
2. Race conditions on concurrent orders/withdrawals
3. Negative values on orders/transfers
4. Sandbox/prod boundary - do sandbox JWTs work on api.bullish.com?

---

## Target 2: Forge of Empires (xs1.forgeofempires.com) - Intigriti

### What We Have
- **INNOGAMES-ZSMET17K** (EUR 140, Low/3.5, Triage) - production game routes diamond purchases to staging.igpayment.com
  - Confirmed still live 2026-04-02 with screenshot showing staging URL and failed ERR_TUNNEL_CONNECTION_FAILED
  - Intigriti comment posted with proof screenshot
  - This is already filed. Nothing more to do on it until triager responds.

### What We Built This Session (Critical)
- **Signing formula cracked:** `signature = MD5(h= + STATIC_KEY + body_string)[1:11]`
- Static key: `***REMOVED***`
- Verified against live session: computed == expected (exact match)
- Script: `D:\Atlas\projects\bug-bounty\foe_idor_probe.py` - uses curl.exe + MD5 signing
- Session credentials expire with browser tab - always grab fresh via Copy as cURL on a /game/json request

### What We Found
- `FriendService.invitePlayerById(player_id)` - returns real player profile data (name, avatar, score, city, era) for arbitrary player IDs. **WARNING: also sends a real friend invite.** Do not call this again without understanding the side effect.
- `OtherPlayerService.motivateById(building_entity, player_id)` - takes player ID parameter, untested for IDOR
- BonusService.getBonuses - responding OK, session alive

### Payment Chunk - VERIFIED DEAD END
Sources tab confirmed: only three JS files exist (ForgeHX, merged-3rd-party, merged-game). No additional lazy-loaded chunks. The payment/shop service methods that returned errors are not in local JS - the checkout UI is an iframe to staging.igpayment.com which is unreachable. That bug is already filed (INNOGAMES-ZSMET17K). No further JS hunting needed.

### FoE Next Steps (Priority Order)
1. Verify Sources tab for additional JS chunks (human gate - Jeff does this)
2. Test `OtherPlayerService.motivateById` with adjacent player IDs - does the server validate you can only motivate players you have a social relationship with?
3. If motivateById returns success on an arbitrary player ID = IDOR finding
4. Profile enumeration via FriendService is low value - probably intended behavior, don't file

### FoE Credentials (Need Fresh Grab Each Session)
- Account: AtlasFoE, player ID 7670076
- Copy as cURL from DevTools > Network > any /game/json request
- Grab: h= from URL, signature from headers, full Cookie string
- Last session hash (likely expired): h=a3kqkXxvIJePc_PPLjyUbU3p

---

## Rules For This Session

1. **No guessing.** Verify before concluding. "Probably" is not proof.
2. **No write methods without reading the JS first.** FriendService.invitePlayerById sent a live friend invite without warning. Check what a method does before calling it.
3. **No filing without complete PoC + screenshot.** Not negotiable.
4. **Atlas is at 30k-40k tokens when last seen.** He may need a fresh session too.
5. **Bugcrowd check is the first action.** If credentials arrived, drop FoE and go to Bullish IDOR.

---

## Key File Locations
| File | Purpose |
|------|---------|
| D:\Atlas\projects\bug-bounty\foe_idor_probe.py | FoE IDOR probe, curl.exe + MD5 signing |
| D:\Atlas\projects\bug-bounty\bullish_alg_confusion.py | JWT forge script, needs valid sub |
| D:\Atlas\knowledge\tactics.md | SOP - read at session start |
| D:\Atlas\memory\feedback.md | Hard rules - read before pitching anything |

---

## Token Cost Note
Session 2026-04-02 total estimate: ~$200+ across all sessions today. Budget is tight. Be efficient.
