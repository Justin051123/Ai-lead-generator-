## 2026-06-23 - Parallel Web Scraping & Order Preservation
**Learning:** Sequential HTTP requests in `lead_gen.py` with `time.sleep(1)` introduced an O(N) latency bottleneck (e.g. 10 leads took >10 seconds). Utilizing `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes I/O-bound requests while preserving search result ranking.
**Action:** Use `ThreadPoolExecutor` and `executor.map` for I/O-bound web scraping tasks where input list order must be preserved.
