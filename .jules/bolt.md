## 2025-02-28 - Parallelizing I/O-Bound Web Scraping & Regex Pre-compilation

**Learning:** Sequential web scraping in `lead_gen.py` creates a severe bottleneck (taking ~1s + HTTP latency per URL). Furthermore, re-compiling the email extraction regular expression inside the request loop adds unnecessary CPU overhead for each scraped page.
**Action:** Parallelize web scraping using `concurrent.futures.ThreadPoolExecutor` with `executor.map` to preserve search result ordering, and pre-compile regular expressions (`EMAIL_PATTERN`) at module scope.
