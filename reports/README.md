# CloudMark Benchmark Reports Directory

This directory contains publication-grade benchmark reports generated from the frozen CloudMark Benchmark Protocol (CBP-1.0).

## Available Reports

1. **[CBP-1.0 Comprehensive Benchmark Report](CBP-1.0_COMPREHENSIVE_BENCHMARK_REPORT.md)**
   - The complete consolidated paper covering all 11 evaluated machines, overall price-to-performance rankings (TPS/$), India Domestic Triangle analysis, and architectural decision trees.
2. **[Cohort A: Standard 4-Core Tier Report](COHORT_A_STANDARD_4CORE.md)**
   - Detailed analysis of 4-vCPU machines comparing GCP C2, GCP Tau ARM64, GCP E2, and Vultr Intel/AMD NVMe.
3. **[Cohort B: Micro & Entry Tier Report](COHORT_B_MICRO_AND_ENTRY.md)**
   - Detailed analysis of $0 to $10 virtual machines comparing GCP Always-Free, GCP Delhi, Vultr Delhi ($5 & $10), Vultr Mumbai ($5), and Vultr Singapore ($5).

## Raw Run Summaries

Individual machine summaries with verbatim tool output logs can be accessed under `../runs/<run_id>/derived/summary.md`:
- **`2026-09-13_vultr_delhi_hp-4c8g-intel_run01`**: [vultr-delhi-vhp-4c-8gb-intel-01](../runs/2026-09-13_vultr_delhi_hp-4c8g-intel_run01/derived/summary.md) (Complete; instance destroyed)
- **`2026-09-13_vultr_mumbai_hp-4c8g-amd_run01`**: [vultr-mumbai-vhp-4c-8gb-amd-01](../runs/2026-09-13_vultr_mumbai_hp-4c8g-amd_run01/derived/summary.md) (Complete; instance destroyed)
- **`2026-09-14_gcp_uswest1_e2-micro_run01`**: [google cloud platform-us-west1-e2-micro-01](../runs/2026-09-14_gcp_uswest1_e2-micro_run01/derived/summary.md) (Complete; persistent baseline preserved)
- **`2026-09-14_gcp_us-west1_e2-standard-4_run01`**: [google cloud platform-us-west1-e2-standard-4-01](../runs/2026-09-14_gcp_us-west1_e2-standard-4_run01/derived/summary.md) (Complete; instance destroyed)
- **`2026-09-14_gcp_us-central1_c2-standard-4_run01`**: [google cloud platform-us-central1-c2-standard-4-01](../runs/2026-09-14_gcp_us-central1_c2-standard-4_run01/derived/summary.md) (Complete; instance destroyed)
- **`2026-09-14_gcp_us-central1_t2a-standard-4_run01`**: [google cloud platform-us-central1-t2a-standard-4-01](../runs/2026-09-14_gcp_us-central1_t2a-standard-4_run01/derived/summary.md) (Complete; instance destroyed)
- **`2026-09-14_gcp_asia-south2_e2-micro_run01`**: [google cloud platform-asia-south2-e2-micro-01](../runs/2026-09-14_gcp_asia-south2_e2-micro_run01/derived/summary.md) (Complete; instance destroyed)
- **`2026-09-14_vultr_delhi_vc2-1c-1gb_run01`**: [vultr-delhi-vc2-1c-1gb-01](../runs/2026-09-14_vultr_delhi_vc2-1c-1gb_run01/derived/summary.md) (Complete; instance destroyed)
- **`2026-09-14_vultr_delhi_vc2-1c-2gb_run01`**: [vultr-delhi-vc2-1c-2gb-01](../runs/2026-09-14_vultr_delhi_vc2-1c-2gb_run01/derived/summary.md) (Complete; instance destroyed)
- **`2026-09-14_vultr_sgp_vc2-1c-1gb_run01`**: [vultr-sgp-vc2-1c-1gb-01](../runs/2026-09-14_vultr_sgp_vc2-1c-1gb_run01/derived/summary.md) (Complete; instance destroyed)
- **`2026-09-14_vultr_mumbai_vc2-1c-1gb_run01`**: [vultr-mumbai-vc2-1c-1gb-01](../runs/2026-09-14_vultr_mumbai_vc2-1c-1gb_run01/derived/summary.md) (Complete; instance destroyed)