import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    def test_qualify_lead_high(self):
        lead_info = {
            "url": "http://example.com",
            "email": "contact@example.com",
            "title": "Example Business Title"
        }
        result = lead_gen.qualify_lead(lead_info)
        self.assertEqual(result["ai_score"], 70)
        self.assertEqual(result["qualification"], "High")

    def test_qualify_lead_low(self):
        lead_info = {
            "url": "http://example.com",
            "email": "N/A",
            "title": "Short"
        }
        result = lead_gen.qualify_lead(lead_info)
        self.assertEqual(result["ai_score"], 0)
        self.assertEqual(result["qualification"], "Low")

    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Business - Best Services</title></head><body>Contact us at info@testbusiness.com</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("http://testbusiness.com")
        self.assertEqual(info["title"], "Test Business - Best Services")
        self.assertEqual(info["email"], "info@testbusiness.com")

    @patch("lead_gen.requests.get")
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        info = lead_gen.extract_info("http://invalidurl.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads_parallel(self, mock_extract, mock_search):
        mock_search.return_value = ["http://biz1.com", "http://biz2.com"]
        mock_extract.side_effect = lambda url: {
            "url": url,
            "email": "contact@" + url.split("//")[1],
            "title": "Business Title for " + url
        }

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "http://biz1.com")
        self.assertEqual(leads[1]["url"], "http://biz2.com")
        self.assertEqual(leads[0]["email"], "contact@biz1.com")
        self.assertEqual(leads[1]["email"], "contact@biz2.com")

if __name__ == "__main__":
    unittest.main()
