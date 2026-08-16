import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):
    @patch('lead_gen.search_businesses')
    @patch('lead_gen.requests.get')
    def test_generate_leads(self, mock_get, mock_search):
        mock_search.return_value = ['http://example1.com', 'http://example2.com']

        def side_effect(url, timeout=10, headers=None):
            mock_response = MagicMock()
            mock_response.status_code = 200
            if url == 'http://example1.com':
                mock_response.text = '<html><head><title>Example 1 Business Page</title></head><body>Contact us at info@example1.com</body></html>'
            elif url == 'http://example2.com':
                mock_response.text = '<html><head><title>Example 2 Title Here</title></head><body>No email here</body></html>'
            return mock_response

        mock_get.side_effect = side_effect

        leads = lead_gen.generate_leads("test", "test", num_results=2)

        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]['url'], 'http://example1.com')
        self.assertEqual(leads[0]['email'], 'info@example1.com')
        self.assertEqual(leads[0]['title'], 'Example 1 Business Page')
        self.assertEqual(leads[0]['ai_score'], 70)

        self.assertEqual(leads[1]['url'], 'http://example2.com')
        self.assertEqual(leads[1]['email'], 'N/A')
        self.assertEqual(leads[1]['title'], 'Example 2 Title Here')
        self.assertEqual(leads[1]['ai_score'], 20)

if __name__ == '__main__':
    unittest.main()
