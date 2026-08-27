## 2026-06-23 - Parallelizing Web Scraping with ThreadPoolExecutor

**Learning:** Web scraping and lead extraction in `lead_gen.py` were previously processed sequentially in a single-threaded loop with an artificial `time.sleep(1)` delay between requests, resulting in ~5.5 seconds total runtime for 5 leads. Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` enables parallel I/O processing while preserving search result order, bringing processing time down to ~0.1s for 5 leads. Additionally, pre-compiling the regex pattern `EMAIL_PATTERN` at module load time avoids redundant compilation inside request loops.

**Action:** For I/O-bound web fetching pipelines where original ranking or order matters, use `ThreadPoolExecutor` with `executor.map` and eliminate sequential sleep delays.
