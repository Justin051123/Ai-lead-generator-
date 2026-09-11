## 2025-09-11 - Parallel I/O Lead Generation with Order Preservation

**Learning:** Sequential scraping of search results with `requests.get` and artificial delays creates massive latency bottlenecks (~N * (I/O latency + delay)). Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes network I/O while strictly preserving the original search relevance ordering of results. Additionally, pre-compiling regular expressions avoids repeated pattern compilation overhead across scraped pages.

**Action:** When performing I/O-bound web scraping or API calls where order matters, use `ThreadPoolExecutor` with `executor.map` instead of sequential loops or `as_completed`, and pre-compile any module-level regexes.
