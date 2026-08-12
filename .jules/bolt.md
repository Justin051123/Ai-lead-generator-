# Bolt's Journal

This journal records critical performance learnings specific to this codebase.

## 2026-06-23 - Parallel Lead Generation Pipeline
**Learning:** Sequential HTTP scraping of search results creates a major blocking bottleneck (especially with artificial polite sleep calls). Utilizing `concurrent.futures.ThreadPoolExecutor` with `executor.map` successfully parallelizes these I/O-bound requests while preserving the original relevance ranking of search results. Pre-compiling the email regular expression as a module-level constant also avoids redundant compilation overhead.
**Action:** Always prefer `ThreadPoolExecutor.map` over sequential loops or unordered concurrent tools for ordered scraping workflows, and compile regex patterns globally to maximize efficiency.
