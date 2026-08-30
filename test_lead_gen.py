import unittest
from unittest.mock import patch
import lead_gen

class TestLeadGen(unittest.TestCase):
    def test_qualify_lead(self):
        lead_high = {"email": "test@example.com", "title": "Valid Business Title"}
        result = lead_gen.qualify_lead(lead_high)
        self.assertEqual(result["ai_score"], 70)
        self.assertEqual(result["qualification"], "High")

        lead_low = {"email": "N/A", "title": "Short"}
        result_low = lead_gen.qualify_lead(lead_low)
        self.assertEqual(result_low["ai_score"], 0)
        self.assertEqual(result_low["qualification"], "Low")

    @patch('lead_gen.requests.get')
    def test_extract_info(self, mock_get):
        mock_response = unittest.mock.MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>Test Business Page</title></head><body>Contact us at contact@testbiz.com</body></html>'
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("http://testbiz.com")
        self.assertEqual(info["url"], "http://testbiz.com")
        self.assertEqual(info["title"], "Test Business Page")
        self.assertEqual(info["email"], "contact@testbiz.com")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads_concurrent(self, mock_extract, mock_search):
        mock_search.return_value = ["http://example1.com", "http://example2.com"]
        mock_extract.side_effect = [
            {"url": "http://example1.com", "email": "info@example1.com", "title": "Example 1 Long Title"},
            {"url": "http://example2.com", "email": "N/A", "title": "Short"}
        ]
        leads = lead_gen.generate_leads("test", "loc", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "http://example1.com")
        self.assertEqual(leads[0]["ai_score"], 70)
        self.assertEqual(leads[1]["url"], "http://example2.com")
        self.assertEqual(leads[1]["ai_score"], 0)

if __name__ == "__main__":
    unittest.main()
