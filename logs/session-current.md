[17:53] - Qwen Code multi-provider setup complete. All keys self-contained in ~/.qwen/settings.json. Duplicate model ID bug identified (gpt-4o, claude-sonnet-4-6 appear twice with different providers) - causes models to disappear after first use. Fix pending next session.

[Session 2026-05-16] - Hack Team shortcut fixes + icon overhaul
[16:00] - Fixed 3 broken BB-oss20b shortcuts (all pointed to Pwn_BB instead of their own dirs)
[16:01] - Created missing start-oss20b-bb.bat files for Crypt_BB, Recon_BB, Sics_BB
[16:02] - Set CTF icons to shield (imageres.dll,102), BB to warning X (shell32.dll,131)
[16:05] - Changed crush.json diff_mode from split to inline per Jeff request
[16:10] - Vision-verified icons: imageres_101=green shield+checkmark (Jeff's CTF pick)
[16:11] - Verified: imageres_96=night mode, shell32_174=display split, shell32_277=info circle - none work for BB
[16:12] - Current BB icon (shell32_131) confirmed as orange X - Jeff right, looks like error not warning
[16:13] - Jeff wants to pick BB icon still - no decision yet

[Session 2026-05-17]
[09:00] - Updated Crush launch-crush.ps1 Google key to paid tier key
[09:05] - Updated Crush small model to gemini-3.1-flash-lite in global config (AppData/Local/crush/crush.json)
[09:10] - Verified gemini-3.1-flash-lite live on free key - no funds needed
