## 2026-06-23 - Concurrent Lead Fetching & Regex Pre-compilation

**Learning:** Scraping sequential lead websites with explicit `time.sleep` delays created a major I/O bottleneck in `lead_gen.py`. Replacing sequential loops with `concurrent.futures.ThreadPoolExecutor` and using thread-local `requests.Session` instances (connection pooling) allows concurrent page fetches while preserving search result order via `executor.map`. Additionally, pre-compiling the email extraction regex at module level avoids repeated regex pattern compilation during scraping.

**Action:** For network I/O bound batch operations in Python, prefer `ThreadPoolExecutor` with `executor.map` to preserve result ordering, paired with thread-local sessions for connection reuse.
