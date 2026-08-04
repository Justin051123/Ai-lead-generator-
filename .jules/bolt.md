# Bolt's Journal - Critical Learnings Only

## 2026-06-23 - Parallelizing I/O-bound Web Scraping in Python
**Learning:** Sequential processing of multiple HTTP requests with artificial sleep delays introduces a massive performance bottleneck. Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` maintains the order of crawled URLs (crucial for search relevance) while performing requests concurrently, and removing `time.sleep(1)` when switching to concurrent calls dramatically reduces overall processing time without violating safety parameters since different domains are being queried.
**Action:** Use `ThreadPoolExecutor` and `executor.map` when crawling/scraping external URLs where the initial query result order is important.

## 2026-06-23 - Regex Compilation for Efficient Batch Processing
**Learning:** Re-compiling email regular expressions inside hot-loops can introduce minor CPU overhead. Pre-compiling the expression pattern at the module level using `re.compile` is a simple yet effective way to save micro-seconds during high-throughput text processing.
**Action:** Always pre-compile regex patterns as module-level constants (e.g., `EMAIL_REGEX`) when matching text in multiple documents.
