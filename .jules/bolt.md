# Bolt's Performance Journal ⚡

This journal contains critical performance learnings for the AI Lead Generator.

## 2025-07-29 - Parallel Scraping and Pre-compiled Regex
**Learning:** Sequential network scraping is a massive bottleneck in business lead discovery. Doing requests in serial with arbitrary pauses (like `time.sleep(1)`) slows down user-facing applications. Parallelizing I/O-bound scraping using `ThreadPoolExecutor` with `executor.map` speeds up throughput significantly while preserving the search result order, and pre-compiling the email matching regular expression avoids compiling it repeatedly across multiple pages.
**Action:** Always prefer concurrent scraping for multiple external websites in user-facing applications, and pre-compile standard regex patterns globally.
