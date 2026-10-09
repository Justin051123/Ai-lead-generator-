## 2026-06-23 - Concurrency and Session Reuse in Lead Generation

**Learning:** Processing lead websites sequentially with blocking `time.sleep(1)` delays was the main bottleneck in lead discovery. In I/O-bound web scraping, using `ThreadPoolExecutor` with `executor.map` parallelizes requests while maintaining Google search result ranking order. Additionally, managing `requests.Session` in thread-local storage (`threading.local()`) enables TCP connection pooling without sharing sessions across threads, and pre-compiling regex avoids redundant compilation.

**Action:** For network I/O batch pipelines where ordering matters, use `ThreadPoolExecutor` + `executor.map` combined with thread-local HTTP sessions and pre-compiled regex.
