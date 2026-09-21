import unittest
from unittest.mock import patch, MagicMock
from lead_gen import extract_info, qualify_lead, generate_leads

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.get_thread_session')
    def test_extract_info_success(self, mock_get_session):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test Business</title></head><body>Contact us at contact@example.com</body></html>'
        mock_session.get.return_value = mock_response
        mock_get_session.return_value = mock_session

        url = "https://example.com"
        info = extract_info(url)

        self.assertEqual(info["url"], url)
        self.assertEqual(info["title"], "Test Business")
        self.assertEqual(info["email"], "contact@example.com")

    @patch('lead_gen.get_thread_session')
    def test_extract_info_failure(self, mock_get_session):
        mock_session = MagicMock()
        mock_session.get.side_effect = Exception("Connection error")
        mock_get_session.return_value = mock_session

        url = "https://example.com"
        info = extract_info(url)

        self.assertEqual(info["url"], url)
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead(self):
        lead_info = {"url": "https://example.com", "title": "Great Plumbing Service", "email": "info@plumbing.com"}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads(self, mock_extract_info, mock_search_businesses):
        mock_search_businesses.return_value = [
            "https://site1.com",
            "https://site2.com"
        ]
        mock_extract_info.side_effect = lambda url, **kwargs: {
            "url": url,
            "title": f"Title for {url}",
            "email": f"info@{url.split('//')[1]}"
        }

        leads = generate_leads("Plumbers", "London", num_results=2)

        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[1]["url"], "https://site2.com")
        self.assertEqual(leads[0]["qualification"], "High")

if __name__ == '__main__':
    unittest.main()
