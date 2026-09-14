#!/usr/bin/env python3
"""
CBP-1.0 Parser for T001 (Machine and Environment Characterization).
Parses raw T001 log, updates metadata.json, updates master/runs.csv,
and appends to master/machines.csv.
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

    # Extract OS and Kernel
    kernel_match = re.search(r"Linux\s+\S+\s+([\d\.\-\w]+)", log_content)
    kernel_ver = kernel_match.group(1) if kernel_match else "unknown"

    os_name_match = re.search(r'PRETTY_NAME="([^"]+)"', log_content)
    os_distro = os_name_match.group(1) if os_name_match else "Linux"

    # Extract Root Disk Type
    if "PersistentDisk" in log_content:
        root_disk_type = "pd-standard"
    elif "nvme" in log_content.lower():
        root_disk_type = "NVMe"
    else:
        root_disk_type = "SSD"

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
        "root_disk_type": root_disk_type,
        "root_disk_size_gb": root_disk_size,
        "virt_type": virt_type,
        "kernel_version": kernel_ver,
        "os_distro": os_distro
    }

    # 1. Update run metadata.json if present
    run_dir = Path("d:/Projects/CloudMark/runs") / run_id
    meta_path = run_dir / "metadata.json"
    if meta_path.exists():
        try:
            curr_meta = json.loads(meta_path.read_text(encoding="utf-8"))
            curr_meta.update(parsed)
            meta_path.write_text(json.dumps(curr_meta, indent=2), encoding="utf-8")
        except Exception as e:
            print(f"Warning: Could not update metadata.json: {e}")

    # 2. Update or append to master/machines.csv
    master_csv = Path("d:/Projects/CloudMark/master/machines.csv")
    new_row = [
        parsed["machine_id"], parsed["provider"], parsed["region"],
        parsed["zone"], parsed["plan_name"], parsed["instance_family"],
        parsed["cpu_arch"], parsed["cpu_model"], parsed["exposed_vcpu"],
        parsed["ram_gb"], parsed["root_disk_type"], parsed["root_disk_size_gb"],
        parsed["virt_type"]
    ]
    if master_csv.exists():
        rows = []
        found = False
        with open(master_csv, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header:
                rows.append(header)
            for row in reader:
                if row and row[0] == machine_id:
                    rows.append(new_row)
                    found = True
                elif row:
                    rows.append(row)
        if not found:
            rows.append(new_row)
        with open(master_csv, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

    # 3. Update OS / Kernel in master/runs.csv
    runs_csv = Path("d:/Projects/CloudMark/master/runs.csv")
    if runs_csv.exists():
        rows = []
        updated = False
        with open(runs_csv, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for r in reader:
                if r.get("run_id") == run_id:
                    r["os_distro"] = os_distro
                    r["kernel_version"] = kernel_ver
                    updated = True
                rows.append(r)
        if updated:
            with open(runs_csv, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

    print(json.dumps(parsed, indent=2))
    return parsed

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Usage: parse_t001.py <raw_log_path> <run_id> <machine_id> <provider> <region> <plan_name>")
        sys.exit(1)
    parse_t001(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
