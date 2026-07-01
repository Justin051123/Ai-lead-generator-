## 2025-05-15 - Parallelizing Lead Generation
**Learning:** Sequential processing of external web requests (scraping) is a major bottleneck in lead generation applications. Using `ThreadPoolExecutor` with `executor.map` allows for significant speedups while preserving the order of search results, which is important for search relevance.
**Action:** Always consider parallelizing I/O-bound tasks like web scraping. Use `executor.map` to maintain input ordering if relevant.
