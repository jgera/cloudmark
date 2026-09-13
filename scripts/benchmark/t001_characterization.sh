#!/usr/bin/env bash
# CBP-1.0 / T001 — Machine and Environment Characterization
# CloudMark Benchmark Suite

set -euo pipefail

echo "========================================="
echo "=== CBP-1.0 / T001: SYSTEM CHARACTERIZATION ==="
echo "=== Timestamp (UTC): $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "========================================="

echo -e "\n--- UNAME ---"
uname -a

echo -e "\n--- OS RELEASE ---"
cat /etc/os-release

echo -e "\n--- CPU ARCHITECTURE & DETAILS (lscpu) ---"
lscpu

echo -e "\n--- DETECTED CORES (nproc) ---"
nproc

echo -e "\n--- MEMORY (free -h) ---"
free -h

echo -e "\n--- MEMORY DETAILED (cat /proc/meminfo) ---"
head -n 25 /proc/meminfo

echo -e "\n--- BLOCK DEVICES (lsblk) ---"
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,ROTA,MODEL,DISC-MAX,DISC-ZERO

echo -e "\n--- FILESYSTEM DISK USAGE (df -hT) ---"
df -hT

echo -e "\n--- MOUNT DETAILS ---"
mount | grep -E '^/dev'

echo -e "\n--- VIRTUALIZATION DETECTION ---"
if command -v systemd-detect-virt &>/dev/null; then
    systemd-detect-virt || true
else
    echo "systemd-detect-virt not installed"
fi

echo -e "\n--- DMI SYSTEM INFO (dmidecode proxy if readable) ---"
if [ -f /sys/class/dmi/id/product_name ]; then
    echo "Product Name: $(cat /sys/class/dmi/id/product_name 2>/dev/null || echo 'N/A')"
    echo "Sys Vendor:   $(cat /sys/class/dmi/id/sys_vendor 2>/dev/null || echo 'N/A')"
    echo "BIOS Version: $(cat /sys/class/dmi/id/bios_version 2>/dev/null || echo 'N/A')"
fi

echo -e "\n========================================="
echo "=== T001 CHARACTERIZATION COMPLETE ==="
echo "========================================="
