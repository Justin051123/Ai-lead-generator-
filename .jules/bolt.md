## 2025-10-07 - Parallel Scraping & Thread-Local Session Reuse
**Learning:** Sequential HTTP scraping with artificial `time.sleep(1)` delays and per-request `requests.get` socket creation is the primary bottleneck for lead generation. `ThreadPoolExecutor` combined with `executor.map` parallelizes I/O requests while preserving search result order.
**Action:** Use thread-local `requests.Session` instances and `ThreadPoolExecutor.map` when batch processing URLs in `lead_gen.py`.
