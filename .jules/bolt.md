# Bolt's Optimization Journal ⚡

Only critical, non-obvious performance learnings go here.

## 2026-06-23 - ThreadPoolExecutor Order & Clean parallelization
**Learning:** When parallelizing web scraping or API queries, using `as_completed` returns results in completion order, which destroys the relevance ranking of Google search results. Using `ThreadPoolExecutor.map` preserves the input list's original order seamlessly. Also, artificial delays like `time.sleep(1)` must be removed when shifting to parallel execution to fully maximize thread throughput, since the requests hit different external domains rather than the same server.
**Action:** Always prefer `executor.map` over `as_completed` when output order/relevance matters, and eliminate sequential sleep timers for different domains.

## 2026-06-23 - Ruff E741 Name Constraints in Parallel Loops
**Learning:** When using thread pools or inline comprehensions, it is easy to default to shorthand names like `l`. However, Ruff's E741 rule prohibits ambiguous single-character variables (like `l`, `I`, `O`).
**Action:** Use unambiguous variable names like `lead` or `url` even in local lambdas, loop vars, or list comprehensions.
