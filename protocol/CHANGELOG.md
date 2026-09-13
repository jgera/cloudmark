# CloudMark Benchmark Protocol Changelog

All notable changes to the CloudMark Benchmark Protocol (CBP) family will be documented in this file.

## [CBP-1.0] - 2026-09-13
### Added
- Standardized multi-provider test sequence: T001 through T056.
- Distinct separation of Raw data and Derived metrics.
- Principle of distinguishing burst vs sustained performance across CPU, Storage, and Database workloads.
- Explicit prohibition against performance tuning prior to establishing default out-of-the-box baselines.
- Standardized directory layout (`master/`, `runs/`, `scripts/`, `protocol/`).
- Standardized metadata schema for runs, machines, and pricing.
- Automated orchestration and parsing workflow guidelines.

## [CBP-0] - Exploratory Baseline
### Historical
- Initial exploratory testing on Google Cloud Platform `e2-micro` (PostgreSQL 18, scale 10).
- Identified substantial burst vs sustained performance gap (e.g. ~475 peak to ~90 sustained TPS at 1 client).
- Preserved as `LEGACY-GCP-001` for historical reference and order-of-magnitude comparisons; not for formal CBP-1.0 statistical comparisons.
