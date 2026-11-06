# Bolt's Performance Journal

Critical performance learnings and architectural insights for the AI Lead Generator codebase.

## 2026-06-23 - Sequential HTTP Scraping Bottleneck
**Learning:** Sequential scraping of search results with individual HTTP GET requests and `time.sleep(1)` polite delay takes O(N) linear time (e.g., 10 leads taking 10-20+ seconds). Parallelizing URL extraction with `ThreadPoolExecutor` and removing the sequential loop delay while preserving search result ordering reduces I/O wait times significantly (by up to 80-90% for typical batch sizes).
**Action:** Use `concurrent.futures.ThreadPoolExecutor` with `executor.map` to preserve result order for I/O-bound web scraping requests.
