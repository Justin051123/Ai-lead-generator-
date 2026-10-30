## 2025-05-18 - Parallelizing Web Scraping with Result Order Preservation

**Learning:** Sequential HTTP scraping of search results creates a severe I/O bottleneck, amplified by sleep delays. Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes I/O-bound web requests while preserving the search result rank ordering required for lead generation.
**Action:** When parallelizing search-result extraction in Python, use `executor.map` over `as_completed` to maintain search relevance order without requiring secondary sorting logic.
