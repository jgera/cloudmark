#!/usr/bin/env bash
# CBP-1.0 / T030 — Storage Identification
# Inspect block device, filesystem, scheduler, queue depth, rotational state

set -euo pipefail

echo "========================================="
echo "=== CBP-1.0 / T030: STORAGE IDENTIFICATION ==="
echo "=== Timestamp (UTC): $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "========================================="

echo -e "\n--- Block Device Hierarchy (lsblk) ---"
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,ROTA,MODEL,DISC-MAX,DISC-ZERO

echo -e "\n--- Mount Options ---"
mount | grep -E '^/dev'

echo -e "\n--- Disk Free (df -hT) ---"
df -hT

echo -e "\n--- Sysfs Disk Queue & Scheduler ---"
for dev in /sys/block/*; do
    devname=$(basename "$dev")
    # Skip loop and ram devices
    if [[ "$devname" =~ ^(loop|ram) ]]; then continue; fi
    echo "Device: $devname"
    [ -f "$dev/queue/scheduler" ] && echo "  scheduler: $(cat "$dev/queue/scheduler")"
    [ -f "$dev/queue/nr_requests" ] && echo "  nr_requests: $(cat "$dev/queue/nr_requests")"
    [ -f "$dev/queue/rotational" ] && echo "  rotational (0=SSD/NVMe, 1=HDD): $(cat "$dev/queue/rotational")"
    [ -f "$dev/queue/read_ahead_kb" ] && echo "  read_ahead_kb: $(cat "$dev/queue/read_ahead_kb")"
done

echo -e "\n========================================="
echo "=== T030 COMPLETE ==="
echo "========================================="
