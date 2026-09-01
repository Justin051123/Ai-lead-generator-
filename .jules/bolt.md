# Bolt's Journal - Critical Learnings

## 2025-09-01 - Parallelizing lead scraping with ThreadPoolExecutor
**Learning:** Sequential scraping of lead websites with hardcoded delays causes a linear scale in latency (10s+ for 10 leads). Since web scraping is heavily I/O-bound, using `ThreadPoolExecutor` with `executor.map` preserves original search order while processing requests concurrently.
**Action:** Use `ThreadPoolExecutor` with `executor.map` for batch URL processing to optimize I/O-bound tasks without changing output order.
