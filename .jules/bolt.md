## 2025-05-18 - Preserving Search Ranking Order During Concurrency
**Learning:** In lead generation pipelines where search results possess inherent rank relevance, standard concurrent worker patterns using `as_completed` yield results out-of-order, compromising lead prioritization for the end user.
**Action:** Always prefer `ThreadPoolExecutor.map` over `as_completed` when processing ordered external search lists to maintain input ordering deterministically while retaining concurrency benefits.
