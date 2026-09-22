## 2025-09-22 - Parallel Web Scraping & Connection Pooling

**Learning:** Sequential processing of web scraping operations with artificial delays causes massive I/O bottlenecks (10 leads took ~15s). Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes HTTP requests while preserving search ordering. Pre-compiling regex patterns and using thread-local `requests.Session` connection pools further minimizes setup overhead per request.

**Action:** For I/O-bound scraping tasks, always use concurrent thread execution and thread-local connection pooling while maintaining strict result ordering with `executor.map`.
