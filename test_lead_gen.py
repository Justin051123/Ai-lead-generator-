import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test Business</title></head><body>Contact us at info@test.com</body></html>'
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Test Business")
        self.assertEqual(info["email"], "info@test.com")

    def test_qualify_lead(self):
        lead_info = {"url": "https://example.com", "email": "info@test.com", "title": "Test Business Title"}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.requests.get')
    def test_generate_leads(self, mock_get, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test</title></head><body>Email contact@example.com</body></html>'
        mock_get.return_value = mock_response

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["email"], "contact@example.com")

if __name__ == '__main__':
    unittest.main()
