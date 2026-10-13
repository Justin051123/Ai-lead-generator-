import unittest
from unittest.mock import patch, MagicMock
from lead_gen import search_businesses, extract_info, qualify_lead, generate_leads


class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        urls = search_businesses("Plumbers London", num_results=2)
        self.assertEqual(urls, ["https://example1.com", "https://example2.com"])
        mock_search.assert_called_once_with("Plumbers London", num_results=2)

    @patch("lead_gen.get_thread_session")
    def test_extract_info_success(self, mock_get_session):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            "<html><head><title>Best Plumber</title></head>"
            "<body>Contact us at info@example.com or support@example.com</body></html>"
        )
        mock_session.get.return_value = mock_response
        mock_get_session.return_value = mock_session

        info = extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Best Plumber")
        self.assertIn("@example.com", info["email"])

    @patch("lead_gen.get_thread_session")
    def test_extract_info_failure(self, mock_get_session):
        mock_session = MagicMock()
        mock_session.get.side_effect = Exception("Connection error")
        mock_get_session.return_value = mock_session

        info = extract_info("https://invalid.com")
        self.assertEqual(info["url"], "https://invalid.com")
        self.assertEqual(info["email"], "N/A")
        self.assertEqual(info["title"], "N/A")

    def test_qualify_lead(self):
        lead_info = {
            "url": "https://example.com",
            "email": "contact@example.com",
            "title": "Great Business Title Here",
        }
        qualified = qualify_lead(lead_info)
        self.assertGreater(qualified["ai_score"], 0)
        self.assertIn(qualified["qualification"], ["High", "Medium", "Low"])

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ["https://site1.com", "https://site2.com"]
        mock_extract.side_effect = lambda url: {
            "url": url,
            "email": f"contact@{url.split('//')[1]}",
            "title": f"Title for {url}",
        }

        leads = generate_leads("Dentists", "Miami", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[1]["url"], "https://site2.com")


if __name__ == "__main__":
    unittest.main()
