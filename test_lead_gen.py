import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Acme Corp</title></head><body>Contact us at info@acme.com</body></html>'
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("http://acme.com")
        self.assertEqual(info["url"], "http://acme.com")
        self.assertEqual(info["title"], "Acme Corp")
        self.assertEqual(info["email"], "info@acme.com")

    @patch('lead_gen.requests.get')
    def test_extract_info_filters_images(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test</title></head><body><img src="logo@2x.png"> contact@example.com</body></html>'
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("http://example.com")
        self.assertEqual(info["email"], "contact@example.com")

    def test_qualify_lead(self):
        lead_info = {"url": "http://example.com", "title": "Example Business Title", "email": "test@example.com"}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch('lead_gen.extract_info')
    @patch('lead_gen.search_businesses')
    def test_generate_leads(self, mock_search, mock_extract):
        mock_search.return_value = ["http://a.com", "http://b.com"]
        mock_extract.side_effect = [
            {"url": "http://a.com", "title": "Company A Title", "email": "a@a.com"},
            {"url": "http://b.com", "title": "Company B Title", "email": "N/A"},
        ]

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "http://a.com")
        self.assertEqual(leads[0]["qualification"], "High")
        self.assertEqual(leads[1]["url"], "http://b.com")
        self.assertEqual(leads[1]["qualification"], "Medium")

if __name__ == "__main__":
    unittest.main()
