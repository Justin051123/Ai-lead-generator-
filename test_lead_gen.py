import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.get_thread_session')
    def test_generate_leads_parallel(self, mock_get_session, mock_search):
        mock_search.return_value = [
            'http://example1.com',
            'http://example2.com',
            'http://example3.com'
        ]

        mock_session = MagicMock()
        mock_response_1 = MagicMock()
        mock_response_1.status_code = 200
        mock_response_1.text = '<html><head><title>Biz 1 Long Company Name</title></head><body>Contact: info@example1.com</body></html>'

        mock_response_2 = MagicMock()
        mock_response_2.status_code = 200
        mock_response_2.text = '<html><head><title>Biz 2 Long Company Name</title></head><body>Contact: info@example2.com</body></html>'

        mock_response_3 = MagicMock()
        mock_response_3.status_code = 200
        mock_response_3.text = '<html><head><title>Biz 3 Long Company Name</title></head><body>No email here</body></html>'

        def get_mock_response(url, **kwargs):
            if 'example1' in url:
                return mock_response_1
            elif 'example2' in url:
                return mock_response_2
            else:
                return mock_response_3

        mock_session.get.side_effect = get_mock_response
        mock_get_session.return_value = mock_session

        leads = lead_gen.generate_leads('Plumbers', 'Miami', num_results=3)

        self.assertEqual(len(leads), 3)
        self.assertEqual(leads[0]['url'], 'http://example1.com')
        self.assertEqual(leads[0]['title'], 'Biz 1 Long Company Name')
        self.assertEqual(leads[0]['email'], 'info@example1.com')
        self.assertEqual(leads[0]['ai_score'], 70)

        self.assertEqual(leads[1]['url'], 'http://example2.com')
        self.assertEqual(leads[1]['title'], 'Biz 2 Long Company Name')
        self.assertEqual(leads[1]['email'], 'info@example2.com')

        self.assertEqual(leads[2]['url'], 'http://example3.com')
        self.assertEqual(leads[2]['email'], 'N/A')

if __name__ == '__main__':
    unittest.main()
