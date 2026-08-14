# Bolt's Journal - Critical Learnings

## 2025-08-14 - Parallelized Web Scraping for Lead Generation
**Learning:** Sequential web scraping of multiple leads incurs substantial cumulative network latency (I/O-bound bottleneck). Parallelizing the web requests using ThreadPoolExecutor with executor.map maintains result relevance ordering while bypassing sequential delay overhead.
**Action:** Always prefer concurrent.futures.ThreadPoolExecutor with executor.map for parallelized fetching of multiple external pages when order matters.
