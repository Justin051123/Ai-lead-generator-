## 2025-05-18 - Parallelizing Web Scraping with `executor.map`

**Learning:** In sequential lead generation pipelines with network request latency (`requests.get`), `executor.map` from `concurrent.futures.ThreadPoolExecutor` provides substantial speed improvements (e.g. 5x faster for 5 items with 1s latency) while naturally preserving search result ordering without needing manually indexed async queues.
**Action:** Use `ThreadPoolExecutor(max_workers=...)` with `executor.map` for I/O-bound web scraping pipelines where input sequence order must match search relevance order.
