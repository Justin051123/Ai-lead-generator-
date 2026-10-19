## 2026-06-23 - Concurrent Lead Scraping with ThreadPoolExecutor

**Learning:** Sequential web scraping with `requests.get` and artificial `time.sleep` delays created a major bottleneck (~12s for 10 leads). Since web scraping is heavily I/O-bound, using `ThreadPoolExecutor` with `executor.map` enables parallel execution while strictly preserving search result ranking. Pre-compiling regex patterns (`re.compile`) avoids redundant regex compilation during batch scraping.
**Action:** Always parallelize I/O-bound scraping tasks using `ThreadPoolExecutor` and `executor.map` to preserve result ordering, and pre-compile regular expressions used repeatedly across iterations.
