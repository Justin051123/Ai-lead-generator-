import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):
    def test_qualify_lead(self):
        info = {"url": "http://example.com", "email": "test@example.com", "title": "A long enough title for test"}
        lead = lead_gen.qualify_lead(info)
        self.assertEqual(lead["ai_score"], 70)
        self.assertEqual(lead["qualification"], "High")

    def test_extract_info_no_email(self):
        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = "<html><head><title>Test Page</title></head><body>Hello World</body></html>"
            mock_get.return_value = mock_response
            info = lead_gen.extract_info("http://example.com")
            self.assertEqual(info["title"], "Test Page")
            self.assertEqual(info["email"], "N/A")

    def test_extract_info_with_email(self):
        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.text = "<html><head><title>Contact Us</title></head><body>Email: support@company.org</body></html>"
            mock_get.return_value = mock_response
            info = lead_gen.extract_info("http://company.org")
            self.assertEqual(info["title"], "Contact Us")
            self.assertEqual(info["email"], "support@company.org")

    def test_generate_leads_parallel(self):
        urls = ["http://example1.com", "http://example2.com", "http://example3.com"]
        with patch("lead_gen.search_businesses", return_value=urls), \
             patch("lead_gen.extract_info") as mock_extract:
            mock_extract.side_effect = lambda u: {"url": u, "email": f"contact@{u.split('//')[1]}", "title": f"Title for {u}"}
            leads = lead_gen.generate_leads("Plumbers", "London", num_results=3)
            self.assertEqual(len(leads), 3)
            # Verify order is preserved
            self.assertEqual(leads[0]["url"], urls[0])
            self.assertEqual(leads[1]["url"], urls[1])
            self.assertEqual(leads[2]["url"], urls[2])

if __name__ == "__main__":
    unittest.main()
