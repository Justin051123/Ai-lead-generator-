## 2025-02-19 - Parallelizing I/O-Bound Scraping while Preserving Relevance Order

**Learning:**
In search-based lead generation, maintaining the search relevance order returned by the Google Search API is crucial. Simple parallelization using `concurrent.futures.as_completed` yields results in completion order, which scrambles the relevance hierarchy. Using `concurrent.futures.ThreadPoolExecutor` with `executor.map` preserves the order of inputs. Additionally, removing artificial `time.sleep(1)` delays between sequential scrapes in a parallel execution context maximizes speedups without hitting the same domain repeatedly, since each lead is on a different domain.

**Action:**
Utilize `executor.map` instead of `as_completed` for ordering-sensitive parallel pipelines in Python. Pre-compile regex expressions globally to avoid compilation overhead inside worker threads.
