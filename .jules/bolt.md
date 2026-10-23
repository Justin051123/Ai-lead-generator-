# Bolt's Journal - Critical Learnings

## 2025-05-10 - Parallel Lead Scraping and Regex Compilation
**Learning:** Sequential web scraping with artificial per-page sleeps is the primary bottleneck in lead generation workflows; using `ThreadPoolExecutor` with `executor.map` parallelizes network I/O while preserving search result ordering. Pre-compiling regex patterns avoids overhead across repeated extractions.
**Action:** Use `ThreadPoolExecutor` with `executor.map` for I/O-bound scraping tasks and compile regex patterns at module level.
