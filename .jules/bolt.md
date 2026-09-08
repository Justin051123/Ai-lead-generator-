# Bolt's Journal - Critical Learnings

## 2025-09-08 - Parallelizing Web Scraping with ThreadPoolExecutor

**Learning:** Sequential HTTP requests with artificial `time.sleep(1)` delays create severe performance bottlenecks in web scraping tasks. Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes I/O-bound requests while maintaining the original search result ordering and eliminates artificial delays.

**Action:** When optimizing batch URL processing, use `ThreadPoolExecutor` and `executor.map` to execute requests concurrently while preserving order, and pre-compile regex patterns at the module level to reduce per-request overhead.
