import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <head><title>Best Plumber in Town</title></head>
            <body>
                <p>Contact us at info@example.com or support@example.com</p>
                <img src="logo.png" />
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Best Plumber in Town")
        self.assertIn("@example.com", info["email"])
        self.assertFalse(info["email"].endswith(".png"))

    @patch("lead_gen.requests.get")
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection error")

        info = lead_gen.extract_info("https://broken-site.com")
        self.assertEqual(info["url"], "https://broken-site.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead(self):
        high_lead = {"url": "https://a.com", "title": "A Very Detailed Business Title", "email": "contact@a.com"}
        qualified_high = lead_gen.qualify_lead(high_lead)
        self.assertEqual(qualified_high["ai_score"], 70)
        self.assertEqual(qualified_high["qualification"], "High")

        low_lead = {"url": "https://b.com", "title": "", "email": "N/A"}
        qualified_low = lead_gen.qualify_lead(low_lead)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://site1.com", "https://site2.com"]
        urls = lead_gen.search_businesses("Plumber Miami", num_results=2)
        self.assertEqual(urls, ["https://site1.com", "https://site2.com"])

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ["https://site1.com", "https://site2.com"]
        mock_extract.side_effect = [
            {"url": "https://site1.com", "title": "Site 1 Title Long Enough", "email": "info@site1.com"},
            {"url": "https://site2.com", "title": "Short", "email": "N/A"},
        ]

        leads = lead_gen.generate_leads("Plumber", "Miami", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[0]["qualification"], "High")
        self.assertEqual(leads[1]["url"], "https://site2.com")
        self.assertEqual(leads[1]["qualification"], "Low")

if __name__ == "__main__":
    unittest.main()
