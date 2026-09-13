#!/usr/bin/env bash
# CBP-1.0 / T033 — Sustained Storage Behavior
# Controlled 300s random write test to detect IOPS burst exhaustion or throttling

set -euo pipefail

TEST_DIR="/var/tmp/fio_test"
mkdir -p "$TEST_DIR"
TEST_FILE="$TEST_DIR/testfile_sustained.dat"

echo "========================================="
echo "=== CBP-1.0 / T033: SUSTAINED STORAGE BEHAVIOR (300s) ==="
echo "=== Timestamp (UTC): $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "========================================="

echo "Running 300s sustained random write test with periodic status logging..."
fio --name=sustained_write \
    --filename="$TEST_FILE" \
    --size=4G \
    --bs=4k \
    --direct=1 \
    --rw=randwrite \
    --ioengine=libaio \
    --iodepth=16 \
    --numjobs=2 \
    --runtime=300 \
    --time_based \
    --status-interval=5 \
    --group_reporting \
    --output-format=normal

rm -f "$TEST_FILE"

echo -e "\n========================================="
echo "=== T033 COMPLETE ==="
echo "========================================="
