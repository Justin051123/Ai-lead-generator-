## 2026-03-31 - Parallelizing Web Scraping with ThreadPoolExecutor & preserving order

**Learning:** Web scraping in `lead_gen.py` was previously sequential with artificial delays (`time.sleep(1)` per lead). Parallelizing I/O-bound web requests with `ThreadPoolExecutor` and `executor.map` drastically reduces processing time while preserving search result ordering.
**Action:** When working on batch I/O operations (like scraping or fetching multiple APIs), use `ThreadPoolExecutor.map` to run requests concurrently while preserving the original input order.
