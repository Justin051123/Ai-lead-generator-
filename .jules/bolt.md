# Bolt's Journal - Critical Learnings Only

This journal contains only critical learnings to avoid mistakes or make better decisions.

## 2026-06-23 - ThreadPoolExecutor Speedups
**Learning:** Found that the lead processing was done sequentially with an artificial sleep delay of 1 second between processing each URL, resulting in very slow execution when processing many leads (e.g., 5-50 leads). Utilizing concurrent.futures.ThreadPoolExecutor with executor.map to perform web scraping concurrently provides massive throughput speedups (up to ~10x for 5 leads) while preserving original search result order.
**Action:** Parallelize I/O-bound web scraping using ThreadPoolExecutor and executor.map instead of sequential loops, and avoid artificial sleep delays during parallel runs.
