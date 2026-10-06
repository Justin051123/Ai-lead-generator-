import time
import unittest
from unittest.mock import MagicMock, patch

import lead_gen


class TestLeadGen(unittest.TestCase):

    def test_qualify_lead(self):
        lead_with_email = {"url": "http://example.com", "email": "test@example.com", "title": "Example Business Title"}
        qualified = lead_gen.qualify_lead(lead_with_email)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

        lead_no_email = {"url": "http://example.com", "email": "N/A", "title": "Short"}
        qualified_no_email = lead_gen.qualify_lead(lead_no_email)
        self.assertEqual(qualified_no_email["ai_score"], 0)
        self.assertEqual(qualified_no_email["qualification"], "Low")

    @patch("lead_gen.get_thread_session")
    def test_extract_info(self, mock_get_session):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Business</title></head><body>Contact us at info@testbusiness.com</body></html>"
        mock_session.get.return_value = mock_response
        mock_get_session.return_value = mock_session

        info = lead_gen.extract_info("http://testbusiness.com")
        self.assertEqual(info["url"], "http://testbusiness.com")
        self.assertEqual(info["title"], "Test Business")
        self.assertEqual(info["email"], "info@testbusiness.com")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads_order_and_concurrency(self, mock_extract, mock_search):
        urls = [f"http://example{i}.com" for i in range(5)]
        mock_search.return_value = urls

        def mock_extract_side_effect(url):
            time.sleep(0.05)  # Simulate small network delay
            return {"url": url, "email": f"contact@{url.split('//')[1]}", "title": f"Title for {url}"}

        mock_extract.side_effect = mock_extract_side_effect

        start_time = time.perf_counter()
        leads = lead_gen.generate_leads("Plumbers", "London", num_results=5, max_workers=5)
        elapsed_time = time.perf_counter() - start_time

        # Verify results count and ordering
        self.assertEqual(len(leads), 5)
        for idx, url in enumerate(urls):
            self.assertEqual(leads[idx]["url"], url)

        # 5 tasks with 0.05s delay sequentially take 0.25s+. Concurrently with 5 workers it should take ~0.05s - 0.15s.
        print(f"\n[Benchmark] Processed 5 mock leads in parallel in {elapsed_time:.4f} seconds.")
        self.assertLess(elapsed_time, 0.20)


if __name__ == "__main__":
    unittest.main()
