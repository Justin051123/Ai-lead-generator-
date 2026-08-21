## 2026-06-23 - Parallelizing Web Scraping in Lead Generation

**Learning:** Web page fetching (`requests.get`) and extraction in `lead_gen.py` were executed sequentially with artificial `time.sleep(1)` delays, making lead generation take O(N * (latency + 1s)). Since network requests are I/O bound, using `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes network requests while maintaining search result order.
**Action:** When scraping multiple web pages sequentially, wrap individual URL processing in a helper and use `ThreadPoolExecutor` with `executor.map` to optimize I/O-bound throughput while keeping result ordering.
