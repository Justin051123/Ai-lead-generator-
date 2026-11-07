import unittest
from unittest.mock import patch, MagicMock
import lead_gen


class TestLeadGen(unittest.TestCase):
    def test_qualify_lead(self):
        lead = {"url": "https://example.com", "email": "test@example.com", "title": "Example Business Title"}
        qualified = lead_gen.qualify_lead(lead)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

        lead_low = {"url": "https://example.com", "email": "N/A", "title": "N/A"}
        qualified_low = lead_gen.qualify_lead(lead_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <head><title>Best Plumbing Services</title></head>
            <body>
                <p>Contact us at info@bestplumbing.com or support@bestplumbing.com</p>
                <img src="logo.png@2x.png" />
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://bestplumbing.com")
        self.assertEqual(info["url"], "https://bestplumbing.com")
        self.assertEqual(info["title"], "Best Plumbing Services")
        self.assertIn("@bestplumbing.com", info["email"])

    @patch("lead_gen.requests.get")
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        info = lead_gen.extract_info("https://invalid-url.fake")
        self.assertEqual(info["url"], "https://invalid-url.fake")
        self.assertEqual(info["email"], "N/A")
        self.assertEqual(info["title"], "N/A")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.requests.get")
    def test_generate_leads(self, mock_get, mock_search):
        mock_search.return_value = [
            "https://lead1.com",
            "https://lead2.com",
            "https://lead3.com",
        ]

        def fake_get(url, *args, **kwargs):
            resp = MagicMock()
            resp.status_code = 200
            name = url.replace("https://", "").replace(".com", "")
            resp.text = f"<html><head><title>{name.capitalize()} Home</title></head><body>contact@{name}.com</body></html>"
            return resp

        mock_get.side_effect = fake_get

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=3)
        self.assertEqual(len(leads), 3)
        self.assertEqual(leads[0]["url"], "https://lead1.com")
        self.assertEqual(leads[0]["email"], "contact@lead1.com")
        self.assertEqual(leads[1]["url"], "https://lead2.com")
        self.assertEqual(leads[2]["url"], "https://lead3.com")

    @patch("lead_gen.search_businesses")
    def test_generate_leads_empty(self, mock_search):
        mock_search.return_value = []
        leads = lead_gen.generate_leads("Nonexistent", "Nowhere", num_results=5)
        self.assertEqual(leads, [])


if __name__ == "__main__":
    unittest.main()
