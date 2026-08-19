## 2026-06-23 - ThreadPoolExecutor order preservation for web scraping

**Learning:** When parallelizing I/O-bound web scraping for search results, using `concurrent.futures.ThreadPoolExecutor` with `executor.map` processes requests concurrently while preserving the original rank/order of search result URLs. Pre-compiling regex patterns (`re.compile`) at module level further eliminates compilation overhead across concurrent requests.
**Action:** Use `executor.map` instead of sequential loops or `as_completed` when order matters for lead search relevance.
