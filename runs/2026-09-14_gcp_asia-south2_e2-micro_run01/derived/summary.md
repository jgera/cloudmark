# CloudMark Benchmark Summary: 2026-09-14_gcp_asia-south2_e2-micro_run01
Generated: 2026-09-14 09:40:08 UTC

## 1. System Metadata
- **run_id**: `2026-09-14_gcp_asia-south2_e2-micro_run01`
- **machine_id**: `google cloud platform-asia-south2-e2-micro-01`
- **protocol_version**: `CBP-1.0`
- **provider**: `Google Cloud Platform`
- **region**: `asia-south2`
- **plan_name**: `e2-micro`
- **created_utc**: `2026-09-14 08:33:07 UTC`
- **pricing**: `{'monthly_usd': 7.3, 'promotional_credit': False, 'currency': 'USD'}`
- **zone**: `default`
- **instance_family**: `e2`
- **cpu_arch**: `x86_64`
- **cpu_model**: `AMD EPYC 7B12`
- **exposed_vcpu**: `2`
- **ram_gb**: `0.95`
- **root_disk_type**: `pd-standard`
- **root_disk_size_gb**: `30G`
- **virt_type**: `KVM`
- **kernel_version**: `6.1.0-53-cloud-amd64`
- **os_distro**: `Debian GNU/Linux 12 (bookworm)`

## 2. CPU Performance
| Test ID | Threads | Events/sec | Mean Latency (ms) | P95 Latency (ms) | Scaling / Burst Metric |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T010 | 1 | 790.2 | 1.26 | 0.75 | N/A |
| T011 | 2 | 269.75 | 7.41 | 1.37 | 0.1707 |
| T012 | 2 | 206.78 | 9.66 | 1.47 | Burst/Sust=1.79, CV=51.54% |
| T010 | 1 | 790.2 | 1.26 | 0.75 | N/A |
| T011 | 2 | 269.75 | 7.41 | 1.37 | 0.1707 |
| T012 | 2 | 206.78 | 9.66 | 1.47 | Burst/Sust=1.79, CV=51.54% |

## 3. PostgreSQL OLTP Performance
| Test ID | Workload | Scale | Clients | Whole-run TPS | Sustained TPS | Latency (ms) | Failures |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T052 | mixed_tpc_b | 10 | 1 | 215.806308 | 94.1 | 10.63 | 0 |
| T052 | mixed_tpc_b | 10 | 4 | 202.129158 | 194.3 | 20.59 | 0 |
| T052 | mixed_tpc_b | 10 | 8 | 239.533276 | 236.2 | 33.95 | 0 |
| T052 | mixed_tpc_b | 10 | 16 | 254.911958 | 250.5 | 63.99 | 0 |
| T053 | select_only | 10 | 1 | 2778.181845 | 971.8 | 1.01 | 0 |
| T053 | select_only | 10 | 4 | 2498.59395 | 2325.4 | 1.68 | 0 |
| T053 | select_only | 10 | 8 | 2393.163289 | 2248.5 | 3.52 | 0 |
| T053 | select_only | 10 | 16 | 2274.05976 | 2290.7 | 6.95 | 0 |
| T053 | select_only | 10 | 32 | 2178.377332 | 2120.5 | 15.17 | 0 |

## 4. Memory Throughput
| Test ID | Operation | Threads | Block Size | Throughput (MiB/s) | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T020 | write | 2 | 1M | 27495.06 | 0.07 |
| T020 | read | 2 | 1M | 14481.34 | 0.14 |
| T020 | write | 2 | 1M | 27495.06 | 0.07 |
| T020 | read | 2 | 1M | 14481.34 | 0.14 |

## 5. Storage I/O Performance
| Test ID | I/O Pattern | Block Size | Read IOPS | Write IOPS | Read (MB/s) | Write (MB/s) | Mean Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T031 | Sequential Write (1MB, iodepth=16, direct=1) | 1M | 0.0 | 101.0 | 0.0 | 102.0 | 0.403 |
| T031 | Sequential Read (1MB, iodepth=16, direct=1) | 1M | 120.0 | 0.0 | 120.0 | 0.0 | 0.079 |
| T032 | Random Read (4K, iodepth=32, numjobs=4) | 4k | 152.0 | 0.0 | 0.6 | 0.0 | 0.048 |
| T032 | Random Write (4K, iodepth=32, numjobs=4) | 4k | 0.0 | 302.0 | 0.0 | 1.18 | 1.146 |
| T032 | Mixed Random 70/30 (4K, iodepth=32, numjobs=4) | 4k | 124.0 | 55.0 | 0.49 | 0.22 | 4.862 |
| T031 | Sequential Write (1MB, iodepth=16, direct=1) | 1M | 0.0 | 101.0 | 0.0 | 102.0 | 0.403 |
| T031 | Sequential Read (1MB, iodepth=16, direct=1) | 1M | 120.0 | 0.0 | 120.0 | 0.0 | 0.079 |
| T032 | Random Read (4K, iodepth=32, numjobs=4) | 4k | 152.0 | 0.0 | 0.6 | 0.0 | 0.048 |
| T032 | Random Write (4K, iodepth=32, numjobs=4) | 4k | 0.0 | 302.0 | 0.0 | 1.18 | 1.146 |
| T032 | Mixed Random 70/30 (4K, iodepth=32, numjobs=4) | 4k | 124.0 | 55.0 | 0.49 | 0.22 | 4.862 |