## 2025-05-18 - Parallel Web Scraping & Regular Expression Pre-compilation
**Learning:** Web scraping in `lead_gen.py` was bound by sequential synchronous network requests (`requests.get`) and artificial delays (`time.sleep(1)`). Parallelizing via `ThreadPoolExecutor` with `executor.map` drastically reduces total lead extraction time while maintaining original search ranking order.
**Action:** Use `ThreadPoolExecutor.map` for I/O-bound scraping tasks where order preservation is required, and pre-compile regular expressions module-wide to avoid redundant compilation per URL.
