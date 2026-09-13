# Bolt's Journal - Critical Learnings

## 2025-05-18 - Parallelizing I/O-bound web scraping with ThreadPoolExecutor
**Learning:** Sequential HTTP fetches with `time.sleep` introduce severe latency (e.g. 10 leads taking 10+ seconds just in sleep delays). Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes I/O requests while preserving search result ordering.
**Action:** Always prefer `ThreadPoolExecutor` and `executor.map` for I/O-bound scraping tasks where order matters.
