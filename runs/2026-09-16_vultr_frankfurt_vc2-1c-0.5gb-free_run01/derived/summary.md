# CloudMark Benchmark Summary: 2026-09-16_vultr_frankfurt_vc2-1c-0.5gb-free_run01
Generated: 2026-09-16 09:08:49 UTC

## 1. System Metadata
- **run_id**: `2026-09-16_vultr_frankfurt_vc2-1c-0.5gb-free_run01`
- **machine_id**: `vultr-frankfurt-vc2-1c-05gb-free-01`
- **protocol_version**: `CBP-1.0`
- **provider**: `Vultr`
- **region**: `Frankfurt`
- **plan_name**: `vc2-1c-0.5gb-free`
- **created_utc**: `2026-09-16 08:25:53 UTC`
- **pricing**: `{'monthly_usd': 0.0, 'promotional_credit': False, 'currency': 'USD'}`
- **zone**: `default`
- **instance_family**: `vc2`
- **cpu_arch**: `x86_64`
- **cpu_model**: `Intel Xeon Processor (Skylake, IBRS)`
- **exposed_vcpu**: `1`
- **ram_gb**: `0.44`
- **root_disk_type**: `SSD`
- **root_disk_size_gb**: `10G`
- **virt_type**: `Microsoft`
- **kernel_version**: `6.1.0-52-amd64`
- **os_distro**: `Debian GNU/Linux 12 (bookworm)`

## 2. CPU Performance
| Test ID | Threads | Events/sec | Mean Latency (ms) | P95 Latency (ms) | Scaling / Burst Metric |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T010 | 1 | 366.22 | 2.73 | 3.25 | N/A |
| T011 | 1 | 380.93 | 2.62 | 3.07 | N/A |
| T012 | 1 | 379.08 | 2.64 | 3.07 | Burst/Sust=1.0, CV=2.87% |

## 3. PostgreSQL OLTP Performance
| Test ID | Workload | Scale | Clients | Whole-run TPS | Sustained TPS | Latency (ms) | Failures |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T052 | mixed_tpc_b | 10 | 1 | 0.0 | N/A | 0.0 | 0 |
| T053 | select_only | 10 | 1 | 0.0 | N/A | 0.0 | 0 |
| T052 | mixed_tpc_b | 10 | 4 | 445.638835 | 437.7 | 12.87 | 0 |
| T052 | mixed_tpc_b | 10 | 8 | 538.831192 | 486.0 | 17.94 | 0 |
| T052 | mixed_tpc_b | 10 | 16 | 536.880869 | 588.2 | 29.76 | 0 |
| T052 | mixed_tpc_b | 10 | 32 | 455.809892 | 442.8 | 77.55 | 0 |
| T053 | select_only | 10 | 4 | 8078.302329 | 8160.3 | 0.49 | 0 |
| T053 | select_only | 10 | 8 | 7370.479192 | 7696.3 | 1.04 | 0 |
| T053 | select_only | 10 | 16 | 5601.220414 | 5643.5 | 2.84 | 0 |
| T053 | select_only | 10 | 32 | 5041.778241 | 5218.8 | 6.13 | 0 |

## 4. Memory Throughput
| Test ID | Operation | Threads | Block Size | Throughput (MiB/s) | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T020 | write | 1 | 1M | 15988.95 | 0.06 |
| T020 | read | 1 | 1M | 20361.07 | 0.05 |

## 5. Storage I/O Performance
| Test ID | I/O Pattern | Block Size | Read IOPS | Write IOPS | Read (MB/s) | Write (MB/s) | Mean Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T031 | Sequential Write (1MB, iodepth=16, direct=1) | 1M | 0.0 | 204.0 | 0.0 | 204.0 | 0.58 |
| T032 | Random Read (4K, iodepth=32, numjobs=4) | 4k | 206000.0 | 0.0 | 805.0 | 0.0 | 0.456 |