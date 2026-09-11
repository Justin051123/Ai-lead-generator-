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

    @patch('lead_gen.search')
    def test_search_businesses_exception(self, mock_search):
        mock_search.side_effect = Exception("Search error")
        urls = lead_gen.search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(urls, [])

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
            <html>
                <head><title> Best Plumber </title></head>
                <body>
                    <p>Contact us at contact@plumber.com or info@plumber.com</p>
                    <img src="logo.png" />
                </body>
            </html>
        """
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Best Plumber")
        self.assertIn(info["email"], ["contact@plumber.com", "info@plumber.com"])

    @patch('lead_gen.requests.get')
    def test_extract_info_exception(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        info = lead_gen.extract_info("https://example.com")
        self.assertEqual(info, {"url": "https://example.com", "email": "N/A", "title": "N/A"})

    def test_qualify_lead(self):
        lead_high = {"url": "https://example.com", "email": "info@example.com", "title": "A Great Plumbing Service"}
        qualified_high = lead_gen.qualify_lead(lead_high)
        self.assertEqual(qualified_high["ai_score"], 70)
        self.assertEqual(qualified_high["qualification"], "High")

        lead_low = {"url": "https://example.com", "email": "N/A", "title": "Short"}
        qualified_low = lead_gen.qualify_lead(lead_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads(self, mock_extract_info, mock_search):
        mock_search.return_value = ["https://site1.com", "https://site2.com"]
        mock_extract_info.side_effect = [
            {"url": "https://site1.com", "email": "a@site1.com", "title": "Site 1 Title Example"},
            {"url": "https://site2.com", "email": "N/A", "title": "Short"}
        ]

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[0]["ai_score"], 70)
        self.assertEqual(leads[1]["url"], "https://site2.com")
        self.assertEqual(leads[1]["ai_score"], 0)

if __name__ == "__main__":
    unittest.main()
