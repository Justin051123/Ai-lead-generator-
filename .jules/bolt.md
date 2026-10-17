## 2026-06-23 - Parallelizing I/O-bound web scraping with ThreadPoolExecutor

**Learning:** Web scraping sequential loops with `requests.get` and artificial delay (`time.sleep(1)`) are a major I/O bottleneck in lead generation workflows. Replacing sequential iteration with `ThreadPoolExecutor(max_workers=...)` and `executor.map` parallelizes network requests while automatically preserving result ranking order. Pre-compiling regex pattern `EMAIL_PATTERN` at the module level avoids redundant compilation across worker threads.
**Action:** When handling batches of HTTP requests where response order matters, use `ThreadPoolExecutor.map` with a worker cap bounded by input size to eliminate sequential latency overhead.
