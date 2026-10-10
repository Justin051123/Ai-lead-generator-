## 2025-10-10 - Parallelizing Web Scraping and HTTP Connection Reuse

**Learning:** Web page scraping and email extraction in `lead_gen.py` were executing sequentially with explicit `time.sleep(1)` delays and creating new HTTP connections per request. For 10 leads, network I/O latency dominated execution time (~10s+). Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelized I/O operations while preserving original search result ordering. Combining this with thread-local `requests.Session` instances enabled TCP connection reuse across concurrent requests.

**Action:** When performing I/O bound web scraping across multiple URLs where search result order is important, use `ThreadPoolExecutor` with `executor.map` and thread-local `requests.Session` instances to maximize throughput without altering output order.
