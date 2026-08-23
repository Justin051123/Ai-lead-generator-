## 2026-06-23 - Parallel Lead Generation with Order Preservation

**Learning:** Lead generation web scraping was doing sequential HTTP requests with `time.sleep(1)` between iterations. Switching to `concurrent.futures.ThreadPoolExecutor` with `executor.map` allowed concurrent I/O execution while preserving search result order without race conditions. Pre-compiling regex at module level also avoided repeated pattern compilation.

**Action:** When parallelizing I/O-bound scraping tasks where input order matters, use `ThreadPoolExecutor.map` to execute requests concurrently while maintaining exact input list ordering.
