import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch("requests.get")
    def test_extract_info(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Business</title></head><body>Email contact@testbiz.com</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://testbiz.com")
        self.assertEqual(info["url"], "https://testbiz.com")
        self.assertEqual(info["title"], "Test Business")
        self.assertEqual(info["email"], "contact@testbiz.com")

    def test_qualify_lead(self):
        lead = {"url": "https://testbiz.com", "title": "Test Business Title", "email": "contact@testbiz.com"}
        qualified = lead_gen.qualify_lead(lead)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ["https://site1.com", "https://site2.com"]
        mock_extract.side_effect = lambda url, session=None: {"url": url, "email": f"info@{url.split('//')[1]}", "title": "Some Title"}

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[1]["url"], "https://site2.com")

if __name__ == "__main__":
    unittest.main()
