# CloudMark Benchmark Summary: 2026-09-14_vultr_delhi_vc2-1c-2gb_run01
Generated: 2026-09-14 13:30:27 UTC

## 1. System Metadata
- **run_id**: `2026-09-14_vultr_delhi_vc2-1c-2gb_run01`
- **machine_id**: `vultr-delhi-vc2-1c-2gb-01`
- **protocol_version**: `CBP-1.0`
- **provider**: `Vultr`
- **region**: `Delhi`
- **plan_name**: `vc2-1c-2gb`
- **created_utc**: `2026-09-14 12:48:38 UTC`
- **pricing**: `{'monthly_usd': 10.0, 'promotional_credit': False, 'currency': 'USD'}`
- **zone**: `default`
- **instance_family**: `vc2`
- **cpu_arch**: `x86_64`
- **cpu_model**: `Intel Xeon Processor (Cascadelake)`
- **exposed_vcpu**: `1`
- **ram_gb**: `1.92`
- **root_disk_type**: `SSD`
- **root_disk_size_gb**: `55G`
- **virt_type**: `Microsoft`
- **kernel_version**: `6.1.0-52-amd64`
- **os_distro**: `Debian GNU/Linux 12 (bookworm)`

## 2. CPU Performance
| Test ID | Threads | Events/sec | Mean Latency (ms) | P95 Latency (ms) | Scaling / Burst Metric |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T010 | 1 | 218.47 | 4.57 | 6.67 | N/A |
| T011 | 1 | 350.17 | 2.85 | 6.32 | N/A |
| T012 | 1 | 449.88 | 2.22 | 2.35 | Burst/Sust=1.0, CV=0.96% |
| T010 | 1 | 218.47 | 4.57 | 6.67 | N/A |
| T011 | 1 | 350.17 | 2.85 | 6.32 | N/A |
| T012 | 1 | 449.88 | 2.22 | 2.35 | Burst/Sust=1.0, CV=0.96% |

## 3. PostgreSQL OLTP Performance
| Test ID | Workload | Scale | Clients | Whole-run TPS | Sustained TPS | Latency (ms) | Failures |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T052 | mixed_tpc_b | 10 | 1 | 2178.437636 | 2180.4 | 0.46 | 0 |
| T052 | mixed_tpc_b | 10 | 4 | 2232.922483 | 2185.1 | 1.84 | 0 |
| T052 | mixed_tpc_b | 10 | 8 | 2137.246004 | 2127.9 | 3.76 | 0 |
| T052 | mixed_tpc_b | 10 | 16 | 1843.084653 | 1813.0 | 8.83 | 0 |
| T052 | mixed_tpc_b | 10 | 32 | 1456.567986 | 1461.7 | 21.92 | 0 |
| T053 | select_only | 10 | 1 | 20730.064064 | 21048.0 | 0.05 | 0 |
| T053 | select_only | 10 | 4 | 16873.279715 | 16933.3 | 0.24 | 0 |
| T053 | select_only | 10 | 8 | 15726.790349 | 15547.8 | 0.51 | 0 |
| T053 | select_only | 10 | 16 | 15041.00829 | 15067.2 | 1.06 | 0 |
| T053 | select_only | 10 | 32 | 11747.874054 | 11508.8 | 2.85 | 0 |
| T052 | mixed_tpc_b | 10 | 1 | 2178.437636 | 2180.4 | 0.46 | 0 |
| T052 | mixed_tpc_b | 10 | 4 | 2232.922483 | 2185.1 | 1.84 | 0 |
| T052 | mixed_tpc_b | 10 | 8 | 2137.246004 | 2127.9 | 3.76 | 0 |
| T052 | mixed_tpc_b | 10 | 16 | 1843.084653 | 1813.0 | 8.83 | 0 |
| T052 | mixed_tpc_b | 10 | 32 | 1456.567986 | 1461.7 | 21.92 | 0 |
| T053 | select_only | 10 | 1 | 20730.064064 | 21048.0 | 0.05 | 0 |
| T053 | select_only | 10 | 4 | 16873.279715 | 16933.3 | 0.24 | 0 |
| T053 | select_only | 10 | 8 | 15726.790349 | 15547.8 | 0.51 | 0 |
| T053 | select_only | 10 | 16 | 15041.00829 | 15067.2 | 1.06 | 0 |
| T053 | select_only | 10 | 32 | 11747.874054 | 11508.8 | 2.85 | 0 |

## 4. Memory Throughput
| Test ID | Operation | Threads | Block Size | Throughput (MiB/s) | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T020 | write | 1 | 1M | 19667.79 | 0.05 |
| T020 | read | 1 | 1M | 24029.8 | 0.04 |
| T020 | write | 1 | 1M | 19667.79 | 0.05 |
| T020 | read | 1 | 1M | 24029.8 | 0.04 |

## 5. Storage I/O Performance
| Test ID | I/O Pattern | Block Size | Read IOPS | Write IOPS | Read (MB/s) | Write (MB/s) | Mean Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T031 | Sequential Write (1MB, iodepth=16, direct=1) | 1M | 0.0 | 2697.0 | 0.0 | 2698.0 | 0.082 |
| T031 | Sequential Read (1MB, iodepth=16, direct=1) | 1M | 3253.0 | 0.0 | 3254.0 | 0.0 | 0.014 |
| T032 | Random Read (4K, iodepth=32, numjobs=4) | 4k | 210000.0 | 0.0 | 819.0 | 0.0 | 0.607 |
| T032 | Random Write (4K, iodepth=32, numjobs=4) | 4k | 0.0 | 193000.0 | 0.0 | 752.0 | 0.663 |
| T032 | Mixed Random 70/30 (4K, iodepth=32, numjobs=4) | 4k | 144000.0 | 61600.0 | 561.0 | 241.0 | 0.641 |
| T031 | Sequential Write (1MB, iodepth=16, direct=1) | 1M | 0.0 | 2697.0 | 0.0 | 2698.0 | 0.082 |
| T031 | Sequential Read (1MB, iodepth=16, direct=1) | 1M | 3253.0 | 0.0 | 3254.0 | 0.0 | 0.014 |
| T032 | Random Read (4K, iodepth=32, numjobs=4) | 4k | 210000.0 | 0.0 | 819.0 | 0.0 | 0.607 |
| T032 | Random Write (4K, iodepth=32, numjobs=4) | 4k | 0.0 | 193000.0 | 0.0 | 752.0 | 0.663 |
| T032 | Mixed Random 70/30 (4K, iodepth=32, numjobs=4) | 4k | 144000.0 | 61600.0 | 561.0 | 241.0 | 0.641 |