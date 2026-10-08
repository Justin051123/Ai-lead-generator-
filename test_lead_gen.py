import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        urls = lead_gen.search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(urls, ["https://example1.com", "https://example2.com"])
        mock_search.assert_called_once_with("Plumbers in London", num_results=2)

    @patch("lead_gen.get_thread_session")
    def test_extract_info_success(self, mock_get_session):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title> Acme Plumbing </title></head><body>Contact us at info@acme.com and logo.png</body></html>"
        mock_session.get.return_value = mock_response
        mock_get_session.return_value = mock_session

        info = lead_gen.extract_info("https://acme.com")
        self.assertEqual(info["url"], "https://acme.com")
        self.assertEqual(info["title"], "Acme Plumbing")
        self.assertEqual(info["email"], "info@acme.com")

    @patch("lead_gen.get_thread_session")
    def test_extract_info_http_error(self, mock_get_session):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_session.get.return_value = mock_response
        mock_get_session.return_value = mock_session

        info = lead_gen.extract_info("https://acme.com/404")
        self.assertEqual(info["url"], "https://acme.com/404")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead(self):
        lead_info = {"url": "https://example.com", "title": "Example Business Title Here", "email": "contact@example.com"}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

        lead_info_low = {"url": "https://example.com", "title": "Short", "email": "N/A"}
        qualified_low = lead_gen.qualify_lead(lead_info_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ["https://site1.com", "https://site2.com"]
        mock_extract.side_effect = [
            {"url": "https://site1.com", "title": "Site 1 Title Long Enough", "email": "site1@test.com"},
            {"url": "https://site2.com", "title": "Site 2 Title Long Enough", "email": "N/A"}
        ]

        leads = lead_gen.generate_leads("Dentists", "Miami", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[0]["qualification"], "High")
        self.assertEqual(leads[1]["url"], "https://site2.com")
        self.assertEqual(leads[1]["qualification"], "Medium")

if __name__ == "__main__":
    unittest.main()
