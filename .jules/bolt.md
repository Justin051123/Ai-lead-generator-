# Bolt's Performance Journal

## 2026-07-30 - Parallelizing I/O-Bound Scrapers with ThreadPoolExecutor
**Learning:** In sequential web scraping architectures, I/O latency blocks the entire thread, leading to high processing times that scale linearly with the number of leads. By parallelizing web scraping using `ThreadPoolExecutor` and maintaining original order via `executor.map`, we can dramatically improve processing times without sacrificing search relevance. Pre-compiling regex patterns avoids recompilation overhead across iterations.
**Action:** Use `ThreadPoolExecutor` and `executor.map` to parallelize I/O-bound web-scraping pipelines, and precompile regex patterns used in repeated operations.
