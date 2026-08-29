import unittest
from unittest.mock import patch, MagicMock
from lead_gen import search_businesses, extract_info, qualify_lead, generate_leads

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.search')
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ['http://example1.com', 'http://example2.com']
        results = search_businesses("Roofers in Miami", num_results=2)
        self.assertEqual(results, ['http://example1.com', 'http://example2.com'])
        mock_search.assert_called_once_with("Roofers in Miami", num_results=2)

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Best Plumber</title></head><body>Contact us at info@plumber.com</body></html>'
        mock_get.return_value = mock_response

        info = extract_info('http://plumber.com')
        self.assertEqual(info['url'], 'http://plumber.com')
        self.assertEqual(info['title'], 'Best Plumber')
        self.assertEqual(info['email'], 'info@plumber.com')

    def test_qualify_lead(self):
        lead_info = {"url": "http://test.com", "email": "contact@test.com", "title": "A Great Business Title"}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ['http://a.com', 'http://b.com']
        mock_extract.side_effect = [
            {"url": "http://a.com", "email": "a@a.com", "title": "A Title long enough"},
            {"url": "http://b.com", "email": "N/A", "title": "Short"}
        ]
        leads = generate_leads("Dentists", "NY", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "http://a.com")
        self.assertEqual(leads[0]["ai_score"], 70)
        self.assertEqual(leads[1]["url"], "http://b.com")
        self.assertEqual(leads[1]["ai_score"], 0)

if __name__ == '__main__':
    unittest.main()
