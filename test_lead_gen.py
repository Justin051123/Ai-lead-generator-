import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["http://example.com", "http://test.com"]
        urls = lead_gen.search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(urls, ["http://example.com", "http://test.com"])
        mock_search.assert_called_once_with("Plumbers in London", num_results=2)

    @patch("lead_gen.requests.get")
    def test_extract_info(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Business</title></head><body>Contact us at contact@test.com</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("http://test.com")
        self.assertEqual(info["url"], "http://test.com")
        self.assertEqual(info["title"], "Test Business")
        self.assertEqual(info["email"], "contact@test.com")

    def test_qualify_lead(self):
        info_high = {"url": "http://test.com", "email": "info@test.com", "title": "A Very Good Long Title"}
        lead = lead_gen.qualify_lead(info_high)
        self.assertEqual(lead["ai_score"], 70)
        self.assertEqual(lead["qualification"], "High")

        info_low = {"url": "http://test.com", "email": "N/A", "title": "Short"}
        lead = lead_gen.qualify_lead(info_low)
        self.assertEqual(lead["ai_score"], 0)
        self.assertEqual(lead["qualification"], "Low")

    @patch("lead_gen.search")
    @patch("lead_gen.requests.get")
    def test_generate_leads(self, mock_get, mock_search):
        mock_search.return_value = ["http://test1.com", "http://test2.com"]

        def side_effect(url, timeout=10, headers=None):
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.text = f"<html><head><title>Title for {url}</title></head><body>Email: admin@{url.replace('http://', '')}</body></html>"
            return mock_resp

        mock_get.side_effect = side_effect

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "http://test1.com")
        self.assertEqual(leads[0]["email"], "admin@test1.com")
        self.assertEqual(leads[1]["url"], "http://test2.com")
        self.assertEqual(leads[1]["email"], "admin@test2.com")

if __name__ == "__main__":
    unittest.main()
