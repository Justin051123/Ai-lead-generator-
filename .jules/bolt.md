# Bolt's Journal - Critical Learnings

## 2025-05-20 - Parallel I/O bound lead scraping
**Learning:** Sequential scraping with `time.sleep(1)` creates a significant delay per lead. Parallelizing requests via `ThreadPoolExecutor` and pre-compiling regex patterns reduces lead generation latency dramatically while preserving result ordering with `executor.map`.
**Action:** Use `ThreadPoolExecutor.map` for I/O bound HTTP requests when input/output ordering must be preserved.
