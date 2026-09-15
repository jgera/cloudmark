#!/usr/bin/env python3
"""
CBP-1.0 Parser for Storage Benchmarks (T031, T032, T033).
Extracts read/write IOPS, bandwidth (MB/s), average latency,
and appends derived metrics to master/storage_results.csv.
"""

import sys
import re
import csv
from pathlib import Path

def parse_fio_section(section_text: str):
    # Match IOPS e.g. IOPS=15.4k or IOPS=4520
    iops = 0.0
    bw_mb_s = 0.0
    lat_ms = 0.0

    iops_match = re.search(r"IOPS=([\d\.]+)([kK]?)", section_text)
    if iops_match:
        val = float(iops_match.group(1))
        if iops_match.group(2).lower() == "k":
            val *= 1000
        iops = round(val, 1)

    bw_match = re.search(r"BW=([\d\.]+)([M|G|K|m|g|k]i?B/s)", section_text)
    if bw_match:
        val = float(bw_match.group(1))
        unit = bw_match.group(2).lower()
        if "g" in unit:
            val *= 1024
        elif "k" in unit:
            val /= 1024
        bw_mb_s = round(val, 2)

    # Match avg latency in usec or msec
    lat_match = re.search(r"(?:lat|clat)\s*\(([um]sec)\):\s*min=[\d\.]+, max=[\d\.]+, avg=([\d\.]+)", section_text)
    if lat_match:
        unit = lat_match.group(1)
        val = float(lat_match.group(2))
        if unit == "usec":
            lat_ms = round(val / 1000.0, 3)
        else:
            lat_ms = round(val, 3)

    return iops, bw_mb_s, lat_ms

def parse_storage_log(raw_log_path: str, run_id: str, test_id: str):
    log_content = Path(raw_log_path).read_text(encoding="utf-8", errors="replace")
    master_csv = Path("d:/Projects/CloudMark/master/storage_results.csv")

    rows_to_add = []

    # Split into sections based on test parts
    parts = re.split(r"--- Part \d+:\s*(.+?) ---", log_content)
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            part_title = parts[i].strip()
            part_body = parts[i+1]

            # Determine read or write or mixed
            read_iops, read_bw, read_lat = 0.0, 0.0, 0.0
            write_iops, write_bw, write_lat = 0.0, 0.0, 0.0

            read_sec = re.search(r"read:\s*IOPS=.*?(?=\n\s*(?:write:|$))", part_body, re.DOTALL)
            if read_sec:
                read_iops, read_bw, read_lat = parse_fio_section(read_sec.group(0))

            write_sec = re.search(r"write:\s*IOPS=.*?(?=\n\s*(?:read:|$))", part_body, re.DOTALL)
            if write_sec:
                write_iops, write_bw, write_lat = parse_fio_section(write_sec.group(0))

            avg_lat = max(read_lat, write_lat)
            block_size = "1M" if "1MB" in part_title or "1M" in part_title else "4k"
            queue_depth = "32" if "iodepth=32" in part_title else ("16" if "iodepth=16" in part_title else "unknown")

            rows_to_add.append([
                run_id, test_id, part_title, block_size, queue_depth,
                read_iops, write_iops, read_bw, write_bw, avg_lat,
                Path(raw_log_path).name
            ])

    if rows_to_add:
        existing_keys = set()
        if master_csv.exists():
            with open(master_csv, mode="r", encoding="utf-8") as f:
                for r in csv.reader(f):
                    if len(r) >= 3:
                        existing_keys.add((r[0], r[1], r[2]))

        filtered_rows = [r for r in rows_to_add if (r[0], r[1], r[2]) not in existing_keys]
        if filtered_rows:
            with open(master_csv, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(filtered_rows)
            for r in filtered_rows:
                print(f"[{test_id}] Parsed: {r[2]} -> R_IOPS={r[5]}, W_IOPS={r[6]}, R_BW={r[7]}MB/s, W_BW={r[8]}MB/s, Lat={r[9]}ms")
        else:
            print(f"[{test_id}] Storage rows already present in master dataset. Skipping duplicate append.")
    else:
        print(f"[{test_id}] No fio sections matched in {raw_log_path}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: parse_storage.py <raw_log_path> <run_id> <test_id>")
        sys.exit(1)
    parse_storage_log(sys.argv[1], sys.argv[2], sys.argv[3])
