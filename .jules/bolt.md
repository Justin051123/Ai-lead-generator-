## 2025-05-15 - Reuse HTTP Connections with Requests Session
**Learning:** Re-using a single `requests.Session` instance across scraping calls avoids overhead from establishing new TCP connection handshakes and TLS negotiations for every lead URL request.
**Action:** Use a shared `requests.Session` instance or pass `session` as an optional parameter to extraction helpers when scraping multiple web pages.
