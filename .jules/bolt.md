## 2026-10-29 - Parallelize I/O lead scraping & pre-compile regex

**Learning:** Web scraping for lead extraction was previously executed sequentially with an artificial `time.sleep(1)` polite delay, causing multi-lead lookups to block the thread for 12+ seconds. Utilizing `concurrent.futures.ThreadPoolExecutor` with `executor.map` enables parallel I/O HTTP requests while preserving search result ordering without blocking. Furthermore, pre-compiling regex at the module level avoids redundant compilation overhead across multiple scraped pages.

**Action:** When handling I/O bound multi-URL fetching, parallelize using `ThreadPoolExecutor.map` to maintain response order and pre-compile regular expressions used repeatedly across iterations.
