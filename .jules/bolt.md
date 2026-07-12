# Bolt's Journal - Critical Learnings

## 2025-05-14 - Parallel Lead Processing Optimization
**Learning:** Sequential processing of leads with artificial `time.sleep(1)` delays and repeated regex compilation is a major bottleneck for I/O-bound web scraping. Parallelizing with `ThreadPoolExecutor` and pre-compiling regex significantly improves throughput.
**Action:** Use `ThreadPoolExecutor.map` for I/O-bound tasks where order matters, and always pre-compile regex patterns used in loops.
