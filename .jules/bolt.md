## 2026-06-23 - Parallel Lead Extraction & Regex Pre-compilation

**Learning:** Sequential HTTP requests with artificial delays (`time.sleep`) in web scraping pipelines create severe execution bottlenecks (e.g. 10 leads took >10-15s). Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` enables parallel I/O-bound web requests while preserving original search result ordering.
**Action:** Always parallelize web scraping I/O tasks using thread pools and pre-compile regex patterns used across repeated extraction calls.
