## 2025-05-15 - Parallelize I/O-bound web scraping
**Learning:** Web scraping and info extraction are highly I/O-bound. Using a `ThreadPoolExecutor` can significantly reduce the total execution time by overlapping network requests.
**Action:** Always consider parallelization for sequential network requests. Use `ThreadPoolExecutor` for Python I/O tasks and ensure order preservation if needed using `executor.map`.
