## 2025-05-18 - Parallelizing Web Scraping with Order Preservation

**Learning:** Web scraping in lead generation is I/O-bound with high latency per site. Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes network HTTP requests and regex parsing across worker threads while automatically maintaining the original search result ordering. Removing artificial `time.sleep(1)` sequential delays when transitioning to parallel execution yields drastic speed gains.

**Action:** When scraping multiple URLs where search result relevance depends on rank order, use `ThreadPoolExecutor` with `executor.map` instead of sequential loops or unordered futures (`as_completed`). Pre-compile regexes at module level for additional performance wins in loop extractions.
