## 2025-05-15 - Parallelizing Lead Generation
**Learning:** Sequential processing of URLs during lead generation was the primary bottleneck, exacerbated by "polite" delays. Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` allowed for parallel execution while preserving the original search result order, which is critical for maintaining lead relevance.
**Action:** When parallelizing I/O-bound tasks where input order matters (like search relevance), prefer `executor.map` over `as_completed` to maintain result ordering.
