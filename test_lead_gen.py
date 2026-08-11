import unittest
from unittest.mock import patch, MagicMock
import time
from lead_gen import extract_info, qualify_lead, generate_leads

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        # Mock a successful response with standard title and email
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Plumber</title></head><body>Contact us at info@testplumber.com</body></html>"
        mock_get.return_value = mock_response

        info = extract_info("http://testplumber.com")
        self.assertEqual(info["url"], "http://testplumber.com")
        self.assertEqual(info["title"], "Test Plumber")
        self.assertEqual(info["email"], "info@testplumber.com")

    @patch('lead_gen.requests.get')
    def test_extract_info_failure(self, mock_get):
        # Mock a failed request or exception
        mock_get.side_effect = Exception("Connection error")

        info = extract_info("http://badlink.com")
        self.assertEqual(info["url"], "http://badlink.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead(self):
        # Lead with email and long title should qualify high
        lead_high = {"url": "http://x.com", "title": "Super Awesome Plumbers", "email": "info@x.com"}
        qualified_high = qualify_lead(lead_high)
        self.assertEqual(qualified_high["qualification"], "High")
        self.assertEqual(qualified_high["ai_score"], 70)

        # Lead with no email and short title should qualify low
        lead_low = {"url": "http://y.com", "title": "Short", "email": "N/A"}
        qualified_low = qualify_lead(lead_low)
        self.assertEqual(qualified_low["qualification"], "Low")
        self.assertEqual(qualified_low["ai_score"], 0)

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.requests.get')
    def test_generate_leads_parallel_speedup_and_correctness(self, mock_get, mock_search):
        # We search for 5 leads.
        urls = [f"http://site{i}.com" for i in range(5)]
        mock_search.return_value = urls

        # Simulate network latency of 1 second per requests.get call
        def mock_get_impl(url, *args, **kwargs):
            time.sleep(1.0)
            mock_res = MagicMock()
            mock_res.status_code = 200
            mock_res.text = f"<html><head><title>Site {url}</title></head><body>contact@site.com</body></html>"
            return mock_res

        mock_get.side_effect = mock_get_impl

        # Measure performance
        start_time = time.time()
        leads = generate_leads("Plumbers", "London", num_results=5)
        duration = time.time() - start_time

        # If it were sequential with 5 leads and 1.0s latency per lead, it would take ~5.0s.
        # With thread pool parallelization (max_workers=5), it should complete in much less time (e.g. < 2.0s).
        print(f"\n[Benchmark] Parallel processing of 5 leads completed in {duration:.4f} seconds.")
        self.assertTrue(duration < 2.5, f"Parallel execution took too long: {duration}s")
        self.assertEqual(len(leads), 5)

        # Verify the order is preserved
        for i, lead in enumerate(leads):
            self.assertEqual(lead["url"], urls[i])

if __name__ == '__main__':
    unittest.main()
