import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.requests.get')
    def test_extract_info(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test Business</title></head><body>Contact us at info@example.com</body></html>'
        mock_get.return_value = mock_response

        info = lead_gen.extract_info('http://example.com')
        self.assertEqual(info['url'], 'http://example.com')
        self.assertEqual(info['title'], 'Test Business')
        self.assertEqual(info['email'], 'info@example.com')

    def test_qualify_lead(self):
        lead = {'title': 'A Very Long Business Title', 'email': 'contact@biz.com'}
        qualified = lead_gen.qualify_lead(lead)
        self.assertEqual(qualified['ai_score'], 70)
        self.assertEqual(qualified['qualification'], 'High')

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads(self, mock_extract_info, mock_search_businesses):
        mock_search_businesses.return_value = ['http://site1.com', 'http://site2.com']
        mock_extract_info.side_effect = [
            {'url': 'http://site1.com', 'title': 'Site One Business', 'email': 'one@site.com'},
            {'url': 'http://site2.com', 'title': 'Site Two Business', 'email': 'two@site.com'}
        ]

        leads = lead_gen.generate_leads('Plumbers', 'Miami', num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]['url'], 'http://site1.com')
        self.assertEqual(leads[1]['url'], 'http://site2.com')

if __name__ == '__main__':
    unittest.main()
