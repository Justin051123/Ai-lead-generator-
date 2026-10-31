## 2026-10-31 - Parallel Lead Generation & Regex Pre-compilation
**Learning:** Sequential scraping with sleep delays (`time.sleep(1)`) turned I/O latency into a major bottleneck (5.5s for 5 leads). Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes network requests without altering the relevance ordering of search results and drops processing time down to ~0.1s in simulated benchmarks.
**Action:** When handling multi-URL web scraping pipelines, use thread pools with `executor.map` to preserve result order and avoid sequential blocking sleeps.
