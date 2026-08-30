## 2026-08-30 - Parallel I/O lead scraping with order preservation

**Learning:** Web scraping multiple lead URLs sequentially with sleep delays creates a severe I/O bottleneck. Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` parallelizes network fetch latencies while maintaining exact input order of search results without requiring `as_completed` sorting overhead.
**Action:** Use `ThreadPoolExecutor.map` for I/O-bound web fetching tasks where result order matters.

## 2026-08-30 - Module-level Regex Compilation for Batch Scraping

**Learning:** Compiling regex patterns (such as email extraction regexes) inside loop functions forces redundant regex parsing on every scraped web page. Pre-compiling regexes at the module scope improves batch execution speed.
**Action:** Always compile static regex patterns at the module top-level in Python scraping modules.
