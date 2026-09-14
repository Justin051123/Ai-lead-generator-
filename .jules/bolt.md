## 2026-06-23 - Parallel Lead Processing with ThreadPoolExecutor
**Learning:** Sequential scraping of business websites with `requests.get` and artificial delays (`time.sleep(1)`) creates a major I/O bottleneck. Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes network requests while preserving search rank order.
**Action:** Always prefer `executor.map` over `as_completed` when processing I/O-bound tasks in Python where ordering (like search relevance) matters.
