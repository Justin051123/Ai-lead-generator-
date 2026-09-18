## 2026-06-23 - Parallel Web Scraping & Connection Reuse in Lead Processing

**Learning:** Web scraping sequential loops with fixed delays and unpooled HTTP connections create a significant throughput bottleneck (e.g. 5 leads taking ~5.5s total).
**Action:** Use `concurrent.futures.ThreadPoolExecutor` with `executor.map` to preserve search result order while executing HTTP requests concurrently, reuse HTTP/TCP connections via `requests.Session`, and pre-compile module-level regular expressions (`EMAIL_PATTERN`).
