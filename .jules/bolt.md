# Bolt's Journal - Critical Learnings

## 2025-08-13 - Parallel Web Scraping Optimization
**Learning:** Sequential scraping in web applications with a static sleep delay (e.g., `time.sleep(1)`) creates a major I/O-bound bottleneck. Utilizing multi-threading with `concurrent.futures.ThreadPoolExecutor` significantly improves execution throughput. Using `executor.map` ensures we retain the original search ranking order (which is crucial for lead generator relevance) while processing requests concurrently.
**Action:** When handling independent network/scraping tasks, prefer `ThreadPoolExecutor` for parallelizing I/O-bound operations and pre-compile any regular expressions (like `EMAIL_REGEX`) at module scope to reduce CPU overhead in loops.
