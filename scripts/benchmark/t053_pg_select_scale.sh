#!/usr/bin/env bash
# CBP-1.0 / T053 — SELECT-Only Concurrency Scaling
# Tests cache and CPU read ceiling across: 1, 4, 8, 16, 32 clients

set -euo pipefail

DURATION=120
CLIENTS_SERIES=(1 4 8 16 32)
CORES=$(nproc)

echo "========================================="
echo "=== CBP-1.0 / T053: SELECT-ONLY SCALING (Scale 10) ==="
echo "=== Duration per test: ${DURATION}s, Interval: 5s ==="
echo "=== Timestamp (UTC): $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "========================================="

for c in "${CLIENTS_SERIES[@]}"; do
    threads=$(( c < CORES ? c : CORES ))
    if [ "$threads" -lt 1 ]; then threads=1; fi

    echo -e "\n------------------------------------------------------------"
    echo "=== Running SELECT-Only: Clients=$c, Threads=$threads, Duration=${DURATION}s ==="
    echo "------------------------------------------------------------"

    sudo -u postgres pgbench -S -c "$c" -j "$threads" -T "$DURATION" -P 5 -r cloudmark

    sleep 5
done

echo -e "\n========================================="
echo "=== T053 COMPLETE ==="
echo "========================================="
