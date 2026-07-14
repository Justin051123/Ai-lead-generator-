## 2025-05-14 - Parallel Lead Processing Optimization
**Learning:** Sequential lead processing with artificial `time.sleep` is a major bottleneck for I/O-bound scraping tasks. Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` significantly improves throughput while maintaining original search result order.
**Action:** Always prefer parallelization for independent network requests. Pre-compile regex patterns when used in a loop across many documents to save CPU cycles.
