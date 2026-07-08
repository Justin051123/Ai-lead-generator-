## 2026-07-08 - Parallelize lead extraction and qualification
**Learning:** In I/O-bound lead generation tasks (like web scraping multiple domains), sequential execution with artificial delays (like `time.sleep(1)`) is a major bottleneck. Switching to `ThreadPoolExecutor` and using `executor.map` significantly increases throughput while maintaining the search result order, which is important for relevance in lead generation.
**Action:** Always look for sequential loops over network requests and parallelize them using `ThreadPoolExecutor.map` when order matters.
