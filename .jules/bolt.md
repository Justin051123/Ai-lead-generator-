# Bolt Journal ⚡

## 2024-10-12 - Parallelizing Lead Generation Web Scraping
**Learning:** Sequential web scraping with `time.sleep(1)` introduced an artificial ~1s delay per lead in addition to network I/O latency. Switching to `ThreadPoolExecutor` with `executor.map` parallelized I/O requests across threads while preserving search result order.
**Action:** Use `ThreadPoolExecutor` for concurrent web scraping in Python applications where order matters.
