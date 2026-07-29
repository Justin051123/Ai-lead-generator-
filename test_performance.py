import unittest
from unittest.mock import patch, MagicMock
import time
from lead_gen import generate_leads, qualify_lead

# Simulated delay for network request
MOCK_NETWORK_DELAY = 0.5
MOCK_URLS = [
    "http://example-biz-1.com",
    "http://example-biz-2.com",
    "http://example-biz-3.com",
    "http://example-biz-4.com",
    "http://example-biz-5.com",
]


def mock_sequential_generate_leads(urls):
    """Simulates the old sequential lead generation logic."""
    leads = []
    for url in urls:
        # Simulate network request delay + extract + qualify
        time.sleep(MOCK_NETWORK_DELAY)
        info = {"url": url, "email": "info@example.com", "title": f"Business {url}"}
        leads.append(qualify_lead(info))
        time.sleep(1)  # Simulates polite sleep
    return leads


class TestPerformance(unittest.TestCase):
    @patch("lead_gen.search")
    @patch("lead_gen.requests.get")
    def test_parallel_performance_gain(self, mock_get, mock_search):
        # Setup mocks
        mock_search.return_value = MOCK_URLS

        # Mock requests.get response
        def mock_get_impl(url, *args, **kwargs):
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.text = f"<html><title>Business {url}</title><body>Email us at info@example.com</body></html>"
            # Simulate real network I/O block
            time.sleep(MOCK_NETWORK_DELAY)
            return mock_resp

        mock_get.side_effect = mock_get_impl

        # Measure Sequential Execution
        print("\nRunning simulated sequential processing of leads...")
        start_seq = time.time()
        seq_leads = mock_sequential_generate_leads(MOCK_URLS)
        seq_duration = time.time() - start_seq
        print(
            f"Sequential duration for {len(MOCK_URLS)} leads: {seq_duration:.3f} seconds"
        )

        # Measure Parallel Execution (Optimized)
        print("Running optimized parallel processing of leads...")
        start_par = time.time()
        par_leads = generate_leads("Niche", "Location", num_results=len(MOCK_URLS))
        par_duration = time.time() - start_par
        print(
            f"Parallel duration for {len(MOCK_URLS)} leads: {par_duration:.3f} seconds"
        )

        # Verify correctness
        self.assertEqual(len(par_leads), len(seq_leads))
        # Verify result order is preserved
        for idx, lead in enumerate(par_leads):
            self.assertEqual(lead["url"], MOCK_URLS[idx])
            self.assertEqual(lead["email"], "info@example.com")
            self.assertEqual(lead["title"], f"Business {MOCK_URLS[idx]}")

        # Parallel should be significantly faster than sequential.
        # Sequential: 5 * (0.5s + 1.0s) = 7.5 seconds
        # Parallel: max 0.5s + small overhead
        speedup = seq_duration / par_duration
        print(f"Speedup factor: {speedup:.1f}x faster!")

        self.assertGreater(
            speedup,
            2.0,
            f"Parallel execution is not fast enough compared to sequential (Speedup was {speedup:.1f}x)",
        )


if __name__ == "__main__":
    unittest.main()
