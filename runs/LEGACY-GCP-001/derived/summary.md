# CloudMark Benchmark Summary: LEGACY-GCP-001
Generated: 2026-09-13 11:18:49 UTC

## 1. System Metadata
- **run_id**: `LEGACY-GCP-001`
- **machine_id**: `gcp-uswest1a-e2micro-01`
- **protocol_version**: `CBP-0`
- **status**: `historical_provisional`
- **provider**: `Google Cloud Platform`
- **region**: `us-west1`
- **zone**: `us-west1-a`
- **instance_family**: `e2`
- **exact_plan_or_shape**: `e2-micro`
- **exposed_vcpu_count**: `2`
- **provider_cpu_classification**: `shared_core`
- **cpu_model**: `Intel Xeon / AMD EPYC (variable shared)`
- **cpu_architecture**: `x86_64`
- **virtualization_type**: `KVM`
- **ram_gb**: `1.0`
- **root_disk_type**: `pd-standard`
- **root_disk_size_gb**: `30`
- **os_distribution**: `unknown`
- **os_version**: `unknown`
- **kernel_version**: `unknown`
- **pg_version**: `18`
- **pricing**: `{'currency': 'USD', 'hourly': 0.0, 'monthly_equivalent': 0.0, 'promotional_or_free_tier': True, 'notes': 'Google Cloud Always Free Tier allocation'}`
- **notes**: `Provisional exploratory baseline. Valid for engineering ballpark; not formal CBP-1.0 statistical comparison.`

## 2. CPU Performance

## 3. PostgreSQL OLTP Performance
| Test ID | Workload | Scale | Clients | Whole-run TPS | Sustained TPS | Latency (ms) | Failures |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T052 | mixed_tpc_b | 10 | 1 | 128.9 | 90.3 | 11.0 | 0 |
| T052 | mixed_tpc_b | 10 | 4 | 397.1 | 180.6 | 22.0 | 0 |
| T052 | mixed_tpc_b | 10 | 8 | 435.6 | 191.0 | 43.0 | 0 |
| T052 | mixed_tpc_b | 10 | 16 | 413.8 | 180.1 | 93.5 | 0 |
| T053 | select_only | 10 | 1 | 2030.0 | 746.6 | 1.35 | 0 |