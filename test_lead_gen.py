import unittest
from unittest.mock import patch, MagicMock
from lead_gen import search_businesses, extract_info, qualify_lead, generate_leads

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["http://example.com", "http://test.com"]
        urls = search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(urls, ["http://example.com", "http://test.com"])

    @patch("lead_gen.get_thread_session")
    def test_extract_info(self, mock_get_thread_session):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Title</title></head><body>Contact us at contact@example.com</body></html>"
        mock_session.get.return_value = mock_response
        mock_get_thread_session.return_value = mock_session

        info = extract_info("http://example.com")
        self.assertEqual(info["url"], "http://example.com")
        self.assertEqual(info["title"], "Test Title")
        self.assertEqual(info["email"], "contact@example.com")

    def test_qualify_lead(self):
        lead_info = {"url": "http://example.com", "title": "A Very Long Business Title", "email": "info@biz.com"}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads(self, mock_extract_info, mock_search_businesses):
        mock_search_businesses.return_value = ["http://example1.com", "http://example2.com"]
        mock_extract_info.side_effect = [
            {"url": "http://example1.com", "email": "info@a.com", "title": "Company A Title"},
            {"url": "http://example2.com", "email": "N/A", "title": "Company B Title"},
        ]

        leads = generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "http://example1.com")
        self.assertEqual(leads[1]["url"], "http://example2.com")
        self.assertEqual(leads[0]["email"], "info@a.com")

if __name__ == "__main__":
    unittest.main()
