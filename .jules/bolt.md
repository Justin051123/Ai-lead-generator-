## 2026-06-23 - Parallel Lead Scraping & Thread-Local HTTP Sessions

**Learning:** Sequential web scraping with explicit `time.sleep(1)` delays and single-use `requests.get()` HTTP connections created an I/O bottleneck during lead generation. Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes I/O-bound web requests while strictly maintaining search result ordering. Additionally, thread-local `requests.Session` instances (`get_thread_session()`) enable TCP/TLS connection reuse across concurrent requests within each thread.

**Action:** For I/O-bound scraping tasks in Python where order matters, use `executor.map` with `ThreadPoolExecutor` and thread-local HTTP sessions to maximize concurrency without losing result order.
