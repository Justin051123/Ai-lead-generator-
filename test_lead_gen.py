import unittest
from unittest.mock import patch, MagicMock
from lead_gen import search_businesses, extract_info, qualify_lead, generate_leads


class TestLeadGen(unittest.TestCase):
    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        urls = search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(urls, ["https://example1.com", "https://example2.com"])
        mock_search.assert_called_once_with("Plumbers in London", num_results=2)

    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <head><title>Best Plumbing Services</title></head>
            <body>
                <p>Contact us at info@example.com or support@example.com</p>
                <img src="icon@2x.png" />
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        info = extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Best Plumbing Services")
        self.assertIn(info["email"], ["info@example.com", "support@example.com"])

    @patch("lead_gen.requests.get")
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        info = extract_info("https://broken.com")
        self.assertEqual(info["url"], "https://broken.com")
        self.assertEqual(info["email"], "N/A")
        self.assertEqual(info["title"], "N/A")

    def test_qualify_lead(self):
        lead_high = {"url": "https://example.com", "email": "a@b.com", "title": "A Very Long Business Title"}
        qualified_high = qualify_lead(lead_high)
        self.assertEqual(qualified_high["ai_score"], 70)
        self.assertEqual(qualified_high["qualification"], "High")

        lead_medium = {"url": "https://example.com", "email": "N/A", "title": "A Very Long Business Title"}
        qualified_medium = qualify_lead(lead_medium)
        self.assertEqual(qualified_medium["ai_score"], 20)
        self.assertEqual(qualified_medium["qualification"], "Medium")

        lead_low = {"url": "https://example.com", "email": "N/A", "title": "Short"}
        qualified_low = qualify_lead(lead_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch("lead_gen.extract_info")
    @patch("lead_gen.search_businesses")
    def test_generate_leads(self, mock_search, mock_extract):
        mock_search.return_value = ["https://a.com", "https://b.com"]
        mock_extract.side_effect = [
            {"url": "https://a.com", "email": "a@a.com", "title": "Business Alpha Long Title"},
            {"url": "https://b.com", "email": "N/A", "title": "Business Beta Long Title"},
        ]

        leads = generate_leads("Roofers", "Miami", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://a.com")
        self.assertEqual(leads[0]["qualification"], "High")
        self.assertEqual(leads[1]["url"], "https://b.com")
        self.assertEqual(leads[1]["qualification"], "Medium")


if __name__ == "__main__":
    unittest.main()
