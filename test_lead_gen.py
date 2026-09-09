import unittest
from unittest.mock import patch, MagicMock
from lead_gen import extract_info, qualify_lead, generate_leads

class TestLeadGen(unittest.TestCase):

    def test_qualify_lead(self):
        lead = {"url": "http://example.com", "email": "test@example.com", "title": "A Very Long Title For Testing"}
        qualified = qualify_lead(lead)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test Title</title></head><body>contact@test.com</body></html>'
        mock_get.return_value = mock_response

        info = extract_info('http://example.com')
        self.assertEqual(info['title'], 'Test Title')
        self.assertEqual(info['email'], 'contact@test.com')

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ['http://example1.com', 'http://example2.com']
        mock_extract.side_effect = [
            {'url': 'http://example1.com', 'email': 'a@b.com', 'title': 'Title One Long Enough'},
            {'url': 'http://example2.com', 'email': 'N/A', 'title': 'Short'}
        ]

        leads = generate_leads('Plumbers', 'London', num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]['url'], 'http://example1.com')
        self.assertEqual(leads[1]['url'], 'http://example2.com')

if __name__ == '__main__':
    unittest.main()
