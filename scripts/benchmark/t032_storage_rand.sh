#!/usr/bin/env bash
# CBP-1.0 / T032 — Random Storage IOPS and Latency
# Standardized 4 KiB random I/O testing using fio

set -euo pipefail

TEST_DIR="/var/tmp/fio_test"
mkdir -p "$TEST_DIR"
TEST_FILE="$TEST_DIR/testfile_rand.dat"

echo "========================================="
echo "=== CBP-1.0 / T032: RANDOM STORAGE IOPS & LATENCY ==="
echo "=== Timestamp (UTC): $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "========================================="

echo -e "\n--- Part 1: Random Read (4K, iodepth=32, numjobs=4) ---"
fio --name=rand_read \
    --filename="$TEST_FILE" \
    --size=4G \
    --bs=4k \
    --direct=1 \
    --rw=randread \
    --ioengine=libaio \
    --iodepth=32 \
    --numjobs=4 \
    --runtime=60 \
    --time_based \
    --group_reporting \
    --output-format=normal

echo -e "\n--- Part 2: Random Write (4K, iodepth=32, numjobs=4) ---"
fio --name=rand_write \
    --filename="$TEST_FILE" \
    --size=4G \
    --bs=4k \
    --direct=1 \
    --rw=randwrite \
    --ioengine=libaio \
    --iodepth=32 \
    --numjobs=4 \
    --runtime=60 \
    --time_based \
    --group_reporting \
    --output-format=normal

echo -e "\n--- Part 3: Mixed Random 70/30 (4K, iodepth=32, numjobs=4) ---"
fio --name=rand_rw7030 \
    --filename="$TEST_FILE" \
    --size=4G \
    --bs=4k \
    --direct=1 \
    --rw=randrw \
    --rwmixread=70 \
    --ioengine=libaio \
    --iodepth=32 \
    --numjobs=4 \
    --runtime=60 \
    --time_based \
    --group_reporting \
    --output-format=normal

rm -f "$TEST_FILE"

echo -e "\n========================================="
echo "=== T032 COMPLETE ==="
echo "========================================="
