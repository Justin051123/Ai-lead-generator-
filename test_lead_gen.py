import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example.com/1", "https://example.com/2"]
        urls = lead_gen.search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(urls, ["https://example.com/1", "https://example.com/2"])
        mock_search.assert_called_once_with("Plumbers in London", num_results=2)

    @patch("lead_gen.get_thread_session")
    def test_extract_info_success(self, mock_get_session):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Business</title></head><body>Contact us at contact@example.com</body></html>"
        mock_session.get.return_value = mock_response
        mock_get_session.return_value = mock_session

        info = lead_gen.extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Test Business")
        self.assertEqual(info["email"], "contact@example.com")

    def test_qualify_lead(self):
        lead_info = {"url": "https://example.com", "title": "Test Business Title", "email": "contact@example.com"}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ["https://example.com/1", "https://example.com/2"]
        mock_extract.side_effect = [
            {"url": "https://example.com/1", "title": "Company One", "email": "info1@example.com"},
            {"url": "https://example.com/2", "title": "Company Two", "email": "info2@example.com"}
        ]

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://example.com/1")
        self.assertEqual(leads[0]["email"], "info1@example.com")
        self.assertEqual(leads[1]["url"], "https://example.com/2")
        self.assertEqual(leads[1]["email"], "info2@example.com")

if __name__ == "__main__":
    unittest.main()
