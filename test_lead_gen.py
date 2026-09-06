import unittest
from unittest.mock import patch, MagicMock
from lead_gen import search_businesses, extract_info, qualify_lead, generate_leads

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.search')
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["http://example1.com", "http://example2.com"]
        urls = search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(urls, ["http://example1.com", "http://example2.com"])
        mock_search.assert_called_once_with("Plumbers in London", num_results=2)

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Title</title></head><body>Contact us at info@example.com</body></html>"
        mock_get.return_value = mock_response

        info = extract_info("http://example.com")
        self.assertEqual(info["url"], "http://example.com")
        self.assertEqual(info["title"], "Test Title")
        self.assertEqual(info["email"], "info@example.com")

    @patch('lead_gen.requests.get')
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        info = extract_info("http://bad-url.com")
        self.assertEqual(info["url"], "http://bad-url.com")
        self.assertEqual(info["email"], "N/A")
        self.assertEqual(info["title"], "N/A")

    def test_qualify_lead(self):
        lead_info = {"url": "http://example.com", "email": "info@example.com", "title": "A Very Good Long Title"}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

        lead_info_low = {"url": "http://example.com", "email": "N/A", "title": "Short"}
        qualified_low = qualify_lead(lead_info_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.process_single_lead')
    def test_generate_leads(self, mock_process, mock_search):
        mock_search.return_value = ["http://example1.com", "http://example2.com"]
        mock_process.side_effect = [
            {"url": "http://example1.com", "email": "contact@ex1.com", "title": "Company One Title", "ai_score": 70, "qualification": "High"},
            {"url": "http://example2.com", "email": "N/A", "title": "Company Two Title", "ai_score": 20, "qualification": "Medium"}
        ]

        leads = generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["email"], "contact@ex1.com")
        self.assertEqual(leads[0]["ai_score"], 70)
        self.assertEqual(leads[1]["email"], "N/A")
        self.assertEqual(leads[1]["ai_score"], 20)

if __name__ == '__main__':
    unittest.main()
