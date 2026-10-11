## 2025-05-18 - ThreadPoolExecutor with executor.map for Ordered Lead Processing

**Learning:** When web scraping multiple URLs, sequential execution with artificial `time.sleep` delays severely degrades user experience (~10s for 10 leads). Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes I/O-bound web requests while preserving original search result ordering. Combining this with thread-local `requests.Session` instances enables connection reuse across concurrent worker threads.

**Action:** Implement `ThreadPoolExecutor` and `threading.local()` session management for all multi-site web scraping pipelines.
