import unittest
from unittest.mock import patch, MagicMock
import time

import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch('requests.get')
    def test_extract_info_success(self, mock_get):
        # Setup mock response
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = "<html><title>   Best Plumber London   </title><body>Reach us at info@londonplumbers.co.uk or ignore@test.png</body></html>"
        mock_get.return_value = mock_resp

        # Call extract_info
        info = lead_gen.extract_info("http://londonplumbers.co.uk")

        # Verify output
        self.assertEqual(info["url"], "http://londonplumbers.co.uk")
        self.assertEqual(info["title"], "Best Plumber London")
        self.assertEqual(info["email"], "info@londonplumbers.co.uk")

    @patch('requests.get')
    def test_extract_info_no_email_or_title(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.text = "Not Found"
        mock_get.return_value = mock_resp

        info = lead_gen.extract_info("http://badurl.com")
        self.assertEqual(info["url"], "http://badurl.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead(self):
        lead_info_high = {"url": "http://test.com", "title": "Super long title indeed", "email": "info@test.com"}
        qualified_high = lead_gen.qualify_lead(lead_info_high)
        self.assertEqual(qualified_high["ai_score"], 70)
        self.assertEqual(qualified_high["qualification"], "High")

        lead_info_medium = {"url": "http://test.com", "title": "Short", "email": "info@test.com"}
        qualified_medium = lead_gen.qualify_lead(lead_info_medium)
        self.assertEqual(qualified_medium["ai_score"], 50)
        self.assertEqual(qualified_medium["qualification"], "Medium")

        lead_info_low = {"url": "http://test.com", "title": "Short", "email": "N/A"}
        qualified_low = lead_gen.qualify_lead(lead_info_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch('lead_gen.search_businesses')
    @patch('requests.get')
    def test_generate_leads_benchmark(self, mock_get, mock_search):
        # We will mock search_businesses to return 5 fake urls
        urls = [f"http://site{i}.com" for i in range(5)]
        mock_search.return_value = urls

        # Mock requests.get with a simulated network delay
        def mock_get_impl(url, *args, **kwargs):
            time.sleep(0.1) # 100ms simulated network delay
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.text = f"<html><title>Site {url}</title><body>contact@{url.split('//')[1]}</body></html>"
            return mock_resp

        mock_get.side_effect = mock_get_impl

        # Run generate_leads and measure elapsed time
        start_time = time.perf_counter()
        leads = lead_gen.generate_leads("Plumbers", "London", num_results=5)
        end_time = time.perf_counter()

        elapsed = end_time - start_time
        print(f"\n[BENCHMARK] Processing 5 leads took {elapsed:.4f} seconds.")
        print(f"[BENCHMARK] Found leads: {leads}")

        # Check correctness of result
        self.assertEqual(len(leads), 5)
        self.assertEqual(leads[0]["url"], "http://site0.com")
        self.assertEqual(leads[0]["email"], "contact@site0.com")

        # Let's assert something about execution time to guarantee performance.
        # Once optimized, 5 requests with 0.1s simulated network delay should take around 0.1s-0.3s.
        # But in sequential mode, it takes 5 * 0.1s network latency + 5 * 1.0s politeness delay = ~5.5 seconds.
        # We can print sequential vs parallel expectation in the benchmark.

if __name__ == "__main__":
    unittest.main()
