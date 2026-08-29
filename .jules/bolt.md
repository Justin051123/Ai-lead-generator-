## 2026-08-29 - Parallel I/O Web Scraping Order Preservation
**Learning:** When fetching external business web pages concurrently in `lead_gen.py`, `concurrent.futures.ThreadPoolExecutor.map` preserves the initial search result ordering while executing requests in parallel, eliminating sequential network latency bottlenecks without scrambling result positions.
**Action:** Use `ThreadPoolExecutor.map` for I/O-bound web scraping pipelines where search relevance order is significant.
