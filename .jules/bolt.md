## 2025-02-15 - Thread Pool Parallelization for I/O Bound Scraping
**Learning:** Sequential scraping with `time.sleep` results in extremely high latency. Parallelizing the network operations via `ThreadPoolExecutor` and pre-compiling regex drastically reduces search/extraction times without compromising the order of search results (when using `executor.map`).
**Action:** Always prefer `executor.map` over sequential loop or `as_completed` when processing I/O bound requests where search relevance and result order are critical.
