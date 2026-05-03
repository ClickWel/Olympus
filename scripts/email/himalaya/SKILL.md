---
name: himalaya
description: CLI to manage emails via IMAP/SMTP. Use himalaya to list, read, write, reply, forward, search, and organize emails from the terminal. Supports multiple accounts and message composition with MML (MIME Meta Language).
version: 1.1.0
author: community
license: MIT
metadata:
  hermes:
    tags: [Email, IMAP, SMTP, CLI, Communication]
    homepage: https://github.com/pimalaya/himalaya
prerequisites:
  commands: [himalaya]
---

# Himalaya Email CLI

Himalaya is a CLI email client for IMAP/SMTP. Installed at `~/.local/bin/himalaya` via the install script.

## Installation

```bash
curl -sSL https://raw.githubusercontent.com/pimalaya/himalaya/master/install.sh | PREFIX=~/.local sh
```

## Gmail Configuration (v1.x TOML format)

### App Passwords vs Advanced Protection

**Standard Gmail:** Enable 2FA first, then generate App Password at https://myaccount.google.com/apppasswords

**Gmail with Advanced Protection / Security Keys ONLY:** App Passwords are BLOCKED — hard Google restriction, no workaround. Use a separate Gmail account without security keys for CLI email.

### Working config for himalaya v1.2.0

**Auth script approach** (recommended — keeps password out of config file):

1. Create auth script:
```bash
mkdir -p ~/.config/hermes
cat > ~/.config/hermes/gmail_auth.sh << 'SCRIPT'
#!/bin/bash
echo "iqyp lena jeoy vddj"
SCRIPT
chmod +x ~/.config/hermes/gmail_auth.sh
```

2. TOML config at `~/.config/himalaya/config.toml`:
```toml
[accounts.gmail]
email = "you@gmail.com"
display_name = "Your Name"
default = true

[accounts.gmail.folder.aliases]
inbox = "INBOX"
sent = "[Gmail]/Sent Mail"
drafts = "[Gmail]/Drafts"
trash = "[Gmail]/Trash"

[accounts.gmail.backend]
type = "imap"
host = "imap.gmail.com"
port = 993
encryption.type = "tls"
login = "you@gmail.com"
auth.type = "password"
auth.cmd = "/home/click/.config/hermes/gmail_auth.sh"

[accounts.gmail.message.send.backend]
type = "smtp"
host = "smtp.gmail.com"
port = 587
encryption.type = "starttls"
login = "you@gmail.com"
auth.type = "password"
auth.cmd = "/home/click/.config/hermes/gmail_auth.sh"
```

### Gmail Folder Aliases

Gmail uses non-standard folder names like `[Gmail]/Sent Mail`. Without aliases, sent mail fails with "Folder doesn't exist." Always include the aliases block.

### Troubleshooting AUTHENTICATIONFAILED

1. Must use **App Password**, not regular account password
2. If App Passwords page says "not available for your account" → account has Advanced Protection, create a separate Gmail
3. After enabling 2FA, App Passwords option appears at https://myaccount.google.com/apppasswords
4. Test: `openssl s_client -connect imap.gmail.com:993 -quiet`

## Common Operations

```bash
# List folders
himalaya folder list

# List emails (INBOX)
himalaya envelope list --page-size 10

# List sent mail
himalaya envelope list --folder sent

# Send email (non-interactive, use this from Hermes)
cat << 'EOF' | himalaya template send
From: you@gmail.com
To: recipient@example.com
Subject: Test

Body here.
EOF

# Read email
himalaya message read <id>

# Search
himalaya envelope list from someone@example.com subject meeting

# Move to folder
himalaya message move <id> "Archive"
```

## Debugging

```bash
RUST_LOG=debug himalaya envelope list
```

## Google Account Signup (2025+)

Google's current signup flow does NOT let you pick your own email upfront. It auto-generates from your name. To get a specific address:
- Complete the name/birthday steps
- At the email step, Google suggests options — if none work, look for a "choose custom" option on that screen
- Do NOT tell users an email is "available" without checking in the browser — Google generates suggestions dynamically

## Tips

- Use `himalaya template send` with piped stdin for reliable non-interactive sending from scripts
- Message IDs are folder-relative — re-list after moving/deleting
- `auth.cmd` requires a script that simply echoes the password (for use when `pass` is not installed and no root for apt)
- `auth.raw` also works but exposes password in config file (testing only)
