# Bolt's Journal - AI Lead Generator Optimizations

## 2025-02-14 - Parallel Processing of I/O Bound Scraping & Regex Pre-compilation
**Learning:** Sequential HTTP requests in web scraping introduce a massive linear delay bottleneck, especially with artificial pauses (like `time.sleep(1)`) and network timeouts (up to 10s per site). Parallelizing these requests with `concurrent.futures.ThreadPoolExecutor` using `executor.map` ensures high throughput while preserving the original relevance-based search result order. Additionally, pre-compiling the email extraction regular expression (`EMAIL_REGEX`) avoids repeated compilation overhead during batch processing.
**Action:** Use `ThreadPoolExecutor` with `executor.map` to concurrently run the scraping tasks on a helper function `process_single_lead(url)` and pre-compile any reused regex patterns.
