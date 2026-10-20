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
        mock_response.text = "<html><head><title>Best Plumber</title></head><body>Contact us at info@plumber.com</body></html>"
        mock_get.return_value = mock_response

        info = extract_info("http://example.com")
        self.assertEqual(info["url"], "http://example.com")
        self.assertEqual(info["title"], "Best Plumber")
        self.assertEqual(info["email"], "info@plumber.com")

    @patch('lead_gen.requests.get')
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        info = extract_info("http://example-fail.com")
        self.assertEqual(info["url"], "http://example-fail.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead(self):
        lead_info = {"url": "http://example.com", "email": "contact@example.com", "title": "Example Business Title"}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads(self, mock_extract_info, mock_search_businesses):
        mock_search_businesses.return_value = ["http://example1.com", "http://example2.com"]
        mock_extract_info.side_effect = [
            {"url": "http://example1.com", "email": "a@b.com", "title": "Company One"},
            {"url": "http://example2.com", "email": "N/A", "title": "N/A"}
        ]

        leads = generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "http://example1.com")
        self.assertEqual(leads[0]["ai_score"], 70)
        self.assertEqual(leads[1]["url"], "http://example2.com")
        self.assertEqual(leads[1]["ai_score"], 0)

if __name__ == "__main__":
    unittest.main()
