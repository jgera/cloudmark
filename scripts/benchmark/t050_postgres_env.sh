#!/usr/bin/env bash
# CBP-1.0 / T050 — PostgreSQL Environment Capture
# Records PostgreSQL version, data directory filesystem, and default configuration parameters

set -euo pipefail

echo "========================================="
echo "=== CBP-1.0 / T050: POSTGRESQL ENVIRONMENT CAPTURE ==="
echo "=== Timestamp (UTC): $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "========================================="

echo -e "\n--- Versions ---"
psql --version
pgbench --version

echo -e "\n--- Service Status ---"
systemctl status postgresql --no-pager | head -n 15

echo -e "\n--- PostgreSQL Engine Version ---"
sudo -u postgres psql -t -A -c "SELECT version();"

echo -e "\n--- Data Directory & Mount ---"
DATA_DIR=$(sudo -u postgres psql -t -A -c "SHOW data_directory;")
echo "Data Directory: $DATA_DIR"
df -hT "$DATA_DIR"

echo -e "\n--- Key PostgreSQL Performance Settings (Out-of-the-Box Defaults) ---"
sudo -u postgres psql -c "
SELECT name, setting, unit, source 
FROM pg_settings 
WHERE name IN (
    'shared_buffers',
    'work_mem',
    'maintenance_work_mem',
    'effective_cache_size',
    'wal_buffers',
    'checkpoint_completion_target',
    'max_wal_size',
    'min_wal_size',
    'synchronous_commit',
    'fsync',
    'max_connections',
    'max_worker_processes',
    'max_parallel_workers',
    'max_parallel_workers_per_gather'
) ORDER BY name;
"

# Ensure cloudmark database and user exist for benchmarking
sudo -u postgres psql -c "CREATE DATABASE cloudmark;" 2>/dev/null || true

echo -e "\n========================================="
echo "=== T050 COMPLETE ==="
echo "========================================="
