# Bolt's Performance Journal

## 2025-10-25 - Parallel Lead Scraping and Pre-compiled Regex
**Learning:** Sequential HTTP fetches with sequential delays in web scraping pipelines slow down response time linearly with lead count ($O(N)$). Using `ThreadPoolExecutor` and `executor.map` parallelizes I/O operations while maintaining original search result ordering without breaking UI expectations.
**Action:** Always prefer concurrent map execution for I/O bound batch scraping tasks, pre-compile regex patterns at module scope, and eliminate unneeded artificial delays.
