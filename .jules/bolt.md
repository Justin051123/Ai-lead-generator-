# Bolt's Journal - Critical Performance Learnings

## 2026-06-23 - Order Preservation in Parallel Lead Generation
**Learning:** In lead generation pipelines, search engine results are ranked by relevance. Using `as_completed` in `concurrent.futures.ThreadPoolExecutor` finishes out-of-order and shuffles the lead ranking. `executor.map` guarantees results remain in the exact order returned by the search engine while parallelizing I/O-bound web requests and eliminating blocking serial sleep delays.
**Action:** Always use `executor.map` when parallelizing I/O tasks where input ranking or ordering affects user experience.
