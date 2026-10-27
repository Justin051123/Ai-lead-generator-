import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    def test_qualify_lead(self):
        lead_info = {"url": "https://example.com", "email": "info@example.com", "title": "Example Business Title"}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

        lead_info_low = {"url": "https://example.com", "email": "N/A", "title": "Short"}
        qualified_low = lead_gen.qualify_lead(lead_info_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch("requests.get")
    def test_extract_info(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title> Best Plumbing Co </title></head><body>Contact us at contact@plumbing.com</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://plumbing.com")
        self.assertEqual(info["url"], "https://plumbing.com")
        self.assertEqual(info["title"], "Best Plumbing Co")
        self.assertEqual(info["email"], "contact@plumbing.com")

    @patch("lead_gen.search_businesses")
    @patch("requests.get")
    def test_generate_leads_parallel_order(self, mock_get, mock_search):
        urls = [f"https://example{i}.com" for i in range(5)]
        mock_search.return_value = urls

        def side_effect(url, timeout=10, headers=None):
            mock_res = MagicMock()
            mock_res.status_code = 200
            idx = url.replace("https://example", "").replace(".com", "")
            mock_res.text = f"<html><head><title>Company {idx}</title></head><body>info{idx}@example.com</body></html>"
            return mock_res

        mock_get.side_effect = side_effect

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=5)
        self.assertEqual(len(leads), 5)
        # Confirm that search result ordering is preserved
        for idx, lead in enumerate(leads):
            self.assertEqual(lead["url"], f"https://example{idx}.com")
            self.assertEqual(lead["email"], f"info{idx}@example.com")
            self.assertEqual(lead["title"], f"Company {idx}")

if __name__ == "__main__":
    unittest.main()
