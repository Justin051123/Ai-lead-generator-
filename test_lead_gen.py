import unittest
from unittest.mock import patch, MagicMock
from lead_gen import search_businesses, extract_info, qualify_lead, process_single_lead, generate_leads, EMAIL_PATTERN

class TestLeadGen(unittest.TestCase):

    def test_email_pattern(self):
        text = "Contact us at info@example.com or support@test.org"
        matches = EMAIL_PATTERN.findall(text)
        self.assertEqual(matches, ["info@example.com", "support@test.org"])

    @patch('lead_gen.search')
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        urls = search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(urls, ["https://example1.com", "https://example2.com"])
        mock_search.assert_called_once_with("Plumbers in London", num_results=2)

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Best Plumber Service</title></head><body>Email: contact@plumber.com</body></html>"
        mock_get.return_value = mock_response

        info = extract_info("https://plumber.com")
        self.assertEqual(info["url"], "https://plumber.com")
        self.assertEqual(info["title"], "Best Plumber Service")
        self.assertEqual(info["email"], "contact@plumber.com")

    def test_qualify_lead(self):
        lead_info = {
            "url": "https://example.com",
            "email": "test@example.com",
            "title": "A Great Business Title"
        }
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch('lead_gen.extract_info')
    def test_process_single_lead(self, mock_extract):
        mock_extract.return_value = {
            "url": "https://example.com",
            "email": "test@example.com",
            "title": "A Great Business Title"
        }
        result = process_single_lead("https://example.com")
        self.assertEqual(result["ai_score"], 70)
        self.assertEqual(result["qualification"], "High")

    @patch('lead_gen.process_single_lead')
    @patch('lead_gen.search_businesses')
    def test_generate_leads_concurrent(self, mock_search, mock_process):
        urls = ["https://site1.com", "https://site2.com", "https://site3.com"]
        mock_search.return_value = urls
        mock_process.side_effect = lambda url: {"url": url, "ai_score": 50, "qualification": "Medium"}

        leads = generate_leads("Dentists", "Miami", num_results=3)
        self.assertEqual(len(leads), 3)
        self.assertEqual([lead["url"] for lead in leads], urls)

if __name__ == '__main__':
    unittest.main()
