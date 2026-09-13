#!/usr/bin/env bash
# CBP-1.0 / T031 — Sequential Storage Throughput
# Large-block sequential read and write performance using fio

set -euo pipefail

TEST_DIR="/var/tmp/fio_test"
mkdir -p "$TEST_DIR"
TEST_FILE="$TEST_DIR/testfile_seq.dat"

echo "========================================="
echo "=== CBP-1.0 / T031: SEQUENTIAL STORAGE THROUGHPUT ==="
echo "=== Timestamp (UTC): $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "========================================="

echo -e "\n--- Part 1: Sequential Write (1MB, iodepth=16, direct=1) ---"
fio --name=seq_write \
    --filename="$TEST_FILE" \
    --size=4G \
    --bs=1M \
    --direct=1 \
    --rw=write \
    --ioengine=libaio \
    --iodepth=16 \
    --runtime=60 \
    --time_based \
    --group_reporting \
    --output-format=normal

echo -e "\n--- Part 2: Sequential Read (1MB, iodepth=16, direct=1) ---"
fio --name=seq_read \
    --filename="$TEST_FILE" \
    --size=4G \
    --bs=1M \
    --direct=1 \
    --rw=read \
    --ioengine=libaio \
    --iodepth=16 \
    --runtime=60 \
    --time_based \
    --group_reporting \
    --output-format=normal

rm -f "$TEST_FILE"

echo -e "\n========================================="
echo "=== T031 COMPLETE ==="
echo "========================================="
