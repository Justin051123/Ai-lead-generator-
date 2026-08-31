## 2026-06-23 - Parallelizing I/O Scraping with Search Result Order Preservation

**Learning:** Sequential scraping of business search result URLs with artificial delay introduced a major bottleneck (~20s for 10 leads). Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes I/O-bound web requests while preserving original search result ordering.

**Action:** For I/O-bound website processing pipelines where input ranking/order matters, use `executor.map` over `as_completed` to maintain search relevance ordering while achieving concurrent throughput gains.
