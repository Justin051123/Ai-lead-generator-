import unittest
from unittest.mock import patch, MagicMock
from lead_gen import extract_info, qualify_lead, generate_leads

class TestLeadGen(unittest.TestCase):
    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test Business</title></head><body>Contact us at info@example.com</body></html>'
        mock_get.return_value = mock_response

        info = extract_info("http://example.com")
        self.assertEqual(info["url"], "http://example.com")
        self.assertEqual(info["title"], "Test Business")
        self.assertEqual(info["email"], "info@example.com")

    def test_qualify_lead(self):
        lead_info = {"url": "http://example.com", "email": "info@example.com", "title": "Test Business Title"}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ["http://example1.com", "http://example2.com"]
        mock_extract.side_effect = lambda url: {"url": url, "email": "test@example.com", "title": "Sample Title"}

        leads = generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "http://example1.com")
        self.assertEqual(leads[1]["url"], "http://example2.com")

if __name__ == '__main__':
    unittest.main()
