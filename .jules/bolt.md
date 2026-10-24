# Bolt's Journal - Critical Learnings

## 2025-05-18 - Parallelizing I/O-bound web scraping with ThreadPoolExecutor
**Learning:** Sequential web scraping with `time.sleep(1)` creates a significant delay (N * (latency + 1s)), which severely bottlenecks lead generation for multiple results. Utilizing `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes network I/O while preserving original search result ranking order.
**Action:** Use `ThreadPoolExecutor` and `executor.map` for I/O-bound scraping tasks where order matters.
