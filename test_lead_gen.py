import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        urls = lead_gen.search_businesses("Plumbers London", num_results=2)
        self.assertEqual(urls, ["https://example1.com", "https://example2.com"])
        mock_search.assert_called_once_with("Plumbers London", num_results=2)

    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Plumber</title></head><body>Contact us at contact@testplumber.com</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://example1.com")
        self.assertEqual(info["url"], "https://example1.com")
        self.assertEqual(info["title"], "Test Plumber")
        self.assertEqual(info["email"], "contact@testplumber.com")

    def test_qualify_lead(self):
        lead_info = {"url": "https://example.com", "email": "contact@example.com", "title": "A Great Business Name"}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads(self, mock_extract_info, mock_search_businesses):
        mock_search_businesses.return_value = ["https://site1.com", "https://site2.com"]
        mock_extract_info.side_effect = [
            {"url": "https://site1.com", "email": "info@site1.com", "title": "Site 1 Title"},
            {"url": "https://site2.com", "email": "N/A", "title": "Site 2 Title"}
        ]

        leads = lead_gen.generate_leads("Dentists", "NY", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[0]["email"], "info@site1.com")
        self.assertEqual(leads[1]["url"], "https://site2.com")
        self.assertEqual(leads[1]["email"], "N/A")

if __name__ == "__main__":
    unittest.main()
