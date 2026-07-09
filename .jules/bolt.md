## 2025-05-14 - Parallelize lead processing and optimize regex
**Learning:** Sequential processing with an artificial `time.sleep(1)` creates a significant bottleneck in lead generation, especially as the number of leads increases. Using `ThreadPoolExecutor.map` can parallelize I/O-bound web scraping while maintaining search result order.
**Action:** Parallelize the lead generation loop and pre-compile the email regex to improve performance.

### Baseline Metrics (Sequential)
- **Environment:** Mocked search and requests (0.5s network latency)
- **Results:** 5 leads
- **Duration:** 7.51 seconds
- **Bottleneck:** O(n) sequential execution + 1s artificial delay per lead.
