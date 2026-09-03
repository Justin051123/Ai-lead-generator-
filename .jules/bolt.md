## 2025-03-03 - Parallelizing Lead Extraction with ThreadPoolExecutor

**Learning:** Sequential web scraping with artificial `time.sleep` delays and repeated regex compilation creates massive I/O bottlenecks in lead generation workflows. Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes network requests while preserving search result relevance ordering.

**Action:** For I/O-bound scraping/fetching tasks where order matters, use `ThreadPoolExecutor.map` with pre-compiled regexes instead of sequential `for` loops.
