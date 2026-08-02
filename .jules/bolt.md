# Bolt's Journal - Critical Learnings Only

## 2026-06-23 - Parallel Lead Generation Pipeline
**Learning:** Network request latency in synchronous, single-threaded scraping runs was the massive bottleneck for lead generation, taking 1.5s+ per URL due to the artificial polite delays and synchronous execution. Using ThreadPoolExecutor with `executor.map` safely parallelizes these I/O bound requests while fully preserving the original Google Search results ordering, reducing lead generation time by up to ~15x. Pre-compiling regex searches globally avoids duplicate evaluation overhead per URL.
**Action:** Always favor `executor.map` over `as_completed` when processing lists in parallel where the input ordering (like search relevance) must be strictly preserved.
