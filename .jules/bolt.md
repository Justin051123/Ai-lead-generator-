# Bolt's Journal - Critical Performance Learnings

## 2026-06-23 - Concurrent Scraping & Regex Pre-compilation in Lead Generation
**Learning:** Lead generation bottlenecked on sequential HTTP requests with hardcoded `time.sleep(1)` delays and per-request regex compilation. Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` enables concurrent I/O fetching while preserving search result order, resulting in multi-fold speedups without added external dependencies.
**Action:** Parallelize network I/O operations using built-in `concurrent.futures.ThreadPoolExecutor` and pre-compile module-level regexes for text extractions.
