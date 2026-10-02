import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):
    @patch('lead_gen.search')
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ['http://example1.com', 'http://example2.com']
        urls = lead_gen.search_businesses('Plumbers in London', 2)
        self.assertEqual(urls, ['http://example1.com', 'http://example2.com'])

    @patch('lead_gen.get_thread_session')
    def test_extract_info_success(self, mock_get_session):
        mock_session = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = '<html><head><title>Test Title</title></head><body>Contact us: test@example.com</body></html>'
        mock_session.get.return_value = mock_resp
        mock_get_session.return_value = mock_session

        info = lead_gen.extract_info('http://example.com')
        self.assertEqual(info['url'], 'http://example.com')
        self.assertEqual(info['title'], 'Test Title')
        self.assertEqual(info['email'], 'test@example.com')

    @patch('lead_gen.get_thread_session')
    def test_extract_info_failure(self, mock_get_session):
        mock_session = MagicMock()
        mock_session.get.side_effect = Exception("Connection error")
        mock_get_session.return_value = mock_session

        info = lead_gen.extract_info('http://example.com')
        self.assertEqual(info['url'], 'http://example.com')
        self.assertEqual(info['title'], 'N/A')
        self.assertEqual(info['email'], 'N/A')

    def test_qualify_lead(self):
        lead_info = {'url': 'http://example.com', 'title': 'Long title here', 'email': 'test@example.com'}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified['ai_score'], 70)
        self.assertEqual(qualified['qualification'], 'High')

    @patch('lead_gen.extract_info')
    @patch('lead_gen.search_businesses')
    def test_generate_leads_order_and_parallel(self, mock_search, mock_extract):
        mock_search.return_value = ['http://site1.com', 'http://site2.com', 'http://site3.com']
        mock_extract.side_effect = lambda url: {'url': url, 'title': f'Title for {url}', 'email': 'N/A'}

        leads = lead_gen.generate_leads('Plumbers', 'London', 3)
        self.assertEqual(len(leads), 3)
        self.assertEqual(leads[0]['url'], 'http://site1.com')
        self.assertEqual(leads[1]['url'], 'http://site2.com')
        self.assertEqual(leads[2]['url'], 'http://site3.com')

if __name__ == '__main__':
    unittest.main()
