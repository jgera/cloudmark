#!/usr/bin/env python3
"""
CBP-1.0 Parser for Network Benchmarks (T041).
Extracts min/avg/max RTT and packet loss, and appends to master/network_results.csv.
"""

import sys
import re
import csv
from pathlib import Path

def parse_network_log(raw_log_path: str, run_id: str, test_id: str, client_location: str = "North India"):
    log_content = Path(raw_log_path).read_text(encoding="utf-8", errors="replace")
    master_csv = Path("d:/Projects/CloudMark/master/network_results.csv")

    # Extract target host
    target_match = re.search(r"=== Target IP:\s*(.+?)\s*===", log_content)
    target_ip = target_match.group(1).strip() if target_match else "remote_vm"

    # Extract packet loss
    loss_match = re.search(r"\((\d+)%\s*loss\)", log_content)
    loss_pct = float(loss_match.group(1)) if loss_match else 0.0

    # Extract min, max, avg
    rtt_match = re.search(r"Minimum\s*=\s*(\d+)ms,\s*Maximum\s*=\s*(\d+)ms,\s*Average\s*=\s*(\d+)ms", log_content)
    if rtt_match:
        min_rtt = float(rtt_match.group(1))
        max_rtt = float(rtt_match.group(2))
        avg_rtt = float(rtt_match.group(3))
    else:
        # Fallback for Linux ping output format if used
        linux_match = re.search(r"rtt min/avg/max/mdev =\s*([\d\.]+)/([\d\.]+)/([\d\.]+)/", log_content)
        if linux_match:
            min_rtt = float(linux_match.group(1))
            avg_rtt = float(linux_match.group(2))
            max_rtt = float(linux_match.group(3))
        else:
            min_rtt, avg_rtt, max_rtt = 0.0, 0.0, 0.0

    with open(master_csv, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            run_id, test_id, f"ping_to_{target_ip}", client_location,
            "bidirectional_rtt", "N/A", 0, min_rtt, avg_rtt, max_rtt,
            loss_pct, Path(raw_log_path).name
        ])

    print(f"[{test_id}] Parsed: Target={target_ip}, Min={min_rtt}ms, Avg={avg_rtt}ms, Max={max_rtt}ms, Loss={loss_pct}%")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: parse_network.py <raw_log_path> <run_id> <test_id> [client_location]")
        sys.exit(1)
    loc = sys.argv[4] if len(sys.argv) > 4 else "North India"
    parse_network_log(sys.argv[1], sys.argv[2], sys.argv[3], loc)
