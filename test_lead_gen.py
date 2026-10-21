import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://site1.com", "https://site2.com"]
        urls = lead_gen.search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(urls, ["https://site1.com", "https://site2.com"])
        mock_search.assert_called_once_with("Plumbers in London", num_results=2)

    @patch("lead_gen.search")
    def test_search_businesses_exception(self, mock_search):
        mock_search.side_effect = Exception("Search API rate limit")
        urls = lead_gen.search_businesses("Plumbers in London")
        self.assertEqual(urls, [])

    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Best Plumber Services</title></head><body>Contact us at contact@plumber.com or info@plumber.com</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://plumber.com")
        self.assertEqual(info["url"], "https://plumber.com")
        self.assertEqual(info["title"], "Best Plumber Services")
        self.assertIn(info["email"], ["contact@plumber.com", "info@plumber.com"])

    @patch("lead_gen.requests.get")
    def test_extract_info_image_email_filtered(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>My Business</title></head><body><img src='logo@2x.png'>hello@business.com</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://business.com")
        self.assertEqual(info["email"], "hello@business.com")

    @patch("lead_gen.requests.get")
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection timeout")
        info = lead_gen.extract_info("https://invalid-domain.test")
        self.assertEqual(info["url"], "https://invalid-domain.test")
        self.assertEqual(info["email"], "N/A")
        self.assertEqual(info["title"], "N/A")

    def test_qualify_lead(self):
        lead_high = {"url": "http://a.com", "email": "a@a.com", "title": "Very Long Business Title Here"}
        lead_med = {"url": "http://b.com", "email": "N/A", "title": "Very Long Business Title Here"}
        lead_low = {"url": "http://c.com", "email": "N/A", "title": "Short"}

        self.assertEqual(lead_gen.qualify_lead(lead_high)["qualification"], "High")
        self.assertEqual(lead_gen.qualify_lead(lead_med)["qualification"], "Medium")
        self.assertEqual(lead_gen.qualify_lead(lead_low)["qualification"], "Low")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads_order_and_content(self, mock_extract, mock_search):
        mock_search.return_value = ["https://site1.com", "https://site2.com", "https://site3.com"]

        def fake_extract(url):
            idx = url[-5]
            return {"url": url, "email": f"info@site{idx}.com", "title": f"Business Title Number {idx}"}

        mock_extract.side_effect = fake_extract

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=3)
        self.assertEqual(len(leads), 3)
        self.assertEqual([lead["url"] for lead in leads], ["https://site1.com", "https://site2.com", "https://site3.com"])
        self.assertEqual(leads[0]["email"], "info@site1.com")
        self.assertEqual(leads[1]["email"], "info@site2.com")
        self.assertEqual(leads[2]["email"], "info@site3.com")

if __name__ == "__main__":
    unittest.main()
