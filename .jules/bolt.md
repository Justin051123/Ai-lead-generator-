# Bolt's Journal - Critical Learnings

## 2026-10-15 - Concurrent Web Scraping with ThreadPoolExecutor

**Learning:** Web scraping and lead generation in `lead_gen.py` were bottlenecked by sequential I/O requests and artificial `time.sleep(1)` delays. Concurrent execution using `ThreadPoolExecutor` and `executor.map` preserves search result ordering while dramatically improving throughput.
**Action:** Use thread-local `requests.Session` instances and `ThreadPoolExecutor.map` for I/O-bound scraping tasks to optimize parallel requests without altering result sequence.
