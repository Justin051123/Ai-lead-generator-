## Bolt's Journal - Critical Learnings

## 2026-06-23 - Concurrent Lead Scraping & Order Preservation
**Learning:** Sequential scraping with `time.sleep(1)` introduced massive I/O delays (~11s for 10 leads with 100ms response times). Parallelizing HTTP scraping using `concurrent.futures.ThreadPoolExecutor` with `executor.map` and thread-local HTTP session connection pooling reduced processing time down to ~0.11s (~100x speedup), while preserving search result rank order.
**Action:** When scraping multiple web endpoints, always use `ThreadPoolExecutor.map` with thread-local `requests.Session` and pre-compiled regex patterns to maximize concurrent I/O throughput without altering result ordering.
