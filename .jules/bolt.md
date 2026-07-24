# Bolt's Journal ⚡

## 2026-06-23 - Parallel Web Scraping & Order Preservation
**Learning:** In the AI lead generator, lead processing is heavily I/O-bound (web requests). Performing these requests sequentially with an artificial `time.sleep(1)` delay creates a major bottleneck where total execution time scales linearly. Parallelizing this with a standard thread pool executor significantly improves throughput, but using generic `as_completed` can disrupt the original search relevancy ranking of the leads. Utilizing `executor.map` is crucial as it automatically maintains the correct input/output ordering of leads while executing scraping in parallel.
**Action:** Always use `ThreadPoolExecutor` with `executor.map` rather than `as_completed` when parallelizing I/O-bound tasks in Python where original list order (such as search relevance ranking) must be preserved.
