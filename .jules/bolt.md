## 2025-08-28 - Parallelizing Web Scraping Pipeline with ThreadPoolExecutor

**Learning:** The lead generation pipeline performs network I/O (`requests.get`) sequentially for each business website returned by Google Search, plus artificial `time.sleep(1)` delays. In I/O-bound scraping workflows where result ordering matters, `concurrent.futures.ThreadPoolExecutor` paired with `executor.map` parallelizes network execution while strictly preserving search ranking order.

**Action:** Use `ThreadPoolExecutor` with `executor.map` for batch web scraping or network requests to maximize throughput while maintaining input ordering. Pre-compile module-level regex patterns (`re.compile`) when processing batch text payloads across threads.
