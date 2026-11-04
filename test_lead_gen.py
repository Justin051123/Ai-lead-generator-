import unittest
from unittest.mock import patch, MagicMock
from lead_gen import search_businesses, extract_info, qualify_lead, generate_leads


class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        urls = search_businesses("Plumbers Miami", num_results=2)
        self.assertEqual(urls, ["https://example1.com", "https://example2.com"])
        mock_search.assert_called_once_with("Plumbers Miami", num_results=2)

    @patch("lead_gen.search", side_effect=Exception("API Error"))
    def test_search_businesses_handles_error(self, mock_search):
        urls = search_businesses("Plumbers Miami", num_results=2)
        self.assertEqual(urls, [])

    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <head><title>Best Plumber Miami</title></head>
            <body>
                <p>Contact us: support@bestplumber.com or icon.png</p>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        info = extract_info("https://bestplumber.com")
        self.assertEqual(info["url"], "https://bestplumber.com")
        self.assertEqual(info["title"], "Best Plumber Miami")
        self.assertEqual(info["email"], "support@bestplumber.com")

    @patch("lead_gen.requests.get")
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection timeout")
        info = extract_info("https://badurl.com")
        self.assertEqual(info["url"], "https://badurl.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead_high(self):
        lead = {"url": "https://example.com", "title": "Example Business Title", "email": "info@example.com"}
        qualified = qualify_lead(lead)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    def test_qualify_lead_medium(self):
        lead = {"url": "https://example.com", "title": "Example Business Title", "email": "N/A"}
        qualified = qualify_lead(lead)
        self.assertEqual(qualified["ai_score"], 20)
        self.assertEqual(qualified["qualification"], "Medium")

    def test_qualify_lead_low(self):
        lead = {"url": "https://example.com", "title": "Short", "email": "N/A"}
        qualified = qualify_lead(lead)
        self.assertEqual(qualified["ai_score"], 0)
        self.assertEqual(qualified["qualification"], "Low")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ["https://site1.com", "https://site2.com"]
        mock_extract.side_effect = [
            {"url": "https://site1.com", "title": "Site One Business", "email": "one@site.com"},
            {"url": "https://site2.com", "title": "Site Two", "email": "N/A"},
        ]

        leads = generate_leads("Dentists", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[0]["qualification"], "High")
        self.assertEqual(leads[1]["url"], "https://site2.com")
        self.assertEqual(leads[1]["qualification"], "Low")


if __name__ == "__main__":
    unittest.main()
