## 2025-10-01 - Parallelizing lead scraping with ThreadPoolExecutor and thread-local Session connection pooling

**Learning:** When fetching website leads, sequential execution with artificial `time.sleep` delays creates a severe bottleneck (~5s for 10 leads @ 500ms network latency). Parallelizing I/O-bound web requests using `concurrent.futures.ThreadPoolExecutor` with `executor.map` reduces processing time to ~0.5s (9.9x speedup) while maintaining search result order. Reusing `requests.Session` per thread via `threading.local()` avoids TCP connection overhead.

**Action:** For I/O-bound batch HTTP requests where search ranking matters, use `ThreadPoolExecutor.map` with thread-local `requests.Session` instances and pre-compiled regex patterns.
