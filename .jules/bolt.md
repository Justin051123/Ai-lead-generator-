## 2026-06-23 - Parallel Lead Scraping with ThreadPoolExecutor
**Learning:** In `lead_gen.py`, web scraping each search result sequentially with artificial `time.sleep(1)` delays caused severe latency (~6s for 5 leads). Parallelizing I/O-bound web requests using `concurrent.futures.ThreadPoolExecutor` with `executor.map` maintains exact lead ordering while removing sequential delays.
**Action:** When parallelizing I/O-bound tasks in Python where input order matters (like search relevance), prefer `executor.map` over `as_completed` to maintain result ordering.
