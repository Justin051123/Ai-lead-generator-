import time
import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):
    @patch('lead_gen.requests.get')
    def test_extract_info(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test Business</title></head><body>Contact us at info@example.com and test@domain.org</body></html>'
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("http://example.com")
        self.assertEqual(info["title"], "Test Business")
        self.assertIn(info["email"], ["info@example.com", "test@domain.org"])

    def test_qualify_lead(self):
        lead_info = {"title": "Test Business Name", "email": "info@example.com"}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads_parallel_and_ordering(self, mock_extract, mock_search):
        mock_search.return_value = [
            "http://example1.com",
            "http://example2.com",
            "http://example3.com"
        ]

        def mock_extract_side_effect(url):
            if "example1" in url:
                time.sleep(0.05)
                return {"url": url, "email": "a@ex.com", "title": "Title 1"}
            elif "example2" in url:
                time.sleep(0.01)
                return {"url": url, "email": "b@ex.com", "title": "Title 2"}
            else:
                return {"url": url, "email": "c@ex.com", "title": "Title 3"}

        mock_extract.side_effect = mock_extract_side_effect

        start_time = time.time()
        leads = lead_gen.generate_leads("Plumbers", "London", num_results=3, max_workers=3)
        duration = time.time() - start_time

        self.assertEqual(len(leads), 3)
        # Verify search result order is preserved despite varying execution times
        self.assertEqual(leads[0]["url"], "http://example1.com")
        self.assertEqual(leads[1]["url"], "http://example2.com")
        self.assertEqual(leads[2]["url"], "http://example3.com")
        # Ensure total duration is close to max worker delay (~0.05s) rather than cumulative (~0.06s + overhead)
        self.assertLess(duration, 0.15)

if __name__ == '__main__':
    unittest.main()
