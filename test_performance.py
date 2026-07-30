import time
from unittest import mock
import lead_gen

# A list of mock URLs
MOCK_URLS = [
    "http://example-plumber-1.com",
    "http://example-plumber-2.com",
    "http://example-plumber-3.com",
    "http://example-plumber-4.com",
    "http://example-plumber-5.com"
]

def mock_get(url, *args, **kwargs):
    # Simulate network/scraping I/O latency of 0.5 seconds
    time.sleep(0.5)
    mock_resp = mock.Mock()
    mock_resp.status_code = 200
    mock_resp.text = f"<html><title>Plumber {url}</title><body>Contact: info@test.com</body></html>"
    return mock_resp

def run_sequential(urls):
    """Simulates the old sequential way with sleep(1) between requests."""
    leads = []
    for url in urls:
        info = lead_gen.extract_info(url)
        leads.append(lead_gen.qualify_lead(info))
        time.sleep(1)  # Be polite sleep from old version
    return leads

def run_parallel(urls):
    """Runs the new parallel way."""
    from concurrent.futures import ThreadPoolExecutor
    max_workers = min(10, len(urls))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        leads = list(executor.map(lead_gen.process_single_lead, urls))
    return leads

def main():
    print("=== PERFORMANCE BENCHMARK ===")
    print(f"Processing {len(MOCK_URLS)} URLs...")

    with mock.patch("requests.get", side_effect=mock_get):
        # 1. Sequential Run
        start_seq = time.perf_counter()
        seq_leads = run_sequential(MOCK_URLS)
        end_seq = time.perf_counter()
        seq_time = end_seq - start_seq
        print(f"Sequential Execution Time: {seq_time:.4f} seconds")

        # 2. Parallel Run
        start_par = time.perf_counter()
        par_leads = run_parallel(MOCK_URLS)
        end_par = time.perf_counter()
        par_time = end_par - start_par
        print(f"Parallel Execution Time: {par_time:.4f} seconds")

        # Assert results match
        assert len(seq_leads) == len(par_leads), "Results count mismatch!"
        for s, p in zip(seq_leads, par_leads):
            assert s["url"] == p["url"], f"URL mismatch: {s['url']} vs {p['url']}"
            assert s["title"] == p["title"], f"Title mismatch: {s['title']} vs {p['title']}"
            assert s["email"] == p["email"], f"Email mismatch: {s['email']} vs {p['email']}"

        speedup = seq_time / par_time
        print(f"⚡ Speedup: {speedup:.1f}x faster!")
        print("Benchmark completed successfully and verified correctness of results.")

if __name__ == "__main__":
    main()
