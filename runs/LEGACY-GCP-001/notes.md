# LEGACY-GCP-001 — Historical Baseline Record

- **Run ID:** `LEGACY-GCP-001`
- **Protocol:** `CBP-0` (Exploratory / Legacy)
- **Provider:** Google Cloud Platform
- **Instance:** `e2-micro` (us-west1-a)
- **Specs:** 2 vCPU (shared-core), ~1 GB RAM, 30 GB `pd-standard`
- **PostgreSQL Version:** 18
- **Working Set:** pgbench scale 10

## Key Observations

1. **Burst vs. Sustained Degradation**:
   - Mixed OLTP exhibited substantial early burst capability (~475 to 1,634 TPS across 1 to 16 clients) before degrading to a steady-state of ~90 to 191 TPS once CPU burst credits were depleted.
   - SELECT-only single-client burst was ~6,383 TPS before falling to ~746.6 TPS sustained.

2. **Scaling Ceiling**:
   - Mixed-workload throughput plateaued between 4 and 8 concurrent clients on this shared-core VM, dropping slightly at 16 clients due to CPU/disk starvation.

3. **Transaction Reliability**:
   - Zero transaction failures observed across all executed runs.

4. **Protocol Limitations**:
   - Unstandardized test run lengths; manual sustained calculation; lack of raw time-series files for all subtests.
   - Preserved as a historical baseline; to be re-run under frozen CBP-1.0.
