import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        urls = lead_gen.search_businesses("Roofers Miami", num_results=2)
        self.assertEqual(urls, ["https://example1.com", "https://example2.com"])
        mock_search.assert_called_once_with("Roofers Miami", num_results=2)

    @patch("lead_gen.search", side_effect=Exception("Network error"))
    def test_search_businesses_exception(self, mock_search):
        urls = lead_gen.search_businesses("Roofers Miami")
        self.assertEqual(urls, [])

    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = """
        <html>
            <head><title> Best Roofing Co </title></head>
            <body>
                <p>Contact us at contact@bestroofing.com or image@domain.png</p>
            </body>
        </html>
        """
        mock_get.return_value = mock_resp

        info = lead_gen.extract_info("https://bestroofing.com")
        self.assertEqual(info["url"], "https://bestroofing.com")
        self.assertEqual(info["title"], "Best Roofing Co")
        self.assertEqual(info["email"], "contact@bestroofing.com")

    @patch("lead_gen.requests.get", side_effect=Exception("Timeout"))
    def test_extract_info_failure(self, mock_get):
        info = lead_gen.extract_info("https://timeout.com")
        self.assertEqual(info["url"], "https://timeout.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead(self):
        lead_high = {"email": "hello@roofing.com", "title": "Roofing Experts Miami"}
        qualified_high = lead_gen.qualify_lead(lead_high)
        self.assertEqual(qualified_high["ai_score"], 70)
        self.assertEqual(qualified_high["qualification"], "High")

        lead_medium = {"email": "N/A", "title": "Roofing Experts Miami"}
        qualified_medium = lead_gen.qualify_lead(lead_medium)
        self.assertEqual(qualified_medium["ai_score"], 20)
        self.assertEqual(qualified_medium["qualification"], "Medium")

        lead_low = {"email": "N/A", "title": "Roof"}
        qualified_low = lead_gen.qualify_lead(lead_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ["https://site1.com", "https://site2.com"]
        mock_extract.side_effect = [
            {"url": "https://site1.com", "email": "info@site1.com", "title": "Site 1 Title Extra Long"},
            {"url": "https://site2.com", "email": "N/A", "title": "Site"},
        ]

        leads = lead_gen.generate_leads("Roofers", "Miami", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[0]["qualification"], "High")
        self.assertEqual(leads[1]["url"], "https://site2.com")
        self.assertEqual(leads[1]["qualification"], "Low")

if __name__ == "__main__":
    unittest.main()
