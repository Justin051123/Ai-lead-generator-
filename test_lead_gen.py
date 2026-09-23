import unittest
from unittest.mock import patch, MagicMock
from lead_gen import extract_info, qualify_lead, generate_leads, search_businesses

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        results = search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(results, ["https://example1.com", "https://example2.com"])
        mock_search.assert_called_once_with("Plumbers in London", num_results=2)

    @patch("lead_gen.get_thread_session", create=True)
    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get, mock_get_thread_session=None):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Business</title></head><body>Contact: contact@example.com</body></html>"
        mock_get.return_value = mock_response

        # In case get_thread_session is present
        if hasattr(mock_get_thread_session, "return_value"):
            session_mock = MagicMock()
            session_mock.get.return_value = mock_response
            mock_get_thread_session.return_value = session_mock

        info = extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Test Business")
        self.assertEqual(info["email"], "contact@example.com")

    def test_qualify_lead(self):
        lead_info = {"url": "https://example.com", "email": "info@example.com", "title": "Example Business Title"}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

        low_lead = {"url": "https://example.com", "email": "N/A", "title": "Short"}
        qualified_low = qualify_lead(low_lead)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ["https://site1.com", "https://site2.com"]
        mock_extract.side_effect = [
            {"url": "https://site1.com", "email": "a@site1.com", "title": "Site 1 Title Example"},
            {"url": "https://site2.com", "email": "N/A", "title": "Site 2 Title Example"},
        ]

        leads = generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[0]["email"], "a@site1.com")
        self.assertEqual(leads[0]["qualification"], "High")
        self.assertEqual(leads[1]["url"], "https://site2.com")
        self.assertEqual(leads[1]["qualification"], "Medium")

if __name__ == "__main__":
    unittest.main()
