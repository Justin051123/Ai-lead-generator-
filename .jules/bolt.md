## 2026-06-23 - Parallelizing Web Scraping with ThreadPoolExecutor

**Learning:** Lead generation web scraping was previously sequential with artificial delays (`time.sleep(1)`), causing 10 leads to take upwards of 15+ seconds. Web scraping is an I/O-bound task where `ThreadPoolExecutor` with `executor.map` can parallelize HTTP requests and page parsing while maintaining search result ranking order.
**Action:** Use `ThreadPoolExecutor` for batch HTTP requests in Python and pre-compile module-level regex patterns (`re.compile`) to avoid repeated string parsing overhead.
