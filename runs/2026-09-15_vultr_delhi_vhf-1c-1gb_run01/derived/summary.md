# CloudMark Benchmark Summary: 2026-09-15_vultr_delhi_vhf-1c-1gb_run01
Generated: 2026-09-15 12:52:54 UTC

## 1. System Metadata
- **run_id**: `2026-09-15_vultr_delhi_vhf-1c-1gb_run01`
- **machine_id**: `vultr-delhi-vhf-1c-1gb-01`
- **protocol_version**: `CBP-1.0`
- **provider**: `Vultr`
- **region**: `Delhi`
- **plan_name**: `vhf-1c-1gb`
- **created_utc**: `2026-09-15 12:11:28 UTC`
- **pricing**: `{'monthly_usd': 6.0, 'promotional_credit': False, 'currency': 'USD'}`
- **zone**: `default`
- **instance_family**: `vhf`
- **cpu_arch**: `x86_64`
- **cpu_model**: `Intel Core Processor (Skylake, IBRS, no TSX)`
- **exposed_vcpu**: `1`
- **ram_gb**: `0.93`
- **root_disk_type**: `SSD`
- **root_disk_size_gb**: `32G`
- **virt_type**: `Microsoft`
- **kernel_version**: `6.1.0-52-amd64`
- **os_distro**: `Debian GNU/Linux 12 (bookworm)`

## 2. CPU Performance
| Test ID | Threads | Events/sec | Mean Latency (ms) | P95 Latency (ms) | Scaling / Burst Metric |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T010 | 1 | 1048.45 | 0.95 | 1.01 | N/A |
| T011 | 1 | 1046.1 | 0.96 | 1.03 | N/A |
| T012 | 1 | 1047.41 | 0.95 | 1.03 | Burst/Sust=0.99, CV=1.11% |

## 3. PostgreSQL OLTP Performance
| Test ID | Workload | Scale | Clients | Whole-run TPS | Sustained TPS | Latency (ms) | Failures |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T052 | mixed_tpc_b | 10 | 1 | 2145.058567 | 2143.7 | 0.47 | 0 |
| T052 | mixed_tpc_b | 10 | 4 | 2029.086978 | 2019.9 | 1.98 | 0 |
| T052 | mixed_tpc_b | 10 | 8 | 1914.864177 | 1915.3 | 4.18 | 0 |
| T052 | mixed_tpc_b | 10 | 16 | 1808.821414 | 1802.8 | 8.88 | 0 |
| T052 | mixed_tpc_b | 10 | 32 | 1719.219309 | 1717.4 | 18.64 | 0 |
| T053 | select_only | 10 | 1 | 16444.517518 | 16523.2 | 0.06 | 0 |
| T053 | select_only | 10 | 4 | 13483.7456 | 13492.9 | 0.3 | 0 |
| T053 | select_only | 10 | 8 | 13088.724189 | 13133.8 | 0.61 | 0 |
| T053 | select_only | 10 | 16 | 12686.793243 | 12701.6 | 1.26 | 0 |
| T053 | select_only | 10 | 32 | 12198.507941 | 12260.8 | 2.61 | 0 |

## 4. Memory Throughput
| Test ID | Operation | Threads | Block Size | Throughput (MiB/s) | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T020 | write | 1 | 1M | 21387.01 | 0.05 |
| T020 | read | 1 | 1M | 25027.96 | 0.04 |

## 5. Storage I/O Performance
| Test ID | I/O Pattern | Block Size | Read IOPS | Write IOPS | Read (MB/s) | Write (MB/s) | Mean Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T031 | Sequential Write (1MB, iodepth=16, direct=1) | 1M | 0.0 | 1566.0 | 0.0 | 1566.0 | 0.049 |
| T031 | Sequential Read (1MB, iodepth=16, direct=1) | 1M | 2620.0 | 0.0 | 2621.0 | 0.0 | 6.096 |
| T032 | Random Read (4K, iodepth=32, numjobs=4) | 4k | 157000.0 | 0.0 | 614.0 | 0.0 | 0.809 |
| T032 | Random Write (4K, iodepth=32, numjobs=4) | 4k | 0.0 | 81000.0 | 0.0 | 317.0 | 0.031 |
| T032 | Mixed Random 70/30 (4K, iodepth=32, numjobs=4) | 4k | 82100.0 | 35200.0 | 321.0 | 137.0 | 0.024 |