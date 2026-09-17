import unittest
from unittest.mock import patch, MagicMock
import lead_gen


class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.search')
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ['http://example1.com', 'http://example2.com']
        urls = lead_gen.search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(urls, ['http://example1.com', 'http://example2.com'])

    @patch('requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Best Plumber Services</title></head><body>Contact us: info@plumber.com</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("http://plumber.com")
        self.assertEqual(info["url"], "http://plumber.com")
        self.assertEqual(info["title"], "Best Plumber Services")
        self.assertEqual(info["email"], "info@plumber.com")

    def test_qualify_lead(self):
        lead_info = {
            "url": "http://plumber.com",
            "title": "Best Plumber Services",
            "email": "info@plumber.com"
        }
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch('lead_gen.search_businesses')
    @patch('requests.Session.get')
    def test_generate_leads_parallel(self, mock_session_get, mock_search_businesses):
        mock_search_businesses.return_value = [
            'http://example1.com',
            'http://example2.com'
        ]

        def side_effect(url, **kwargs):
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            if "example1" in url:
                mock_resp.text = "<html><head><title>Company One Title</title></head><body>contact1@example.com</body></html>"
            else:
                mock_resp.text = "<html><head><title>Company Two Title</title></head><body>contact2@example.com</body></html>"
            return mock_resp

        mock_session_get.side_effect = side_effect

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "http://example1.com")
        self.assertEqual(leads[0]["email"], "contact1@example.com")
        self.assertEqual(leads[1]["url"], "http://example2.com")
        self.assertEqual(leads[1]["email"], "contact2@example.com")


if __name__ == "__main__":
    unittest.main()
