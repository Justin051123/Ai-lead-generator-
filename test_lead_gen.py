import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test Business</title></head><body>Contact us at info@example.com</body></html>'
        mock_get.return_value = mock_response

        info = lead_gen.extract_info('https://example.com')
        self.assertEqual(info['url'], 'https://example.com')
        self.assertEqual(info['title'], 'Test Business')
        self.assertEqual(info['email'], 'info@example.com')

    @patch('lead_gen.requests.get')
    def test_extract_info_filters_image_emails(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test</title></head><body><img src="logo@2x.png"> contact@example.com</body></html>'
        mock_get.return_value = mock_response

        info = lead_gen.extract_info('https://example.com')
        self.assertEqual(info['email'], 'contact@example.com')

    def test_qualify_lead(self):
        lead_info = {"url": "https://example.com", "email": "info@example.com", "title": "Great Plumbers Ltd"}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified['ai_score'], 70)
        self.assertEqual(qualified['qualification'], 'High')

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ['https://a.com', 'https://b.com']
        mock_extract.side_effect = [
            {"url": "https://a.com", "email": "a@a.com", "title": "Great Plumbers Ltd"},
            {"url": "https://b.com", "email": "N/A", "title": "Company B"}
        ]

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]['url'], 'https://a.com')
        self.assertEqual(leads[0]['ai_score'], 70)
        self.assertEqual(leads[1]['url'], 'https://b.com')

if __name__ == '__main__':
    unittest.main()
