import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.search')
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        urls = lead_gen.search_businesses("plumbers in london", num_results=2)
        self.assertEqual(urls, ["https://example1.com", "https://example2.com"])

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test Business</title></head><body>Contact us at contact@testbusiness.com</body></html>'
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Test Business")
        self.assertEqual(info["email"], "contact@testbusiness.com")

    def test_qualify_lead(self):
        info = {"url": "https://example.com", "email": "contact@testbusiness.com", "title": "A Very Long Business Title"}
        qualified = lead_gen.qualify_lead(info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch('lead_gen.extract_info')
    @patch('lead_gen.search_businesses')
    def test_generate_leads(self, mock_search, mock_extract):
        mock_search.return_value = ["https://site1.com", "https://site2.com"]
        mock_extract.side_effect = lambda url: {
            "url": url,
            "title": f"Title for {url}",
            "email": "info@test.com"
        }

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[1]["url"], "https://site2.com")
        self.assertIn("ai_score", leads[0])
        self.assertIn("qualification", leads[0])

if __name__ == "__main__":
    unittest.main()
