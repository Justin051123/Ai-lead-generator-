## 2026-06-23 - Parallelizing Web Scraping for Lead Generation

**Learning:** Batch lead web scraping in `lead_gen.py` was strictly sequential and included artificial 1-second `time.sleep` delays between requests. For I/O-bound network scraping, `concurrent.futures.ThreadPoolExecutor` paired with `requests.Session()` connection pooling drastically reduces processing latency while maintaining exact search result ordering via `executor.map`.

**Action:** Whenever scraping or making concurrent HTTP calls where order matters, use `ThreadPoolExecutor` with `executor.map` and pass a shared `requests.Session()` to avoid TCP/TLS handshake overhead.
