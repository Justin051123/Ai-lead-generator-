import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    def test_qualify_lead(self):
        lead_with_email = {"title": "A standard company title", "email": "test@example.com"}
        qualified = lead_gen.qualify_lead(lead_with_email)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

        lead_no_email = {"title": "Short", "email": "N/A"}
        qualified_low = lead_gen.qualify_lead(lead_no_email)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch("requests.get")
    def test_extract_info(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Business</title></head><body>Contact us at info@testbusiness.com</body></html>"

        if hasattr(lead_gen, "get_thread_session"):
            mock_session = MagicMock()
            mock_session.get.return_value = mock_response
            with patch("lead_gen.get_thread_session", return_value=mock_session):
                info = lead_gen.extract_info("http://example.com")
        else:
            mock_requests_get.return_value = mock_response
            info = lead_gen.extract_info("http://example.com")

        self.assertEqual(info["url"], "http://example.com")
        self.assertEqual(info["title"], "Test Business")
        self.assertEqual(info["email"], "info@testbusiness.com")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads(self, mock_extract_info, mock_search):
        mock_search.return_value = ["http://example1.com", "http://example2.com"]
        mock_extract_info.side_effect = [
            {"url": "http://example1.com", "email": "e1@test.com", "title": "Title long enough 1"},
            {"url": "http://example2.com", "email": "e2@test.com", "title": "Title long enough 2"}
        ]

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "http://example1.com")
        self.assertEqual(leads[1]["url"], "http://example2.com")
        self.assertEqual(leads[0]["ai_score"], 70)

if __name__ == "__main__":
    unittest.main()
