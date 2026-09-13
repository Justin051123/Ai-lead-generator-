import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.search')
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        urls = lead_gen.search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(urls, ["https://example1.com", "https://example2.com"])
        mock_search.assert_called_once_with("Plumbers in London", num_results=2)

    @patch('lead_gen.requests.get')
    def test_extract_info(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Best Plumbers</title></head><body>Contact us at info@plumbers.com</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Best Plumbers")
        self.assertEqual(info["email"], "info@plumbers.com")

    def test_qualify_lead(self):
        lead_info = {"title": "Best Plumbers in London", "email": "contact@plumbers.com"}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch('lead_gen.extract_info')
    @patch('lead_gen.search_businesses')
    def test_generate_leads(self, mock_search, mock_extract):
        mock_search.return_value = ["https://site1.com", "https://site2.com"]
        mock_extract.side_effect = [
            {"url": "https://site1.com", "email": "a@site1.com", "title": "Site One Title"},
            {"url": "https://site2.com", "email": "N/A", "title": "Site Two Title"}
        ]

        leads = lead_gen.generate_leads("Roofers", "Miami", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[0]["email"], "a@site1.com")
        self.assertEqual(leads[1]["url"], "https://site2.com")
        self.assertEqual(leads[1]["email"], "N/A")

if __name__ == "__main__":
    unittest.main()
