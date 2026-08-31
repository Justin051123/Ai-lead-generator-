import unittest
from unittest.mock import patch, MagicMock
from lead_gen import extract_info, qualify_lead, generate_leads

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test Business</title></head><body>Contact us at contact@example.com</body></html>'
        mock_get.return_value = mock_response

        info = extract_info('http://example.com')
        self.assertEqual(info['url'], 'http://example.com')
        self.assertEqual(info['title'], 'Test Business')
        self.assertEqual(info['email'], 'contact@example.com')

    @patch('lead_gen.requests.get')
    def test_extract_info_filters_image_emails(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test</title></head><body>image@example.png info@example.com</body></html>'
        mock_get.return_value = mock_response

        info = extract_info('http://example.com')
        self.assertEqual(info['email'], 'info@example.com')

    @patch('lead_gen.requests.get')
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        info = extract_info('http://invalid-domain.com')
        self.assertEqual(info['email'], 'N/A')
        self.assertEqual(info['title'], 'N/A')

    def test_qualify_lead(self):
        lead = {"url": "http://example.com", "email": "test@example.com", "title": "A Great Business Name"}
        qualified = qualify_lead(lead)
        self.assertEqual(qualified['ai_score'], 70)
        self.assertEqual(qualified['qualification'], 'High')

        low_lead = {"url": "http://example.com", "email": "N/A", "title": "Short"}
        qualified_low = qualify_lead(low_lead)
        self.assertEqual(qualified_low['ai_score'], 0)
        self.assertEqual(qualified_low['qualification'], 'Low')

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ['http://example1.com', 'http://example2.com']
        mock_extract.side_effect = lambda url: {'url': url, 'email': 'test@example.com', 'title': 'Long Business Title'}

        leads = generate_leads('Plumbers', 'London', num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]['url'], 'http://example1.com')
        self.assertEqual(leads[1]['url'], 'http://example2.com')
        self.assertEqual(leads[0]['ai_score'], 70)

if __name__ == '__main__':
    unittest.main()
