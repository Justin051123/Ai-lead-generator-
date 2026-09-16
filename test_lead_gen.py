import unittest
from unittest.mock import patch, MagicMock
from lead_gen import search_businesses, extract_info, qualify_lead, generate_leads, EMAIL_PATTERN

class TestLeadGen(unittest.TestCase):

    def test_email_pattern(self):
        text = "Contact us at info@example.com or support@test.org"
        matches = EMAIL_PATTERN.findall(text)
        self.assertIn("info@example.com", matches)
        self.assertIn("support@test.org", matches)

    @patch('lead_gen.search')
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ['http://example1.com', 'http://example2.com']
        urls = search_businesses('Plumbers in London', num_results=2)
        self.assertEqual(len(urls), 2)
        self.assertEqual(urls[0], 'http://example1.com')

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Best Plumber Services in London</title></head><body>Email: contact@plumber.com</body></html>'
        mock_get.return_value = mock_response

        info = extract_info('http://plumber.com')
        self.assertEqual(info['url'], 'http://plumber.com')
        self.assertEqual(info['title'], 'Best Plumber Services in London')
        self.assertEqual(info['email'], 'contact@plumber.com')

    def test_qualify_lead(self):
        lead_info = {'url': 'http://test.com', 'email': 'test@test.com', 'title': 'A Very Long Business Title Here'}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified['ai_score'], 70)
        self.assertEqual(qualified['qualification'], 'High')

    @patch('lead_gen.extract_info')
    @patch('lead_gen.search_businesses')
    def test_generate_leads_concurrent(self, mock_search, mock_extract):
        mock_search.return_value = [f'http://example{i}.com' for i in range(5)]
        mock_extract.side_effect = lambda url, session=None: {
            'url': url,
            'email': f'info@{url.split("//")[1]}',
            'title': f'Title for {url}'
        }

        leads = generate_leads('Plumbers', 'London', num_results=5)
        self.assertEqual(len(leads), 5)
        self.assertEqual(leads[0]['url'], 'http://example0.com')
        self.assertEqual(leads[4]['url'], 'http://example4.com')

if __name__ == '__main__':
    unittest.main()
