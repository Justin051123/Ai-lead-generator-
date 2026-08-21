import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title> Test Company </title></head><body>Contact us at info@example.com</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("http://example.com")
        self.assertEqual(info["url"], "http://example.com")
        self.assertEqual(info["title"], "Test Company")
        self.assertEqual(info["email"], "info@example.com")

    def test_qualify_lead(self):
        info = {"url": "http://example.com", "title": "Test Company", "email": "info@example.com"}
        qualified = lead_gen.qualify_lead(info)
        self.assertIn("ai_score", qualified)
        self.assertEqual(qualified["qualification"], "High")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.requests.get')
    def test_generate_leads(self, mock_get, mock_search):
        mock_search.return_value = ["http://example1.com", "http://example2.com"]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Company</title></head><body>contact@test.com</body></html>"
        mock_get.return_value = mock_response

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "http://example1.com")
        self.assertEqual(leads[1]["url"], "http://example2.com")

if __name__ == '__main__':
    unittest.main()
