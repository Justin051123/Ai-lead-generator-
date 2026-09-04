## 2025-09-04 - Concurrency with Order Preservation for Web Scraping

**Learning:** Web page scraping for lead generation is strictly I/O-bound. Processing leads sequentially creates a massive latency bottleneck (e.g., 10 leads at 100ms HTTP latency takes 1.0s+ sequentially vs. ~0.11s concurrently). Using `ThreadPoolExecutor.map` parallelizes I/O requests while preserving search relevance ordering without complex async event loops.

**Action:** Prefer `ThreadPoolExecutor.map` for batch I/O operations where order matters, and pre-compile module-level regex objects for repeated string extractions.
