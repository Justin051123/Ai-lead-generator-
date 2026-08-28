import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Business</title></head><body>Contact us at info@example.com</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Test Business")
        self.assertEqual(info["email"], "info@example.com")

    @patch("lead_gen.requests.get")
    def test_extract_info_ignores_image_emails(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><img src='logo@2x.png'>Contact: contact@domain.org</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://example.com")
        self.assertEqual(info["email"], "contact@domain.org")

    def test_qualify_lead(self):
        lead_with_email = {"url": "https://a.com", "email": "a@a.com", "title": "A Very Long Title Business"}
        qualified = lead_gen.qualify_lead(lead_with_email)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

        lead_no_email = {"url": "https://b.com", "email": "N/A", "title": "Short"}
        qualified_low = lead_gen.qualify_lead(lead_no_email)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ["https://site1.com", "https://site2.com"]
        mock_extract.side_effect = [
            {"url": "https://site1.com", "email": "one@site1.com", "title": "Site One Title"},
            {"url": "https://site2.com", "email": "N/A", "title": "Site Two Title"},
        ]

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[0]["email"], "one@site1.com")
        self.assertEqual(leads[1]["url"], "https://site2.com")

if __name__ == "__main__":
    unittest.main()
