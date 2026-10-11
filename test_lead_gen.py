import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["http://example.com", "http://example.org"]
        urls = lead_gen.search_businesses("plumbers in London", num_results=2)
        self.assertEqual(len(urls), 2)
        self.assertIn("http://example.com", urls)

    @patch("lead_gen.get_thread_session")
    def test_extract_info(self, mock_get_session):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Business</title></head><body>Contact us at info@example.com</body></html>"
        mock_session.get.return_value = mock_response
        mock_get_session.return_value = mock_session

        info = lead_gen.extract_info("http://example.com")
        self.assertEqual(info["url"], "http://example.com")
        self.assertEqual(info["title"], "Test Business")
        self.assertEqual(info["email"], "info@example.com")

    def test_qualify_lead(self):
        lead_info = {
            "url": "http://example.com",
            "title": "A Very Long Business Name That Meets Criteria",
            "email": "contact@example.com"
        }
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertGreater(qualified["ai_score"], 50)
        self.assertEqual(qualified["qualification"], "High")

    @patch("lead_gen.extract_info")
    @patch("lead_gen.search_businesses")
    def test_generate_leads(self, mock_search, mock_extract):
        mock_search.return_value = ["http://example1.com", "http://example2.com"]
        mock_extract.side_effect = lambda url: {
            "url": url,
            "title": f"Title for {url}",
            "email": "test@domain.com" if "example1" in url else "N/A"
        }

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "http://example1.com")
        self.assertEqual(leads[1]["url"], "http://example2.com")

if __name__ == "__main__":
    unittest.main()
