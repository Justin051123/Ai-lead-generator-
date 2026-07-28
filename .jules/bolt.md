# Bolt's Journal

## 2025-07-28 - Parallelizing Web Scraping and Regex Optimization
**Learning:** Parallelizing I/O-bound operations using `ThreadPoolExecutor` alongside compiling regular expressions significantly improves throughput. Using `executor.map` ensures we preserve the input search query order for leads.
**Action:** Replace sequential web scraping loops with `ThreadPoolExecutor` and map operations, pre-compile Regex patterns, and remove sequential blocking delays like `time.sleep(1)`.
