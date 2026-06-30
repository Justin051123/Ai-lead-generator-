## 2025-05-22 - Parallel I/O with Result Order Preservation
**Learning:** When parallelizing I/O-bound tasks using `ThreadPoolExecutor`, using `as_completed` improves speed by yielding results as they finish, but loses the input order. For tasks where input rank (like search result order) matters, `executor.map` is a cleaner alternative that preserves order while still benefiting from parallel execution.
**Action:** Use `executor.map` for parallel tasks where result ordering relative to input is important.
