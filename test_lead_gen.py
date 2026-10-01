import unittest
from unittest.mock import MagicMock, patch
from lead_gen import (
    search_businesses,
    extract_info,
    qualify_lead,
    generate_leads,
)


class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        urls = search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(len(urls), 2)
        self.assertEqual(urls[0], "https://example1.com")

    @patch("lead_gen.get_thread_session")
    def test_extract_info_success(self, mock_get_session):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Best Plumber Services</title></head><body>Contact us at info@bestplumber.com</body></html>"

        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_get_session.return_value = mock_session

        info = extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Best Plumber Services")
        self.assertEqual(info["email"], "info@bestplumber.com")

    def test_qualify_lead(self):
        lead_info = {
            "url": "https://example.com",
            "title": "Best Plumber Services",
            "email": "info@bestplumber.com",
        }
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads_concurrent(self, mock_extract_info, mock_search_businesses):
        mock_search_businesses.return_value = [
            "https://example1.com",
            "https://example2.com",
        ]
        mock_extract_info.side_effect = lambda url: {
            "url": url,
            "title": f"Title for {url}",
            "email": "test@example.com" if "1" in url else "N/A",
        }

        leads = generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://example1.com")
        self.assertEqual(leads[0]["email"], "test@example.com")
        self.assertEqual(leads[1]["url"], "https://example2.com")
        self.assertEqual(leads[1]["email"], "N/A")


if __name__ == "__main__":
    unittest.main()
