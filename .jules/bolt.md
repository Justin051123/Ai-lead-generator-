# Bolt's Journal - Critical Learnings Only

## 2026-07-07 - Parallelized I/O-bound Lead Scraping
**Learning:** Sequential processing with artificial delays was the primary bottleneck. Using `ThreadPoolExecutor` with `executor.map` provides a massive speedup for I/O-bound tasks while maintaining search result order.
**Action:** Always prefer parallel execution for batch web scraping tasks.
