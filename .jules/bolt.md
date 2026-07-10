## 2025-05-14 - Parallelize lead processing and optimize regex
**Learning:** Web scraping is heavily I/O-bound. Replacing sequential processing and an artificial 1-second delay with `ThreadPoolExecutor` and `executor.map` drastically improves performance (from ~5.5s to ~0.1s in mock benchmarks) while preserving search result order. Pre-compiling regex patterns also adds a small efficiency boost for batch processing.
**Action:** Always prefer `ThreadPoolExecutor` for parallelizing I/O-bound tasks in Python, especially when scraping multiple domains. Use `executor.map` to maintain input order.
