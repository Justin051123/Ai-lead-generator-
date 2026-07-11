## 2025-05-15 - Parallelizing I/O-bound Web Scraping
**Learning:** Parallelizing I/O-bound tasks like web scraping using `ThreadPoolExecutor` significantly improves performance by reducing waiting time for network responses. Using `executor.map` is preferred over `as_completed` when the order of results (e.g., search relevance) must be preserved.
**Action:** Always identify sequential I/O loops and consider parallelization with `ThreadPoolExecutor` to maximize throughput. Pre-compiling regex patterns also provides a small but valuable performance boost in batch processing.
