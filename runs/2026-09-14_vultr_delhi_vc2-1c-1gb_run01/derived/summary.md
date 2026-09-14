# CloudMark Benchmark Summary: 2026-09-14_vultr_delhi_vc2-1c-1gb_run01
Generated: 2026-09-14 10:22:51 UTC

## 1. System Metadata
- **run_id**: `2026-09-14_vultr_delhi_vc2-1c-1gb_run01`
- **machine_id**: `vultr-delhi-vc2-1c-1gb-01`
- **protocol_version**: `CBP-1.0`
- **provider**: `Vultr`
- **region**: `Delhi`
- **plan_name**: `vc2-1c-1gb`
- **created_utc**: `2026-09-14 09:41:08 UTC`
- **pricing**: `{'monthly_usd': 5.0, 'promotional_credit': False, 'currency': 'USD'}`
- **zone**: `default`
- **instance_family**: `vc2`
- **cpu_arch**: `x86_64`
- **cpu_model**: `Intel Xeon Processor (Cascadelake)`
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
| T010 | 1 | 440.77 | 2.27 | 2.52 | N/A |
| T011 | 1 | 435.65 | 2.29 | 2.61 | N/A |
| T012 | 1 | 440.95 | 2.27 | 2.52 | Burst/Sust=1.02, CV=2.1% |
| T010 | 1 | 440.77 | 2.27 | 2.52 | N/A |
| T011 | 1 | 435.65 | 2.29 | 2.61 | N/A |
| T012 | 1 | 440.95 | 2.27 | 2.52 | Burst/Sust=1.02, CV=2.1% |

## 3. PostgreSQL OLTP Performance
| Test ID | Workload | Scale | Clients | Whole-run TPS | Sustained TPS | Latency (ms) | Failures |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T052 | mixed_tpc_b | 10 | 1 | 2027.533841 | 2071.1 | 0.48 | 0 |
| T052 | mixed_tpc_b | 10 | 4 | 1992.519845 | 1957.5 | 2.06 | 0 |
| T052 | mixed_tpc_b | 10 | 8 | 1835.685893 | 1821.2 | 4.4 | 0 |
| T052 | mixed_tpc_b | 10 | 16 | 1559.527055 | 1539.0 | 10.43 | 0 |
| T052 | mixed_tpc_b | 10 | 32 | 1230.517715 | 1217.1 | 26.38 | 0 |
| T053 | select_only | 10 | 1 | 19436.032272 | 19475.2 | 0.05 | 0 |
| T053 | select_only | 10 | 4 | 15234.172333 | 15287.2 | 0.26 | 0 |
| T053 | select_only | 10 | 8 | 14288.49629 | 14442.4 | 0.55 | 0 |
| T053 | select_only | 10 | 16 | 13501.055511 | 13695.9 | 1.17 | 0 |
| T053 | select_only | 10 | 32 | 9336.898071 | 9308.0 | 3.44 | 0 |
| T052 | mixed_tpc_b | 10 | 1 | 2027.533841 | 2071.1 | 0.48 | 0 |
| T052 | mixed_tpc_b | 10 | 4 | 1992.519845 | 1957.5 | 2.06 | 0 |
| T052 | mixed_tpc_b | 10 | 8 | 1835.685893 | 1821.2 | 4.4 | 0 |
| T052 | mixed_tpc_b | 10 | 16 | 1559.527055 | 1539.0 | 10.43 | 0 |
| T052 | mixed_tpc_b | 10 | 32 | 1230.517715 | 1217.1 | 26.38 | 0 |
| T053 | select_only | 10 | 1 | 19436.032272 | 19475.2 | 0.05 | 0 |
| T053 | select_only | 10 | 4 | 15234.172333 | 15287.2 | 0.26 | 0 |
| T053 | select_only | 10 | 8 | 14288.49629 | 14442.4 | 0.55 | 0 |
| T053 | select_only | 10 | 16 | 13501.055511 | 13695.9 | 1.17 | 0 |
| T053 | select_only | 10 | 32 | 9336.898071 | 9308.0 | 3.44 | 0 |

## 4. Memory Throughput
| Test ID | Operation | Threads | Block Size | Throughput (MiB/s) | Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T020 | write | 1 | 1M | 19787.67 | 0.05 |
| T020 | read | 1 | 1M | 24095.46 | 0.04 |
| T020 | write | 1 | 1M | 19787.67 | 0.05 |
| T020 | read | 1 | 1M | 24095.46 | 0.04 |

## 5. Storage I/O Performance
| Test ID | I/O Pattern | Block Size | Read IOPS | Write IOPS | Read (MB/s) | Write (MB/s) | Mean Latency (ms) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T031 | Sequential Write (1MB, iodepth=16, direct=1) | 1M | 0.0 | 2677.0 | 0.0 | 2678.0 | 0.084 |
| T031 | Sequential Read (1MB, iodepth=16, direct=1) | 1M | 3177.0 | 0.0 | 3178.0 | 0.0 | 0.015 |
| T032 | Random Read (4K, iodepth=32, numjobs=4) | 4k | 144000.0 | 0.0 | 564.0 | 0.0 | 0.883 |
| T032 | Random Write (4K, iodepth=32, numjobs=4) | 4k | 0.0 | 102000.0 | 0.0 | 400.0 | 1.226 |
| T032 | Mixed Random 70/30 (4K, iodepth=32, numjobs=4) | 4k | 125000.0 | 53400.0 | 486.0 | 209.0 | 0.737 |
| T031 | Sequential Write (1MB, iodepth=16, direct=1) | 1M | 0.0 | 2677.0 | 0.0 | 2678.0 | 0.084 |
| T031 | Sequential Read (1MB, iodepth=16, direct=1) | 1M | 3177.0 | 0.0 | 3178.0 | 0.0 | 0.015 |
| T032 | Random Read (4K, iodepth=32, numjobs=4) | 4k | 144000.0 | 0.0 | 564.0 | 0.0 | 0.883 |
| T032 | Random Write (4K, iodepth=32, numjobs=4) | 4k | 0.0 | 102000.0 | 0.0 | 400.0 | 1.226 |
| T032 | Mixed Random 70/30 (4K, iodepth=32, numjobs=4) | 4k | 125000.0 | 53400.0 | 486.0 | 209.0 | 0.737 |