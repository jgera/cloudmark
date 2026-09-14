# CloudMark Benchmark Summary: 2026-09-13_vultr_mumbai_hp-4c8g-amd_run01
Generated: 2026-09-14 04:50:20 UTC

## 1. System Metadata
- **run_id**: `2026-09-13_vultr_mumbai_hp-4c8g-amd_run01`
- **machine_id**: `vultr-mumbai-vhp-4c-8gb-amd-01`
- **protocol_version**: `CBP-1.0`
- **provider**: `Vultr`
- **region**: `Mumbai`
- **plan_name**: `vhp-4c-8gb-amd`
- **created_utc**: `2026-09-13 18:39:55 UTC`
- **pricing**: `{'monthly_usd': 48.0, 'promotional_credit': True, 'currency': 'USD'}`
- **zone**: `default`
- **instance_family**: `vhp`
- **cpu_arch**: `x86_64`
- **cpu_model**: `AMD EPYC-Rome Processor`
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
| T010 | 1 | 1348.07 | 0.74 | 0.77 | N/A |
| T011 | 4 | 5412.28 | 0.74 | 0.75 | 1.0037 |
| T012 | 4 | 5393.78 | 0.74 | 0.77 | Burst/Sust=1.01, CV=0.64% |

## 3. PostgreSQL OLTP Performance
| Test ID | Workload | Scale | Clients | Whole-run TPS | Sustained TPS | Latency (ms) | Failures |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T052 | mixed_tpc_b | 10 | 1 | 1196.525341 | 1213.3 | 0.83 | 0 |
| T052 | mixed_tpc_b | 10 | 4 | 3168.164154 | 3136.1 | 1.28 | 0 |
| T052 | mixed_tpc_b | 10 | 8 | 4545.93015 | 4561.9 | 1.75 | 0 |
| T052 | mixed_tpc_b | 10 | 16 | 4224.331174 | 4199.1 | 3.81 | 0 |
| T052 | mixed_tpc_b | 10 | 32 | 3600.750637 | 3636.8 | 8.82 | 0 |
| T053 | select_only | 10 | 1 | 10440.391224 | 10223.5 | 0.1 | 0 |
| T053 | select_only | 10 | 4 | 40749.727497 | 40771.8 | 0.09 | 0 |
| T053 | select_only | 10 | 8 | 36393.800302 | 36401.1 | 0.22 | 0 |
| T053 | select_only | 10 | 16 | 39053.896859 | 39028.9 | 0.41 | 0 |
| T053 | select_only | 10 | 32 | 38808.839309 | 38912.3 | 0.82 | 0 |

## 4. Memory Throughput
| Test ID | Operation | Threads | Block Size | Throughput (MiB/s) | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T020 | write | 4 | 1M | 18633.78 | 0.2 |
| T020 | read | 4 | 1M | 156755.7 | 0.02 |

## 5. Storage I/O Performance
| Test ID | I/O Pattern | Block Size | Read IOPS | Write IOPS | Read (MB/s) | Write (MB/s) | Mean Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T031 | Sequential Write (1MB, iodepth=16, direct=1) | 1M | 0.0 | 2878.0 | 0.0 | 2878.0 | 0.086 |
| T031 | Sequential Read (1MB, iodepth=16, direct=1) | 1M | 6460.0 | 0.0 | 6460.0 | 0.0 | 0.065 |
| T032 | Random Read (4K, iodepth=32, numjobs=4) | 4k | 127000.0 | 0.0 | 497.0 | 0.0 | 1.0 |
| T032 | Random Write (4K, iodepth=32, numjobs=4) | 4k | 0.0 | 124000.0 | 0.0 | 484.0 | 1.025 |
| T032 | Mixed Random 70/30 (4K, iodepth=32, numjobs=4) | 4k | 88000.0 | 37700.0 | 344.0 | 147.0 | 1.024 |