# CloudMark — Cross-Provider Cloud Benchmarking Suite

**CloudMark** is a long-term, provider-neutral benchmarking framework designed to measure, analyze, and compare the real-world performance of cloud virtual machines, VPS platforms, free-tier instances, and bare-metal servers.

The current frozen benchmarking protocol is **CBP-1.0** (Cloud Benchmark Protocol v1.0).

---

## 1. Core Operating Principles

1. **Identical Protocol Across Providers**: The core battery is executed identically across GCP, Vultr, OCI, Hetzner, AWS, Azure, and bare metal.
2. **Separation of Raw and Derived Data**: Unmodified stdout/stderr streams are captured and preserved under `runs/<run_id>/raw/`. Derived metrics are extracted by deterministic parsers and logged to `master/*.csv`.
3. **Sustained Over Headline Burst**: CPU burst degradation, IOPS burst limits, and PostgreSQL steady-state TPS are systematically distinguished from short-term peak burst credits.
4. **Zero Pre-Benchmark Tuning**: Out-of-the-box vendor configurations (kernels, sysctl, PostgreSQL defaults) are profiled first before any tuning is applied.
5. **No Discarding of Anomalies**: High variability or unexpected results are documented, not rerun to hit desired scores.

---

## 2. Directory Layout

```text
CloudMark/
├── protocol/
│   ├── CBP-1.0.md                  # Standardized protocol specification
│   └── CHANGELOG.md                # Protocol evolution & version tracking
│
├── master/                         # Central cumulative datasets (CSV)
│   ├── machines.csv                # Hardware, vCPU, RAM, architecture, virtualization
│   ├── runs.csv                    # Run records, OS/kernel versions, timestamps
│   ├── cpu_results.csv             # Single, multi-core, and sustained burst/sustained metrics
│   ├── memory_results.csv          # Read & write memory bandwidth and latency
│   ├── storage_results.csv         # Sequential & random IOPS, bandwidth, latency
│   ├── network_results.csv         # Throughput & client-side RTT/packet loss
│   ├── postgres_results.csv        # Mixed OLTP and SELECT-only concurrency scaling
│   └── pricing.csv                 # Hourly/monthly pricing and price/TPS economics
│
├── runs/
│   ├── LEGACY-GCP-001/             # Historical baseline (CBP-0 / exploratory)
│   └── <run_id>/                   # Per-run execution directory
│       ├── raw/                    # Exact, unmodified command outputs
│       ├── derived/                # Structured summaries and reports
│       └── metadata.json           # Instance and execution parameters
│
├── scripts/
│   ├── benchmark/                  # CBP-1.0 remote execution scripts
│   │   ├── setup_node.sh           # Default tool & package provisioning
│   │   ├── t001_characterization.sh
│   │   ├── t002_idle_baseline.sh
│   │   ├── t010_cpu_single.sh
│   │   ├── t011_cpu_multi.sh
│   │   ├── t012_cpu_sustained.sh   # 300s time-series CPU test
│   │   ├── t020_memory.sh
│   │   ├── t030_storage_id.sh
│   │   ├── t031_storage_seq.sh
│   │   ├── t032_storage_rand.sh
│   │   ├── t033_storage_sustained.sh
│   │   ├── t040_network_throughput.sh
│   │   ├── t041_client_rtt.ps1     # Client-to-server RTT probe
│   │   ├── t050_postgres_env.sh
│   │   ├── t051_pg_init_s10.sh
│   │   ├── t052_pg_oltp_scale.sh   # Concurrency series: 1, 4, 8, 16, 32
│   │   ├── t053_pg_select_scale.sh
│   │   ├── t054_pg_init_s100.sh
│   │   └── t055_pg_monitored.sh    # PostgreSQL with concurrent vmstat/iostat
│   │
│   ├── parsers/                    # Metric extraction routines
│   │   ├── parse_t001.py
│   │   ├── parse_cpu.py
│   │   ├── parse_memory.py
│   │   ├── parse_storage.py
│   │   ├── parse_postgres.py
│   │   └── parse_network.py
│   │
│   └── orchestrator/
│       ├── vultr_ops.ps1           # Vultr cloud CLI operations
│       └── cloudmark_runner.py     # Master benchmark execution engine
```

---

## 3. Orchestration & Usage

### 3.1 Initializing a Benchmark Run
```bash
python scripts/orchestrator/cloudmark_runner.py init-run <run_id> <provider> <region> <plan_name> <monthly_usd>
```
*Example:*
```bash
python scripts/orchestrator/cloudmark_runner.py init-run 2026-09-13_vultr_delhi_hp-4c8g_run01 Vultr Delhi vhp-4c-8gb 48.00
```

### 3.2 Setting Up the Target Node
```bash
python scripts/orchestrator/cloudmark_runner.py setup-node <run_id> <host_ip> [--key-path <path>]
```

### 3.3 Executing Benchmark Tests (One at a Time)
```bash
python scripts/orchestrator/cloudmark_runner.py run-test <run_id> <test_id> <host_ip> [--key-path <path>]
```
*Test IDs:* `T001`, `T002`, `T010`, `T011`, `T012`, `T020`, `T030`, `T031`, `T032`, `T033`, `T040`, `T050`, `T051`, `T052`, `T053`, `T054`, `T055`.

### 3.4 Client RTT Probe
```bash
python scripts/orchestrator/cloudmark_runner.py run-client-rtt <run_id> <host_ip>
```

### 3.5 Checking Run Progress & Generating Summary
```bash
# Check test completion status
python scripts/orchestrator/cloudmark_runner.py status <run_id>

# Generate derived Markdown report
python scripts/orchestrator/cloudmark_runner.py report <run_id>
```
