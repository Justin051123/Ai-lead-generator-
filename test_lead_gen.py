import unittest
from unittest.mock import patch, MagicMock
from lead_gen import extract_info, qualify_lead, generate_leads

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.get_thread_session')
    def test_extract_info_success(self, mock_get_session):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test Business</title></head><body>Contact us at info@example.com</body></html>'
        mock_session.get.return_value = mock_response
        mock_get_session.return_value = mock_session

        info = extract_info('https://example.com')
        self.assertEqual(info['url'], 'https://example.com')
        self.assertEqual(info['title'], 'Test Business')
        self.assertEqual(info['email'], 'info@example.com')

    @patch('lead_gen.get_thread_session')
    def test_extract_info_filters_images(self, mock_get_session):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test</title></head><body><img src="logo@2x.png"/> Contact: hello@company.com</body></html>'
        mock_session.get.return_value = mock_response
        mock_get_session.return_value = mock_session

        info = extract_info('https://example.com')
        self.assertEqual(info['email'], 'hello@company.com')

    def test_qualify_lead(self):
        lead_info = {'url': 'https://example.com', 'title': 'Long Business Title Here', 'email': 'info@example.com'}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified['ai_score'], 70)
        self.assertEqual(qualified['qualification'], 'High')

        lead_info_low = {'url': 'https://example.com', 'title': 'Short', 'email': 'N/A'}
        qualified_low = qualify_lead(lead_info_low)
        self.assertEqual(qualified_low['ai_score'], 0)
        self.assertEqual(qualified_low['qualification'], 'Low')

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ['https://site1.com', 'https://site2.com']
        mock_extract.side_effect = [
            {'url': 'https://site1.com', 'title': 'Site 1 Official Title', 'email': 'contact@site1.com'},
            {'url': 'https://site2.com', 'title': 'Site 2', 'email': 'N/A'}
        ]

        leads = generate_leads('Plumbers', 'London', num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]['url'], 'https://site1.com')
        self.assertEqual(leads[0]['ai_score'], 70)
        self.assertEqual(leads[1]['url'], 'https://site2.com')

if __name__ == '__main__':
    unittest.main()
