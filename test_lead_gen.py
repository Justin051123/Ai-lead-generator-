import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.get_thread_session")
    def test_extract_info_success(self, mock_get_session):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Business</title></head><body>Contact us at contact@testbiz.com</body></html>"
        mock_session.get.return_value = mock_response
        mock_get_session.return_value = mock_session

        info = lead_gen.extract_info("https://testbiz.com")
        self.assertEqual(info["url"], "https://testbiz.com")
        self.assertEqual(info["title"], "Test Business")
        self.assertEqual(info["email"], "contact@testbiz.com")

    def test_qualify_lead(self):
        lead_info = {"url": "https://test.com", "title": "A Very Long Business Title", "email": "info@test.com"}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ["https://site1.com", "https://site2.com"]
        mock_extract.side_effect = lambda url: {"url": url, "email": f"info@{url.split('//')[1]}", "title": f"Title for {url}"}

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[1]["url"], "https://site2.com")

if __name__ == "__main__":
    unittest.main()
