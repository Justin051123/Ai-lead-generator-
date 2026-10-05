## 2026-06-23 - Parallel Lead Generation & Thread-Local Session Reuse

**Learning:** Processing web scraping targets sequentially with artificial delays (`time.sleep(1)`) and creating new HTTP connections per request creates severe I/O bottlenecks (e.g. 10 leads taking ~12s). Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes I/O requests while maintaining the original search ranking order. Utilizing `threading.local()` to reuse `requests.Session` instances per worker thread further optimizes HTTP connection pooling without thread safety issues.

**Action:** For I/O-bound web scraping pipelines where order matters, use `executor.map` with `ThreadPoolExecutor` and thread-local HTTP sessions to achieve multi-fold throughput improvements while preserving result order.
