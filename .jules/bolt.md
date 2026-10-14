# Bolt's Journal - Critical Learnings

## 2025-05-20 - Concurrent Lead Extraction with ThreadPoolExecutor & Session Reuse
**Learning:** Sequential website scraping with sequential `time.sleep(1)` delays and per-request socket overhead creates a major I/O bottleneck in lead generation. `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes I/O-bound requests while strictly maintaining the original search result ranking order.
**Action:** Use `ThreadPoolExecutor` and thread-local `requests.Session()` instances for batch network scraping while preserving search result order with `executor.map`.
