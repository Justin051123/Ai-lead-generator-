## 2026-07-05 - Parallelizing I/O-Bound Lead Generation
**Learning:** Sequential processing of URLs with artificial delays (`time.sleep`) is a massive bottleneck for lead generation apps. Switching to `ThreadPoolExecutor` and removing the sequential sleep reduced execution time by ~93% (from 7.5s to 0.5s for 5 leads). Pre-compiling regex also reduces micro-overhead in batch processing.
**Action:** Always prefer `ThreadPoolExecutor` for I/O-bound scraping tasks. Use `executor.map` to maintain result order when search relevance matters.
