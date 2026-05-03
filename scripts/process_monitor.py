"""
Process Monitor - Olympus
Checks for orphaned, long-running, high-CPU, and known-agent processes.
Writes report to D:/Shared/reports/process_report.txt
"""

import subprocess
import json
import datetime
import os
import sys

REPORT_PATH = "D:/Shared/reports/process_report.txt"

KNOWN_AGENTS = {
    "argus":   "D:/Argus",
    "atlas":   "D:/Atlas",
    "hermes":  "D:/Hermes",
    "ares":    "D:/Ares",
    "olympus": "D:/Olympus",
}

BRAVE_DEBUG_PORT = 9222

SYSTEM_PROCESS_NAMES = {
    "svchost", "lsass", "csrss", "wininit", "winlogon", "services",
    "smss", "dwm", "fontdrvhost", "registry", "system", "idle",
    "spoolsv", "searchindexer", "taskhostw", "sihost", "ctfmon",
    "runtimebroker", "securityhealthservice", "antimalware service executable",
    "msmpeng", "wmiprvse", "dllhost", "conhost", "audiodg"
}

def run_ps(cmd):
    result = subprocess.run(
        ["powershell", "-Command", cmd],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    return result.stdout.strip()

def get_processes():
    ps_cmd = """
    Get-Process | ForEach-Object {
        $wmi = Get-WmiObject Win32_Process -Filter "ProcessId=$($_.Id)" -ErrorAction SilentlyContinue
        [PSCustomObject]@{
            Name       = $_.Name
            Id         = $_.Id
            CPU        = [math]::Round($_.CPU, 1)
            RAM_MB     = [math]::Round($_.WorkingSet / 1MB, 1)
            StartTime  = if ($_.StartTime) { $_.StartTime.ToString("yyyy-MM-dd HH:mm") } else { "unknown" }
            CommandLine = if ($wmi) { $wmi.CommandLine } else { "" }
            ParentId   = if ($wmi) { $wmi.ParentProcessId } else { 0 }
        }
    } | ConvertTo-Json -Depth 2
    """
    out = run_ps(ps_cmd)
    try:
        data = json.loads(out)
        if isinstance(data, dict):
            data = [data]
        return data
    except Exception:
        return []

def check_brave_debug():
    out = run_ps(f"netstat -ano | findstr ':{BRAVE_DEBUG_PORT}'")
    listening = f":{BRAVE_DEBUG_PORT}" in out and "LISTENING" in out
    pid = None
    if listening:
        for line in out.splitlines():
            if "LISTENING" in line:
                parts = line.strip().split()
                if parts:
                    pid = parts[-1]
    return listening, pid

def age_days(start_str):
    if start_str == "unknown":
        return None
    try:
        start = datetime.datetime.strptime(start_str, "%Y-%m-%d %H:%M")
        return (datetime.datetime.now() - start).days
    except Exception:
        return None

def build_report(procs):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = []
    lines.append("=" * 60)
    lines.append(f"  PROCESS MONITOR REPORT - {now}")
    lines.append("=" * 60)

    # --- Brave debug port ---
    brave_listening, brave_pid = check_brave_debug()
    lines.append("\n[BRAVE DEBUG PORT :9222]")
    if brave_listening:
        lines.append(f"  STATUS : ACTIVE (PID {brave_pid})")
        lines.append("  ACTION : Run kill-brave-debug.bat to stop it")
    else:
        lines.append("  STATUS : not listening (safe)")

    # --- Agent processes ---
    # Read agent PID registry (Atlas/Argus write Windows PIDs here)
    pid_registry = {}
    pid_registry_path = "D:/Shared/reports/agent_pids.json"
    try:
        with open(pid_registry_path, "r", encoding="utf-8") as f:
            pid_registry = json.load(f)
    except Exception:
        pass

    # Read Hermes/Ares status files (WSL PIDs - used for alive/dead detection only)
    wsl_agent_status = {}
    for agent in ["hermes", "ares"]:
        pid_file = f"D:/Shared/reports/{agent}_pid.txt"
        try:
            with open(pid_file, "r", encoding="utf-8") as f:
                wsl_pid = f.read().strip()
            wsl_agent_status[agent] = wsl_pid
        except Exception:
            wsl_agent_status[agent] = None

    lines.append("\n[AGENT PROCESSES]")
    agent_hits = {k: [] for k in KNOWN_AGENTS}
    claude_cli_procs = []
    for p in procs:
        name_lower = p["Name"].lower()
        cmd_lower = (p.get("CommandLine") or "").lower()
        # Check PID registry first
        pid_match = pid_registry.get(str(p["Id"]))
        if pid_match and pid_match in agent_hits:
            agent_hits[pid_match].append(p)
            continue
        # claude.exe CLI - collect separately, can't determine working dir
        if name_lower == "claude" and ".local" in cmd_lower:
            claude_cli_procs.append(p)
            continue
        for agent, path in KNOWN_AGENTS.items():
            if agent in name_lower or path.lower().replace("d:/", "d:\\") in cmd_lower or path.lower() in cmd_lower:
                agent_hits[agent].append(p)
    for agent, hits in agent_hits.items():
        if agent in wsl_agent_status:
            # WSL agent - check status file
            wsl_pid = wsl_agent_status[agent]
            if wsl_pid:
                lines.append(f"  {agent.upper():<10} RUNNING (WSL PID {wsl_pid})")
            else:
                lines.append(f"  {agent.upper():<10} not detected")
        elif hits:
            for p in hits:
                lines.append(f"  {agent.upper():<10} PID {p['Id']:<7} CPU {p['CPU']:<8} RAM {p['RAM_MB']} MB  started {p['StartTime']}")
        else:
            lines.append(f"  {agent.upper():<10} not detected")
    if claude_cli_procs:
        lines.append(f"  {'CLAUDE CLI':<10} {len(claude_cli_procs)} unregistered session(s)")
        for p in claude_cli_procs:
            lines.append(f"    PID {p['Id']:<7} CPU {p['CPU']:<8} RAM {p['RAM_MB']} MB  started {p['StartTime']}")

    # --- Long-running unknowns (over 24h, not system) ---
    lines.append("\n[LONG-RUNNING UNKNOWN PROCESSES (>24h)]")
    flagged = []
    for p in procs:
        if p["Name"].lower() in SYSTEM_PROCESS_NAMES:
            continue
        days = age_days(p["StartTime"])
        if days is not None and days >= 1:
            cmd = p.get("CommandLine") or ""
            if not cmd:
                flagged.append((days, p))
    flagged.sort(key=lambda x: x[0], reverse=True)
    if flagged:
        for days, p in flagged:
            lines.append(f"  {p['Name']:<25} PID {p['Id']:<7} age {days}d  CPU {p['CPU']}")
    else:
        lines.append("  none")

    # --- High active CPU (top 10 non-system) ---
    lines.append("\n[TOP CPU CONSUMERS]")
    top = sorted(
        [p for p in procs if p["Name"].lower() not in SYSTEM_PROCESS_NAMES],
        key=lambda x: x["CPU"] or 0,
        reverse=True
    )[:10]
    for p in top:
        lines.append(f"  {p['Name']:<25} PID {p['Id']:<7} CPU {p['CPU']:<10} RAM {p['RAM_MB']} MB")

    # --- High RAM consumers ---
    lines.append("\n[TOP RAM CONSUMERS]")
    top_ram = sorted(
        [p for p in procs if p["Name"].lower() not in SYSTEM_PROCESS_NAMES],
        key=lambda x: x["RAM_MB"] or 0,
        reverse=True
    )[:10]
    for p in top_ram:
        lines.append(f"  {p['Name']:<25} PID {p['Id']:<7} RAM {p['RAM_MB']:<10} MB  CPU {p['CPU']}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)

def main():
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    print("Collecting process data...")
    procs = get_processes()
    report = build_report(procs)
    print(report)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\nReport saved to {REPORT_PATH}")

if __name__ == "__main__":
    main()
