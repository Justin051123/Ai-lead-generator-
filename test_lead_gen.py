import unittest
from unittest.mock import MagicMock, patch

import lead_gen


class TestLeadGen(unittest.TestCase):

    def test_qualify_lead_high(self):
        lead_info = {
            "url": "https://example.com",
            "email": "contact@example.com",
            "title": "A Great Plumbing Business",
        }
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    def test_qualify_lead_low(self):
        lead_info = {
            "url": "https://example.com",
            "email": "N/A",
            "title": "N/A",
        }
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 0)
        self.assertEqual(qualified["qualification"], "Low")

    @patch("lead_gen.get_thread_session")
    def test_extract_info(self, mock_get_session):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            "<html><head><title>Test Title</title></head>"
            "<body>Contact: info@example.com</body></html>"
        )
        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_get_session.return_value = mock_session

        info = lead_gen.extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Test Title")
        self.assertEqual(info["email"], "info@example.com")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads_parallel_order(self, mock_extract, mock_search):
        mock_search.return_value = [
            "https://site1.com",
            "https://site2.com",
            "https://site3.com",
        ]

        def fake_extract(url):
            return {
                "url": url,
                "email": f"info@{url.split('//')[1]}",
                "title": f"Title for {url}",
            }

        mock_extract.side_effect = fake_extract

        leads = lead_gen.generate_leads("Plumbers", "Miami", num_results=3)

        self.assertEqual(len(leads), 3)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[1]["url"], "https://site2.com")
        self.assertEqual(leads[2]["url"], "https://site3.com")


if __name__ == "__main__":
    unittest.main()
