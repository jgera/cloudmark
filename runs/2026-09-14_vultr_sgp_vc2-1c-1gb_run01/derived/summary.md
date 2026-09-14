# CloudMark Benchmark Summary: 2026-09-14_vultr_sgp_vc2-1c-1gb_run01
Generated: 2026-09-14 17:25:49 UTC

## 1. System Metadata
- **run_id**: `2026-09-14_vultr_sgp_vc2-1c-1gb_run01`
- **machine_id**: `vultr-sgp-vc2-1c-1gb-01`
- **protocol_version**: `CBP-1.0`
- **provider**: `Vultr`
- **region**: `Sgp`
- **plan_name**: `vc2-1c-1gb`
- **created_utc**: `2026-09-14 16:42:52 UTC`
- **pricing**: `{'monthly_usd': 5.0, 'promotional_credit': False, 'currency': 'USD'}`
- **zone**: `default`
- **instance_family**: `vc2`
- **cpu_arch**: `x86_64`
- **cpu_model**: `Intel Core Processor (Broadwell, no TSX, IBRS)`
- **exposed_vcpu**: `1`
- **ram_gb**: `0.93`
- **root_disk_type**: `SSD`
- **root_disk_size_gb**: `25G`
- **virt_type**: `Microsoft`
- **kernel_version**: `6.1.0-52-amd64`
- **os_distro**: `Debian GNU/Linux 12 (bookworm)`

## 2. CPU Performance
| Test ID | Threads | Events/sec | Mean Latency (ms) | P95 Latency (ms) | Scaling / Burst Metric |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T010 | 1 | 303.49 | 3.29 | 3.55 | N/A |
| T011 | 1 | 304.47 | 3.28 | 3.55 | N/A |
| T012 | 1 | 302.88 | 3.3 | 3.68 | Burst/Sust=1.02, CV=1.58% |
| T010 | 1 | 303.49 | 3.29 | 3.55 | N/A |
| T011 | 1 | 304.47 | 3.28 | 3.55 | N/A |
| T012 | 1 | 302.88 | 3.3 | 3.68 | Burst/Sust=1.02, CV=1.58% |

## 3. PostgreSQL OLTP Performance
| Test ID | Workload | Scale | Clients | Whole-run TPS | Sustained TPS | Latency (ms) | Failures |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T052 | mixed_tpc_b | 10 | 1 | 775.896736 | 825.3 | 1.21 | 0 |
| T052 | mixed_tpc_b | 10 | 4 | 1159.123983 | 1164.5 | 3.44 | 0 |
| T052 | mixed_tpc_b | 10 | 8 | 1174.408736 | 1164.4 | 6.88 | 0 |
| T052 | mixed_tpc_b | 10 | 16 | 1001.767251 | 982.9 | 16.32 | 0 |
| T052 | mixed_tpc_b | 10 | 32 | 876.93821 | 897.3 | 35.69 | 0 |
| T053 | select_only | 10 | 1 | 8957.197855 | 9224.7 | 0.11 | 0 |
| T053 | select_only | 10 | 4 | 8165.373964 | 8076.3 | 0.5 | 0 |
| T053 | select_only | 10 | 8 | 8005.923383 | 8120.8 | 0.98 | 0 |
| T053 | select_only | 10 | 16 | 7534.51183 | 7418.1 | 2.16 | 0 |
| T053 | select_only | 10 | 32 | 6365.540336 | 6317.1 | 5.08 | 0 |
| T052 | mixed_tpc_b | 10 | 1 | 775.896736 | 825.3 | 1.21 | 0 |
| T052 | mixed_tpc_b | 10 | 4 | 1159.123983 | 1164.5 | 3.44 | 0 |
| T052 | mixed_tpc_b | 10 | 8 | 1174.408736 | 1164.4 | 6.88 | 0 |
| T052 | mixed_tpc_b | 10 | 16 | 1001.767251 | 982.9 | 16.32 | 0 |
| T052 | mixed_tpc_b | 10 | 32 | 876.93821 | 897.3 | 35.69 | 0 |
| T053 | select_only | 10 | 1 | 8957.197855 | 9224.7 | 0.11 | 0 |
| T053 | select_only | 10 | 4 | 8165.373964 | 8076.3 | 0.5 | 0 |
| T053 | select_only | 10 | 8 | 8005.923383 | 8120.8 | 0.98 | 0 |
| T053 | select_only | 10 | 16 | 7534.51183 | 7418.1 | 2.16 | 0 |
| T053 | select_only | 10 | 32 | 6365.540336 | 6317.1 | 5.08 | 0 |

## 4. Memory Throughput
| Test ID | Operation | Threads | Block Size | Throughput (MiB/s) | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T020 | write | 1 | 1M | 11893.03 | 0.08 |
| T020 | read | 1 | 1M | 17497.42 | 0.06 |
| T020 | write | 1 | 1M | 11893.03 | 0.08 |
| T020 | read | 1 | 1M | 17497.42 | 0.06 |

## 5. Storage I/O Performance
| Test ID | I/O Pattern | Block Size | Read IOPS | Write IOPS | Read (MB/s) | Write (MB/s) | Mean Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T031 | Sequential Write (1MB, iodepth=16, direct=1) | 1M | 0.0 | 308.0 | 0.0 | 308.0 | 0.118 |
| T031 | Sequential Read (1MB, iodepth=16, direct=1) | 1M | 352.0 | 0.0 | 352.0 | 0.0 | 0.032 |
| T032 | Random Read (4K, iodepth=32, numjobs=4) | 4k | 56000.0 | 0.0 | 219.0 | 0.0 | 2.275 |
| T032 | Random Write (4K, iodepth=32, numjobs=4) | 4k | 0.0 | 37000.0 | 0.0 | 145.0 | 3.444 |
| T032 | Mixed Random 70/30 (4K, iodepth=32, numjobs=4) | 4k | 33400.0 | 14400.0 | 131.0 | 56.1 | 2.8 |
| T031 | Sequential Write (1MB, iodepth=16, direct=1) | 1M | 0.0 | 308.0 | 0.0 | 308.0 | 0.118 |
| T031 | Sequential Read (1MB, iodepth=16, direct=1) | 1M | 352.0 | 0.0 | 352.0 | 0.0 | 0.032 |
| T032 | Random Read (4K, iodepth=32, numjobs=4) | 4k | 56000.0 | 0.0 | 219.0 | 0.0 | 2.275 |
| T032 | Random Write (4K, iodepth=32, numjobs=4) | 4k | 0.0 | 37000.0 | 0.0 | 145.0 | 3.444 |
| T032 | Mixed Random 70/30 (4K, iodepth=32, numjobs=4) | 4k | 33400.0 | 14400.0 | 131.0 | 56.1 | 2.8 |