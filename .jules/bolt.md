## 2026-06-23 - Parallel lead processing with ThreadPoolExecutor
**Learning:** In I/O bound lead scraping workloads, sequential processing with `time.sleep` delays severely throttles total lead generation throughput. Using `ThreadPoolExecutor.map` parallelizes network requests while guaranteeing search result ordering is preserved. Pre-compiling regex patterns avoids per-URL compilation overhead.
**Action:** When scraping or processing lists of web URLs where order matters, use `ThreadPoolExecutor.map` with pre-compiled regex objects for maximum concurrency and efficiency.
