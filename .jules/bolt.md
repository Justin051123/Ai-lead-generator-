## 2025-05-14 - Parallelize lead processing
**Learning:** Parallelizing I/O-bound web scraping tasks using `ThreadPoolExecutor` significantly reduces the total execution time for lead generation. Sequential processing with `time.sleep(1)` was the primary bottleneck.
**Action:** Always consider `ThreadPoolExecutor` for multiple independent network requests to different domains.
