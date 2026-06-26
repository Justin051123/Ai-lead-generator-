## 2026-06-26 - [Parallelize Lead Extraction]
**Learning:** Sequential processing of multiple URLs for web scraping is a major bottleneck due to I/O-bound operations. Even with a polite `time.sleep(1)`, the total execution time scales linearly with the number of leads.
**Action:** Use `concurrent.futures.ThreadPoolExecutor` to parallelize I/O-bound tasks like fetching website content. This can lead to significant (e.g., 7x) performance improvements for typical lead counts (5-10) without overloading the target servers excessively, provided the `max_workers` is reasonable.
