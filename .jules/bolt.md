## 2026-06-23 - Parallel Lead Extraction & Connection Reuse

**Learning:** Lead processing in `lead_gen.py` was previously sequential with a hardcoded `time.sleep(1)` per URL, resulting in linear processing time ($O(N)$ network latency).
**Action:** Use `concurrent.futures.ThreadPoolExecutor` along with `requests.Session` and pre-compiled regex patterns to scrape leads concurrently while maintaining search result order.
