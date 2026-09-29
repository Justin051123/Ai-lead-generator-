## 2025-05-18 - Concurrent Scraping & Thread-Local Sessions
**Learning:** Sequential web scraping with explicit `time.sleep` calls was the primary bottleneck in lead generation. Replacing sequential loops with `ThreadPoolExecutor(max_workers=5)` using `executor.map` parallelizes I/O requests while maintaining search result ranking. Thread-local `requests.Session` instances enable HTTP connection pooling without thread contention.
**Action:** Always prefer `executor.map` over `as_completed` when scraping or processing items where search relevance / output order matters.
