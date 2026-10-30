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
        mock_response.text = "<html><head><title>Best Plumber</title></head><body>Email: contact@plumber.com</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Best Plumber")
        self.assertEqual(info["email"], "contact@plumber.com")

    @patch("lead_gen.requests.get")
    def test_extract_info_image_email_filtered(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Best Plumber</title></head><body><img src='logo@2x.png'/>Email: info@plumber.com</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://example.com")
        self.assertEqual(info["email"], "info@plumber.com")

    def test_qualify_lead(self):
        lead_info = {"url": "https://example.com", "email": "contact@plumber.com", "title": "Best Plumber"}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        mock_extract.side_effect = [
            {"url": "https://example1.com", "email": "a@ex1.com", "title": "Company One Title"},
            {"url": "https://example2.com", "email": "N/A", "title": "Company Two Title"}
        ]

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://example1.com")
        self.assertEqual(leads[0]["qualification"], "High")
        self.assertEqual(leads[1]["url"], "https://example2.com")
        self.assertEqual(leads[1]["qualification"], "Medium")

if __name__ == "__main__":
    unittest.main()
