# Bolt's Journal ⚡

## Critical Learnings

## 2026-03-23 - Parallel Lead Scraping and Thread-Local Session Reuse
**Learning:** Parallelizing I/O-bound web page scraping with `ThreadPoolExecutor.map` maintains search result ordering while eliminating sequential delays (`O(N)` network overhead + artificial sleeps). Pre-compiling regexes at module scope and using thread-local `requests.Session` instances further optimizes repeated HTTP connections and pattern evaluations.
**Action:** Use `ThreadPoolExecutor.map` and thread-local HTTP sessions for concurrent I/O requests where order matters.
