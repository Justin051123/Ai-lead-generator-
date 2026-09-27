import unittest
from unittest.mock import patch, MagicMock
from lead_gen import extract_info, qualify_lead, generate_leads

class TestLeadGen(unittest.TestCase):
    def test_qualify_lead(self):
        info = {"url": "https://example.com", "email": "test@example.com", "title": "A Very Good Title Here"}
        qualified = qualify_lead(info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch("lead_gen.get_thread_session")
    def test_extract_info(self, mock_get_session):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Business</title></head><body>Contact us at info@example.com</body></html>"
        mock_session.get.return_value = mock_response
        mock_get_session.return_value = mock_session

        info = extract_info("https://example.com")
        self.assertEqual(info["title"], "Test Business")
        self.assertEqual(info["email"], "info@example.com")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ["https://site1.com", "https://site2.com"]
        mock_extract.side_effect = [
            {"url": "https://site1.com", "email": "contact@site1.com", "title": "Site 1 Title Long"},
            {"url": "https://site2.com", "email": "N/A", "title": "Short"}
        ]

        leads = generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[0]["qualification"], "High")
        self.assertEqual(leads[1]["url"], "https://site2.com")
        self.assertEqual(leads[1]["qualification"], "Low")

if __name__ == "__main__":
    unittest.main()
