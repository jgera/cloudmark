# CloudMark Benchmark Summary: 2026-09-13_vultr_delhi_hp-4c8g-intel_run01
Generated: 2026-09-13 12:28:05 UTC

## 1. System Metadata
- **run_id**: `2026-09-13_vultr_delhi_hp-4c8g-intel_run01`
- **machine_id**: `vultr-delhi-vhp-4c-8gb-intel-01`
- **protocol_version**: `CBP-1.0`
- **provider**: `Vultr`
- **region**: `Delhi`
- **plan_name**: `vhp-4c-8gb-intel`
- **created_utc**: `2026-09-13 11:32:43 UTC`
- **pricing**: `{'monthly_usd': 48.0, 'promotional_credit': True, 'currency': 'USD'}`
- **zone**: `default`
- **instance_family**: `vhp`
- **cpu_arch**: `x86_64`
- **cpu_model**: `Intel Xeon Processor (Cascadelake)`
- **exposed_vcpu**: `4`
- **ram_gb**: `7.75`
- **root_disk_type**: `NVMe/SSD`
- **root_disk_size_gb**: `180G`
- **virt_type**: `Microsoft`
- **kernel_version**: `6.8.0-138-generic`
- **os_distro**: `Ubuntu 24.04.4 LTS`

## 2. CPU Performance
| Test ID | Threads | Events/sec | Mean Latency (ms) | P95 Latency (ms) | Scaling / Burst Metric |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T010 | 1 | 472.04 | 2.12 | 2.18 | N/A |
| T011 | 4 | 1888.52 | 2.12 | 2.18 | 1.0002 |
| T012 | 4 | 1887.48 | 2.12 | 2.18 | Burst/Sust=1.0, CV=0.34% |

## 3. PostgreSQL OLTP Performance
| Test ID | Workload | Scale | Clients | Whole-run TPS | Sustained TPS | Latency (ms) | Failures |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T052 | mixed_tpc_b | 10 | 1 | 2326.355556 | 2360.4 | 0.42 | 0 |
| T052 | mixed_tpc_b | 10 | 4 | 6007.56094 | 5976.0 | 0.67 | 0 |
| T052 | mixed_tpc_b | 10 | 8 | 8190.970216 | 8279.7 | 0.97 | 0 |
| T052 | mixed_tpc_b | 10 | 16 | 7753.427222 | 7788.8 | 2.05 | 0 |
| T052 | mixed_tpc_b | 10 | 32 | 6900.151128 | 6933.0 | 4.62 | 0 |
| T053 | select_only | 10 | 1 | 20714.027131 | 20778.7 | 0.05 | 0 |
| T053 | select_only | 10 | 4 | 86652.683141 | 86816.8 | 0.04 | 0 |
| T053 | select_only | 10 | 8 | 69418.1938 | 69477.1 | 0.11 | 0 |
| T053 | select_only | 10 | 16 | 63172.519435 | 63268.7 | 0.25 | 0 |
| T053 | select_only | 10 | 32 | 64720.038781 | 64260.1 | 0.5 | 0 |