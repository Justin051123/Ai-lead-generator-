## 2025-05-18 - Concurrent HTTP Lead Generation Optimization

**Learning:** Processing web scrapings sequentially with blocking network requests and per-iteration delays creates severe I/O bottlenecks. Using `ThreadPoolExecutor.map` with thread-local `requests.Session` and module-level pre-compiled regex significantly speeds up lead processing while guaranteeing the original search result ranking order.

**Action:** When extracting web data across multiple URLs, always parallelize I/O bound requests using `ThreadPoolExecutor.map` and maintain connection pools via `threading.local()` sessions.
