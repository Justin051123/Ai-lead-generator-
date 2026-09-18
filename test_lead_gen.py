import unittest
from unittest.mock import patch, MagicMock
from lead_gen import search_businesses, extract_info, qualify_lead, generate_leads

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.search')
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ['https://example1.com', 'https://example2.com']
        urls = search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(urls, ['https://example1.com', 'https://example2.com'])
        mock_search.assert_called_once_with("Plumbers in London", num_results=2)

    @patch('lead_gen.requests.get')
    def test_extract_info(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test Business</title></head><body>Contact us at contact@testbusiness.com or info.png</body></html>'
        mock_get.return_value = mock_response

        info = extract_info('https://testbusiness.com')
        self.assertEqual(info['url'], 'https://testbusiness.com')
        self.assertEqual(info['title'], 'Test Business')
        self.assertEqual(info['email'], 'contact@testbusiness.com')

    def test_qualify_lead(self):
        lead_high = {'url': 'https://a.com', 'email': 'contact@a.com', 'title': 'Long Enough Title'}
        qualified_high = qualify_lead(lead_high.copy())
        self.assertEqual(qualified_high['ai_score'], 70)
        self.assertEqual(qualified_high['qualification'], 'High')

        lead_medium = {'url': 'https://b.com', 'email': 'N/A', 'title': 'Long Enough Title'}
        qualified_medium = qualify_lead(lead_medium.copy())
        self.assertEqual(qualified_medium['ai_score'], 20)
        self.assertEqual(qualified_medium['qualification'], 'Medium')

        lead_low = {'url': 'https://c.com', 'email': 'N/A', 'title': 'Short'}
        qualified_low = qualify_lead(lead_low.copy())
        self.assertEqual(qualified_low['ai_score'], 0)
        self.assertEqual(qualified_low['qualification'], 'Low')

    @patch('lead_gen.extract_info')
    @patch('lead_gen.search_businesses')
    def test_generate_leads(self, mock_search_businesses, mock_extract_info):
        mock_search_businesses.return_value = ['https://site1.com', 'https://site2.com']
        mock_extract_info.side_effect = [
            {'url': 'https://site1.com', 'email': 'a@site1.com', 'title': 'Site 1 Business'},
            {'url': 'https://site2.com', 'email': 'N/A', 'title': 'Site 2 Business'}
        ]

        leads = generate_leads('Plumbers', 'London', num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]['url'], 'https://site1.com')
        self.assertEqual(leads[0]['ai_score'], 70)
        self.assertEqual(leads[1]['url'], 'https://site2.com')
        self.assertEqual(leads[1]['ai_score'], 20)

if __name__ == '__main__':
    unittest.main()
