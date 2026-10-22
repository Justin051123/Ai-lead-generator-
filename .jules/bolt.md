## 2026-06-23 - Parallelize I/O Scraping with ThreadPoolExecutor

**Learning:** Web scraping sequential loops with `time.sleep` introduce severe I/O bottlenecks. Using `ThreadPoolExecutor.map` parallelizes HTTP requests while preserving search result ordering.
**Action:** Always use `ThreadPoolExecutor.map` for I/O-bound page scraping tasks where original search result ordering needs to be maintained.
