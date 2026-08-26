## 2026-06-23 - Parallel Web Scraping & Regex Pre-compilation
**Learning:** Sequential HTTP requests and `time.sleep(1)` create significant I/O latency in lead extraction pipelines. Using `ThreadPoolExecutor.map` parallelizes I/O tasks while maintaining initial search result order.
**Action:** When scraping or fetching multiple independent URLs, use `ThreadPoolExecutor.map` and pre-compile regex patterns at the module scope.
