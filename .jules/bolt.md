## 2026-07-06 - Parallel Lead Extraction
**Learning:** Sequential processing with artificial delays (`time.sleep(1)`) was the primary bottleneck in `lead_gen.py`. Replacing this with `ThreadPoolExecutor` and `executor.map` allows for concurrent I/O-bound web scraping while maintaining search result order.
**Action:** Use `ThreadPoolExecutor` for I/O-bound tasks where order matters, and always check for/remove unnecessary sequential delays when parallelizing.
