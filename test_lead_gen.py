import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):
    def test_extract_info(self):
        mock_html = "<html><head><title>Test Business</title></head><body>Email: test@example.com</body></html>"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = mock_html

        with patch("requests.get", return_value=mock_response):
            info = lead_gen.extract_info("http://test.com")
            self.assertEqual(info["url"], "http://test.com")
            self.assertEqual(info["title"], "Test Business")
            self.assertEqual(info["email"], "test@example.com")

    def test_qualify_lead(self):
        info = {"url": "http://test.com", "email": "test@example.com", "title": "Test Business Title"}
        qualified = lead_gen.qualify_lead(info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    def test_generate_leads(self):
        mock_urls = ["http://example1.com", "http://example2.com"]
        mock_html = "<html><head><title>Test Title Long Enough</title></head><body>info@example.com</body></html>"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = mock_html

        with patch("lead_gen.search_businesses", return_value=mock_urls), patch("requests.get", return_value=mock_response):
            leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
            self.assertEqual(len(leads), 2)
            self.assertEqual(leads[0]["url"], "http://example1.com")
            self.assertEqual(leads[1]["url"], "http://example2.com")

if __name__ == "__main__":
    unittest.main()
