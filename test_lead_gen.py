import unittest
from unittest.mock import patch, MagicMock
from lead_gen import search_businesses, extract_info, qualify_lead, generate_leads

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.search')
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ['http://example1.com', 'http://example2.com']
        results = search_businesses('plumbers in London', num_results=2)
        self.assertEqual(results, ['http://example1.com', 'http://example2.com'])
        mock_search.assert_called_once_with('plumbers in London', num_results=2)

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test Business</title></head><body>Contact us at info@example.com</body></html>'
        mock_get.return_value = mock_response

        info = extract_info('http://example.com')
        self.assertEqual(info['url'], 'http://example.com')
        self.assertEqual(info['title'], 'Test Business')
        self.assertEqual(info['email'], 'info@example.com')

    @patch('lead_gen.requests.get')
    def test_extract_info_image_email_filtered(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test Business</title></head><body><img src="logo@2x.png"> contact@domain.com</body></html>'
        mock_get.return_value = mock_response

        info = extract_info('http://example.com')
        self.assertEqual(info['email'], 'contact@domain.com')

    def test_qualify_lead(self):
        lead_high = {'url': 'http://a.com', 'title': 'Very Long Business Title', 'email': 'contact@a.com'}
        qualified_high = qualify_lead(lead_high)
        self.assertEqual(qualified_high['ai_score'], 70)
        self.assertEqual(qualified_high['qualification'], 'High')

        lead_medium = {'url': 'http://b.com', 'title': 'Short', 'email': 'contact@b.com'}
        qualified_medium = qualify_lead(lead_medium)
        self.assertEqual(qualified_medium['ai_score'], 50)
        self.assertEqual(qualified_medium['qualification'], 'Medium')

        lead_low = {'url': 'http://c.com', 'title': 'Short', 'email': 'N/A'}
        qualified_low = qualify_lead(lead_low)
        self.assertEqual(qualified_low['ai_score'], 0)
        self.assertEqual(qualified_low['qualification'], 'Low')

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ['http://example1.com', 'http://example2.com']
        mock_extract.side_effect = [
            {'url': 'http://example1.com', 'title': 'Business 1 Long Name', 'email': 'a@example1.com'},
            {'url': 'http://example2.com', 'title': 'Business 2 Long Name', 'email': 'b@example2.com'}
        ]

        leads = generate_leads('Plumbers', 'London', num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]['url'], 'http://example1.com')
        self.assertEqual(leads[1]['url'], 'http://example2.com')

if __name__ == '__main__':
    unittest.main()
