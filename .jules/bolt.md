## 2025-05-18 - Parallelize Web Scraping with ThreadPoolExecutor and executor.map

**Learning:** Web scraping in lead generation applications is strictly I/O-bound. Sequential fetching with synchronous delays (`time.sleep(1)`) creates severe latency bottlenecks (e.g. 10 leads taking >11 seconds). Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` and an HTTP session allows parallel fetching while preserving search ranking order without breaking downstream lead qualifications.

**Action:** Always parallelize I/O-bound web request loops using `ThreadPoolExecutor` and `executor.map` when output ranking order matters, and reuse `requests.Session()` across threads.
