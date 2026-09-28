# Bolt's Journal - Critical Performance Learnings

## 2025-05-20 - ThreadPoolExecutor with Thread-Local Sessions for Lead Extraction
**Learning:** Sequential scraping with `time.sleep(1)` creates a major bottleneck in I/O bound web scraping pipelines. Using `ThreadPoolExecutor` with `executor.map` parallelizes requests while maintaining result order, and thread-local `requests.Session` instances enable HTTP connection reuse across concurrent worker threads.
**Action:** Use `ThreadPoolExecutor` for batch I/O operations and maintain per-thread session objects via `threading.local()` for efficient HTTP pooling.
