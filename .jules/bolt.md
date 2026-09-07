## 2025-05-18 - Parallelizing I/O Scraping and Regex Pre-compilation

**Learning:** Sequential web scraping with `time.sleep(1)` creates a major delay (~1s per lead). Using `ThreadPoolExecutor` with `executor.map` parallelizes I/O-bound requests while preserving search result ordering. Pre-compiling regex avoids recompilation overhead on every extracted page.
**Action:** Always prefer `executor.map` over `as_completed` when processing I/O-bound lists where original order matters, and pre-compile module-level regexes.
