import unittest
from unittest.mock import patch, MagicMock
from lead_gen import search_businesses, extract_info, qualify_lead, generate_leads, process_single_lead

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.search')
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ['https://example1.com', 'https://example2.com']
        urls = search_businesses('Plumbers in London', num_results=2)
        self.assertEqual(urls, ['https://example1.com', 'https://example2.com'])

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test Business</title></head><body>Contact us: info@example.com</body></html>'
        mock_get.return_value = mock_response

        info = extract_info('https://example.com')
        self.assertEqual(info['url'], 'https://example.com')
        self.assertEqual(info['title'], 'Test Business')
        self.assertEqual(info['email'], 'info@example.com')

    def test_qualify_lead(self):
        lead_info = {'url': 'https://example.com', 'title': 'Test Business', 'email': 'info@example.com'}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified['ai_score'], 70)
        self.assertEqual(qualified['qualification'], 'High')

    @patch('lead_gen.extract_info')
    def test_process_single_lead(self, mock_extract):
        mock_extract.return_value = {'url': 'https://example.com', 'title': 'Test Business', 'email': 'info@example.com'}
        result = process_single_lead('https://example.com')
        self.assertEqual(result['url'], 'https://example.com')
        self.assertEqual(result['ai_score'], 70)
        self.assertEqual(result['qualification'], 'High')

    @patch('lead_gen.process_single_lead')
    @patch('lead_gen.search_businesses')
    def test_generate_leads_parallel(self, mock_search, mock_process):
        mock_search.return_value = ['https://example1.com', 'https://example2.com']
        mock_process.side_effect = [
            {'url': 'https://example1.com', 'title': 'Biz 1', 'email': 'a@b.com', 'ai_score': 70, 'qualification': 'High'},
            {'url': 'https://example2.com', 'title': 'Biz 2', 'email': 'N/A', 'ai_score': 0, 'qualification': 'Low'}
        ]

        leads = generate_leads('Plumbers', 'London', num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]['url'], 'https://example1.com')
        self.assertEqual(leads[1]['url'], 'https://example2.com')

if __name__ == '__main__':
    unittest.main()
