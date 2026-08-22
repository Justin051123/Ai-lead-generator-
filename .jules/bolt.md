## 2026-08-22 - Parallelizing Lead Scraping with ThreadPoolExecutor

**Learning:** In I/O-bound web scraping workloads like lead extraction, sequential HTTP GET requests with artificial delays create severe bottlenecks (~1s delay per lead). Replacing sequential iteration with `ThreadPoolExecutor(max_workers=...)` and using `executor.map` parallelizes network I/O while preserving the exact input order of search results.

**Action:** For batch network requests or external web scraping, use `concurrent.futures.ThreadPoolExecutor` with `executor.map` instead of sequential loops or `as_completed` when order matters.
