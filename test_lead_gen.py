import unittest
from unittest.mock import patch, MagicMock
from lead_gen import search_businesses, extract_info, qualify_lead, generate_leads

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example.com", "https://test.com"]
        urls = search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(urls, ["https://example.com", "https://test.com"])
        mock_search.assert_called_once_with("Plumbers in London", num_results=2)

    @patch("lead_gen.requests.get")
    def test_extract_info(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Business</title></head><body>Contact us at contact@testbusiness.com</body></html>"
        mock_get.return_value = mock_response

        info = extract_info("https://testbusiness.com")
        self.assertEqual(info["url"], "https://testbusiness.com")
        self.assertEqual(info["title"], "Test Business")
        self.assertEqual(info["email"], "contact@testbusiness.com")

    def test_qualify_lead(self):
        lead_info = {"url": "https://example.com", "title": "A Very Long Title For Business", "email": "info@example.com"}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch("lead_gen.time.sleep")
    @patch("lead_gen.extract_info")
    @patch("lead_gen.search_businesses")
    def test_generate_leads(self, mock_search, mock_extract, mock_sleep):
        mock_search.return_value = ["https://example.com"]
        mock_extract.return_value = {"url": "https://example.com", "title": "Example", "email": "info@example.com"}

        leads = generate_leads("Plumbers", "London", num_results=1)
        self.assertEqual(len(leads), 1)
        self.assertEqual(leads[0]["email"], "info@example.com")
        self.assertEqual(leads[0]["qualification"], "Medium") # score = 50 -> Medium

if __name__ == "__main__":
    unittest.main()
