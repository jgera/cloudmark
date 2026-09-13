#!/usr/bin/env bash
# CBP-1.0 / T054 — Larger PostgreSQL Working Set (Scale 100 Initialization)
# Scale 100 represents ~1.5 GB database footprint, reducing trivial cache effects

set -euo pipefail

echo "========================================="
echo "=== CBP-1.0 / T054: POSTGRESQL INIT SCALE 100 ==="
echo "=== Timestamp (UTC): $(date -u '+%Y-%m-%d %H:%M:%S UTC') ==="
echo "========================================="

echo "Initializing pgbench database at scale 100..."
sudo -u postgres pgbench -i -s 100 -I dtgvp cloudmark

echo -e "\n--- Database & Relation Sizes (Scale 100) ---"
sudo -u postgres psql -d cloudmark -c "
SELECT 
    relname AS table_name,
    pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
    pg_size_pretty(pg_relation_size(relid)) AS data_size,
    pg_size_pretty(pg_indexes_size(relid)) AS index_size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
"

echo -e "\n--- Total Database Size ---"
sudo -u postgres psql -d cloudmark -t -A -c "SELECT pg_size_pretty(pg_database_size('cloudmark'));"

echo -e "\n========================================="
echo "=== T054 COMPLETE ==="
echo "========================================="
