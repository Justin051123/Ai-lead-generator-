## 2026-11-10 - Parallel Web Scraping & Order Preservation with ThreadPoolExecutor

**Learning:** Sequential web scraping with explicit sleep delays (e.g., `time.sleep(1)`) creates a severe I/O bottleneck in lead generation when fetching multiple business websites. Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes network I/O across worker threads while strictly preserving the original ranking order returned by the search engine, avoiding the arbitrary ordering risks of `as_completed`.

**Action:** Whenever scraping or querying multiple independent URLs whose ranking matters, use `ThreadPoolExecutor` with `executor.map` and pre-compile regular expressions at the module level.
