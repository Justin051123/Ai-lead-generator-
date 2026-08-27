import unittest
from unittest.mock import patch, MagicMock
from lead_gen import search_businesses, extract_info, qualify_lead, process_single_lead, generate_leads

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.search')
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ['http://example1.com', 'http://example2.com']
        urls = search_businesses('Plumbers in London', num_results=2)
        self.assertEqual(urls, ['http://example1.com', 'http://example2.com'])
        mock_search.assert_called_once_with('Plumbers in London', num_results=2)

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Example Business Website</title></head><body>Contact us at contact@example.com</body></html>'
        mock_get.return_value = mock_response

        info = extract_info('http://example.com')
        self.assertEqual(info['url'], 'http://example.com')
        self.assertEqual(info['title'], 'Example Business Website')
        self.assertEqual(info['email'], 'contact@example.com')

    @patch('lead_gen.requests.get')
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection error")

        info = extract_info('http://invalid-url.com')
        self.assertEqual(info['url'], 'http://invalid-url.com')
        self.assertEqual(info['email'], 'N/A')
        self.assertEqual(info['title'], 'N/A')

    def test_qualify_lead(self):
        info_high = {"url": "http://example.com", "email": "info@example.com", "title": "A Very Long Business Title Here"}
        qualified_high = qualify_lead(info_high)
        self.assertEqual(qualified_high["ai_score"], 70)
        self.assertEqual(qualified_high["qualification"], "High")

        info_low = {"url": "http://example.com", "email": "N/A", "title": "Short"}
        qualified_low = qualify_lead(info_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch('lead_gen.extract_info')
    def test_process_single_lead(self, mock_extract):
        mock_extract.return_value = {"url": "http://example.com", "email": "test@test.com", "title": "Long Enough Title"}
        lead = process_single_lead("http://example.com")
        self.assertEqual(lead["url"], "http://example.com")
        self.assertEqual(lead["ai_score"], 70)

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads_parallel_and_order(self, mock_extract, mock_search):
        mock_search.return_value = [
            'http://site1.com',
            'http://site2.com',
            'http://site3.com'
        ]
        def side_effect(url):
            return {
                'url': url,
                'email': f'info@{url.split("//")[1]}',
                'title': f'Title for {url}'
            }
        mock_extract.side_effect = side_effect

        leads = generate_leads('Roofers', 'Miami', num_results=3)
        self.assertEqual(len(leads), 3)
        self.assertEqual(leads[0]['url'], 'http://site1.com')
        self.assertEqual(leads[1]['url'], 'http://site2.com')
        self.assertEqual(leads[2]['url'], 'http://site3.com')

if __name__ == '__main__':
    unittest.main()
