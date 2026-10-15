import unittest
from unittest.mock import patch, MagicMock
from lead_gen import search_businesses, extract_info, qualify_lead, generate_leads

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.search')
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        urls = search_businesses("Plumbers", num_results=2)
        self.assertEqual(urls, ["https://example1.com", "https://example2.com"])

    @patch('lead_gen.get_thread_session')
    def test_extract_info_success(self, mock_get_session):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Plumber</title></head><body>Contact us at info@example.com</body></html>"
        mock_session.get.return_value = mock_response
        mock_get_session.return_value = mock_session

        info = extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Test Plumber")
        self.assertEqual(info["email"], "info@example.com")

    def test_qualify_lead(self):
        lead_info = {
            "url": "https://example.com",
            "email": "info@example.com",
            "title": "A Great Plumbing Service Company"
        }
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.process_single_lead')
    def test_generate_leads(self, mock_process, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        mock_process.side_effect = lambda url: {
            "url": url,
            "email": f"contact@{url.split('//')[1]}",
            "title": "Business Title Example",
            "ai_score": 70,
            "qualification": "High"
        }

        leads = generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://example1.com")
        self.assertEqual(leads[1]["url"], "https://example2.com")

if __name__ == "__main__":
    unittest.main()
