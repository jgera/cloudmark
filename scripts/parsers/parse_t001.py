#!/usr/bin/env python3
"""
CBP-1.0 Parser for T001 (Machine and Environment Characterization).
Parses raw T001 log, updates metadata.json, and appends to master/machines.csv.
"""

import sys
import re
import json
import csv
from pathlib import Path

def parse_t001(raw_log_path: str, run_id: str, machine_id: str, provider: str, region: str, plan_name: str):
    log_content = Path(raw_log_path).read_text(encoding="utf-8", errors="replace")

    # Extract CPU model
    cpu_model_match = re.search(r"Model name:\s*(.+)", log_content)
    cpu_model = cpu_model_match.group(1).strip() if cpu_model_match else "unknown"

    # Extract CPU architecture
    arch_match = re.search(r"Architecture:\s*(.+)", log_content)
    cpu_arch = arch_match.group(1).strip() if arch_match else "unknown"

    # Extract exposed vCPU count
    vcpu_match = re.search(r"CPU\(s\):\s*(\d+)", log_content)
    exposed_vcpu = int(vcpu_match.group(1)) if vcpu_match else 1

    # Extract Total RAM in GB
    mem_match = re.search(r"MemTotal:\s*(\d+)\s*kB", log_content)
    if mem_match:
        ram_gb = round(int(mem_match.group(1)) / (1024 * 1024), 2)
    else:
        # Fallback to free -h output
        mem_free_match = re.search(r"Mem:\s+([0-9\.]+[GMK]i?)", log_content)
        ram_gb = mem_free_match.group(1) if mem_free_match else "unknown"

    # Extract Root Disk
    disk_match = re.search(r"(\w+)\s+(\d+[G|M|T]?)\s+disk", log_content)
    root_disk_size = disk_match.group(2) if disk_match else "unknown"

    # Extract Virtualization
    virt_match = re.search(r"Hypervisor vendor:\s*(.+)", log_content)
    virt_type = virt_match.group(1).strip() if virt_match else "unknown"
    if virt_type == "unknown":
        virt_line = re.search(r"--- VIRTUALIZATION DETECTION ---\n(\w+)", log_content)
        if virt_line:
            virt_type = virt_line.group(1).strip()

    parsed = {
        "machine_id": machine_id,
        "provider": provider,
        "region": region,
        "zone": "default",
        "plan_name": plan_name,
        "instance_family": plan_name.split("-")[0] if "-" in plan_name else plan_name,
        "cpu_arch": cpu_arch,
        "cpu_model": cpu_model,
        "exposed_vcpu": exposed_vcpu,
        "ram_gb": ram_gb,
        "root_disk_type": "NVMe/SSD",
        "root_disk_size_gb": root_disk_size,
        "virt_type": virt_type
    }

    # Append to master/machines.csv if not present
    master_csv = Path("d:/Projects/CloudMark/master/machines.csv")
    existing_ids = set()
    if master_csv.exists():
        with open(master_csv, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_ids.add(row.get("machine_id"))

    if machine_id not in existing_ids:
        with open(master_csv, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                parsed["machine_id"], parsed["provider"], parsed["region"],
                parsed["zone"], parsed["plan_name"], parsed["instance_family"],
                parsed["cpu_arch"], parsed["cpu_model"], parsed["exposed_vcpu"],
                parsed["ram_gb"], parsed["root_disk_type"], parsed["root_disk_size_gb"],
                parsed["virt_type"]
            ])

    print(json.dumps(parsed, indent=2))
    return parsed

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Usage: parse_t001.py <raw_log_path> <run_id> <machine_id> <provider> <region> <plan_name>")
        sys.exit(1)
    parse_t001(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
