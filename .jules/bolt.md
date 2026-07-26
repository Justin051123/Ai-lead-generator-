## 2024-07-26 - Order-Preserving Parallel Scraping
**Learning:** For web scraping search results where the order represents search relevance, utilizing parallel execution via `as_completed` destroys the relevance order. Using `ThreadPoolExecutor.map` preserves the input order while parallelizing network requests.
**Action:** Use `executor.map` to maintain input ordering when parallelizing search results.
