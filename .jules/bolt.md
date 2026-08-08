# Bolt's Journal - Critical Learnings Only

## 2025-08-08 - Parallelization of Lead Generation
**Learning:** Web scraping of discovered leads is highly I/O-bound. Running requests sequentially with a `time.sleep(1)` polite delay restricts throughput significantly. Transitioning to a parallelized approach using `concurrent.futures.ThreadPoolExecutor` allows multiple web scrapes to occur simultaneously. Furthermore, using `executor.map` is ideal because it preserves the order of search results from the search engine, which translates to keeping higher relevance results at the top.
**Action:** Replace the sequential loop over scraped websites with a parallel pool execution (`ThreadPoolExecutor`), modularize the lead scraping into a standalone helper `process_single_lead(url)` to keep it clean, pre-compile the email regex pattern, and remove the sequential `time.sleep` delay to maximize performance.
