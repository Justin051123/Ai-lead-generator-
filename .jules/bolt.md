## 2025-05-14 - Parallelize I/O-bound web scraping
**Learning:** Sequential processing of multiple websites for lead generation is a major bottleneck due to network latency and intentional delays. Using `ThreadPoolExecutor` can provide nearly an 10x speedup for typical search result sizes (10-20 leads) without significant complexity.
**Action:** Always check for sequential network requests in loops and consider `ThreadPoolExecutor` (for I/O) or `ProcessPoolExecutor` (for CPU) for easy performance gains.
