## 2025-02-23 - Initial Parallelization & Optimization
**Learning:** Sequential, blocking network I/O in scraping operations creates a massive performance bottleneck. Implementing parallel execution using a `ThreadPoolExecutor` and pre-compiling regular expressions significantly boosts execution throughput. Using `executor.map` is preferable over `as_completed` when maintaining the original search result order is important.
**Action:** Always refactor sequential I/O-bound loops into parallelized executions with safe timeouts and pre-compiled regex patterns to minimize overhead.
