import time
import unittest
from unittest.mock import MagicMock, patch


# Import the code to test/benchmark
from lead_gen import extract_info, generate_leads, qualify_lead


class TestPerformanceAndCorrectness(unittest.TestCase):

    @patch('lead_gen.search')
    @patch('lead_gen.requests.get')
    def test_benchmark_and_correctness(self, mock_get, mock_search):
        # 1. Setup mock search results
        mock_urls = [
            "https://test-roofer-1.com",
            "https://test-roofer-2.com",
            "https://test-roofer-3.com",
            "https://test-roofer-4.com",
            "https://test-roofer-5.com"
        ]
        mock_search.return_value = mock_urls

        # 2. Setup mock responses with realistic delays to simulate real HTTP request latency (e.g. 100ms per request)
        def mock_requests_get(url, *args, **kwargs):
            mock_resp = MagicMock()
            mock_resp.status_code = 200

            # Simulate network latency of 100ms
            time.sleep(0.1)

            if "1" in url:
                mock_resp.text = "<html><title>Roofers of Miami #1</title><body>Contact us at contact@miamiroof1.com today!</body></html>"
            elif "2" in url:
                mock_resp.text = "<html><title>Roofers of Miami #2</title><body>Our support is support@miamiroof2.org</body></html>"
            elif "3" in url:
                mock_resp.text = "<html><title>Roofers of Miami #3</title><body>No emails here!</body></html>"
            elif "4" in url:
                mock_resp.text = "<html><title>Roofers of Miami #4</title><body>Reach info@miamiroof4.com for queries.</body></html>"
            else:
                mock_resp.text = "<html><title>Roofers of Miami #5</title><body>Email us: team@miamiroof5.co.uk</body></html>"

            return mock_resp

        mock_get.side_effect = mock_requests_get

        # 3. Time sequential execution manually (simulated by processing leads one by one and waiting 1s polite sleep like previous logic)
        def simulated_sequential_generate_leads():
            leads = []
            for url in mock_urls:
                # Mock sequential logic: extract info (with its 0.1s network mock latency) + 1.0s polite delay
                info = extract_info(url)
                leads.append(qualify_lead(info))
                time.sleep(1.0) # The polite delay that was previously there
            return leads

        print("\n--- Running Simulated Sequential Run ---")
        start_seq = time.perf_counter()
        simulated_sequential_generate_leads()
        end_seq = time.perf_counter()
        seq_time = end_seq - start_seq
        print(f"Sequential lead processing time: {seq_time:.4f} seconds")

        # 4. Time the parallel optimized execution
        print("\n--- Running Optimized Parallel Run ---")
        start_par = time.perf_counter()
        par_leads = generate_leads("Roofers", "Miami", num_results=5)
        end_par = time.perf_counter()
        par_time = end_par - start_par
        print(f"Parallelized lead processing time: {par_time:.4f} seconds")

        # Calculate performance speedup
        speedup = seq_time / par_time
        print(f"⚡ Performance Speedup: {speedup:.2f}x faster! (Sequential: {seq_time:.2f}s vs Parallel: {par_time:.2f}s)")

        # 5. Assertions to ensure correctness and no regressions
        self.assertEqual(len(par_leads), 5)
        self.assertEqual(par_leads[0]["title"], "Roofers of Miami #1")
        self.assertEqual(par_leads[0]["email"], "contact@miamiroof1.com")
        self.assertEqual(par_leads[0]["ai_score"], 70)
        self.assertEqual(par_leads[0]["qualification"], "High")

        self.assertEqual(par_leads[2]["email"], "N/A")
        self.assertEqual(par_leads[2]["qualification"], "Medium") # score = 20 (title > 10)

        # Ensure our optimization made it significantly faster
        # In a simulated environment, sequential wait takes (0.1s latency + 1s polite sleep) * 5 = ~5.5 seconds.
        # Parallel run has 5 parallel threads doing 100ms network requests simultaneously with NO polite sleep. Total is ~100-200ms (~0.1-0.2 seconds).
        # Speedup should be > 10x!
        self.assertGreater(speedup, 5.0, "Parallel execution should be at least 5x faster than sequential execution in simulation.")

if __name__ == "__main__":
    unittest.main()
