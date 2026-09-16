#!/usr/bin/env python3
"""
CloudMark Vultr Free Tier Automatic Deletion Script
Checks if the current date is on or after the safety threshold (August 30, 2027).
If so, deletes the free tier instance (74e74adf-df0d-4e45-808d-37b9fdabb7aa)
to guarantee zero surprise billing 2 weeks before the 1-year deadline.
"""

import sys
import os
import subprocess
import json
from datetime import datetime, timezone
from pathlib import Path

# Target details
TARGET_INSTANCE_ID = "74e74adf-df0d-4e45-808d-37b9fdabb7aa"
TARGET_LABEL = "vultr-free-fra-01"
PROGRAM_EXPIRATION_UTC = datetime(2027, 9, 13, 0, 0, 0, tzinfo=timezone.utc)
SAFETY_DELETE_UTC = datetime(2027, 8, 30, 0, 0, 0, tzinfo=timezone.utc)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
VULTR_CLI = str(BASE_DIR / "bin" / "vultr" / "vultr-cli.exe")
LOG_PATH = BASE_DIR / "runs" / "free_tier_lifecycle.log"

def log(msg):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{now}] {msg}"
    print(line)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def main():
    force = "--force" in sys.argv
    now = datetime.now(timezone.utc)
    log(f"Auto-delete check invoked. Current UTC: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    if not force and now < SAFETY_DELETE_UTC:
        days_remaining = (SAFETY_DELETE_UTC - now).days
        log(f"Safety threshold date is {SAFETY_DELETE_UTC.strftime('%Y-%m-%d')}. Not deleting yet.")
        log(f"Days remaining until scheduled auto-deletion: {days_remaining} days.")
        log(f"Free Tier program deadline: {PROGRAM_EXPIRATION_UTC.strftime('%Y-%m-%d')}.")
        return

    log(f"Safety threshold reached (or --force specified). Checking active instances...")
    
    # Check if instance is alive
    res = subprocess.run([VULTR_CLI, "instance", "list", "-o", "json"], capture_output=True, text=True)
    if res.returncode != 0:
        log(f"ERROR: vultr-cli instance list failed: {res.stderr.strip()}")
        return

    try:
        data = json.loads(res.stdout)
        instances = data.get("instances", [])
    except Exception as e:
        log(f"Failed to parse instance list JSON: {e}")
        return

    target = None
    for inst in instances:
        if inst.get("id") == TARGET_INSTANCE_ID or inst.get("label") == TARGET_LABEL:
            target = inst
            break

    if not target:
        log(f"Target instance ({TARGET_INSTANCE_ID}) is NOT found in active instances.")
        log("The instance has already been destroyed. Zero billing risk confirmed!")
        return

    log(f"Found active instance: {target.get('label')} ({target.get('id')}) at IP {target.get('main_ip')}.")
    log(f"Deleting instance {TARGET_INSTANCE_ID} to prevent billing conversion...")

    del_res = subprocess.run([VULTR_CLI, "instance", "delete", TARGET_INSTANCE_ID], capture_output=True, text=True)
    if del_res.returncode == 0:
        log(f"SUCCESS: Vultr instance {TARGET_INSTANCE_ID} has been permanently deleted!")
        log("Safety auto-deletion completed with zero billing exposure.")
    else:
        log(f"ERROR: Failed to delete instance: {del_res.stderr.strip()}")

if __name__ == "__main__":
    main()
