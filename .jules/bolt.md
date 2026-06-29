## 2025-05-15 - Parallel Lead Extraction
**Learning:** Sequential processing of multiple URLs for lead generation was a major bottleneck due to network I/O and artificial delays (`time.sleep`). Even with a 1s delay per lead, 10 leads took ~15s.
**Action:** Used `concurrent.futures.ThreadPoolExecutor` to parallelize network-bound tasks. This drastically improved throughput without sacrificing readability.
