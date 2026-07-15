## 2025-05-14 - Parallelize I/O bound lead processing
**Learning:** Sequential processing of leads with artificial delays (`time.sleep(1)`) creates a massive bottleneck. Moving to `ThreadPoolExecutor` allows multiple web requests to happen concurrently, which is ideal for I/O-bound scraping tasks. Pre-compiling regex also provides a minor but important efficiency gain during batch processing.
**Action:** Use `ThreadPoolExecutor.map` for I/O bound tasks where order matters. Pre-compile regex patterns that are used in loops.
