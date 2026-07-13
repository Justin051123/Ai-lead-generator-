## 2025-05-14 - Threaded Lead Processing
**Learning:** Parallelizing I/O-bound web scraping using `ThreadPoolExecutor` with `executor.map` significantly improves performance while preserving the original search result order. Removing sequential `time.sleep(1)` when processing multiple domains maximizes throughput.
**Action:** Always prefer `executor.map` for parallelizing web scraping tasks where order matters.
