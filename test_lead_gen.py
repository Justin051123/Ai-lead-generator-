import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        urls = lead_gen.search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(urls, ["https://example1.com", "https://example2.com"])
        mock_search.assert_called_once_with("Plumbers in London", num_results=2)

    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Best Plumbers</title></head><body>Contact us at info@bestplumbers.com or logo.png</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://bestplumbers.com")
        self.assertEqual(info["url"], "https://bestplumbers.com")
        self.assertEqual(info["title"], "Best Plumbers")
        self.assertEqual(info["email"], "info@bestplumbers.com")

    @patch("lead_gen.requests.get")
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        info = lead_gen.extract_info("https://badurl.com")
        self.assertEqual(info["url"], "https://badurl.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead(self):
        lead_info_high = {"url": "https://a.com", "email": "a@a.com", "title": "Long Title Business"}
        qualified_high = lead_gen.qualify_lead(lead_info_high)
        self.assertEqual(qualified_high["ai_score"], 70)
        self.assertEqual(qualified_high["qualification"], "High")

        lead_info_low = {"url": "https://b.com", "email": "N/A", "title": "Short"}
        qualified_low = lead_gen.qualify_lead(lead_info_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch("lead_gen.extract_info")
    @patch("lead_gen.search_businesses")
    def test_generate_leads(self, mock_search_businesses, mock_extract_info):
        mock_search_businesses.return_value = ["https://site1.com", "https://site2.com"]
        mock_extract_info.side_effect = [
            {"url": "https://site1.com", "email": "s1@site1.com", "title": "Site One Title"},
            {"url": "https://site2.com", "email": "N/A", "title": "Site Two Title"},
        ]

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[0]["email"], "s1@site1.com")
        self.assertEqual(leads[1]["url"], "https://site2.com")

if __name__ == "__main__":
    unittest.main()
