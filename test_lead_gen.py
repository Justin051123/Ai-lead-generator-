import unittest
from unittest.mock import patch, Mock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        urls = lead_gen.search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(urls, ["https://example1.com", "https://example2.com"])
        mock_search.assert_called_once_with("Plumbers in London", num_results=2)

    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Business</title></head><body>Email: contact@test.com</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Test Business")
        self.assertEqual(info["email"], "contact@test.com")

    def test_qualify_lead(self):
        lead_info = {"title": "A Very Long Business Title Here", "email": "contact@example.com"}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch("lead_gen.search")
    @patch("lead_gen.requests.get")
    def test_generate_leads(self, mock_get, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Business Title</title></head><body>Email: info@example.com</body></html>"
        mock_get.return_value = mock_response

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://example1.com")
        self.assertEqual(leads[1]["url"], "https://example2.com")

if __name__ == "__main__":
    unittest.main()
