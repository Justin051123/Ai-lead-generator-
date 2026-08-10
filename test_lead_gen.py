import unittest
from unittest.mock import patch, MagicMock
from lead_gen import extract_info, qualify_lead, process_single_lead, generate_leads

class TestLeadGenerator(unittest.TestCase):

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        # Mock requests.get response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Business</title></head><body>Contact us at contact@testbiz.com or image@testbiz.png</body></html>"
        mock_get.return_value = mock_response

        info = extract_info("http://testbiz.com")
        self.assertEqual(info["url"], "http://testbiz.com")
        self.assertEqual(info["title"], "Test Business")
        self.assertEqual(info["email"], "contact@testbiz.com")

    @patch('lead_gen.requests.get')
    def test_extract_info_failure(self, mock_get):
        # Mock a connection error/failure
        mock_get.side_effect = Exception("Connection refused")
        info = extract_info("http://badurl.com")
        self.assertEqual(info["url"], "http://badurl.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead_high(self):
        lead_info = {"url": "http://test.com", "title": "Test Business Title With Length", "email": "test@test.com"}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    def test_qualify_lead_medium(self):
        lead_info = {"url": "http://test.com", "title": "Test Title", "email": "N/A"}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 0) # title <= 10 -> score 0
        self.assertEqual(qualified["qualification"], "Low")

        lead_info_medium = {"url": "http://test.com", "title": "Test Business Title With Length", "email": "N/A"}
        qualified_medium = qualify_lead(lead_info_medium)
        self.assertEqual(qualified_medium["ai_score"], 20)
        self.assertEqual(qualified_medium["qualification"], "Medium")

    @patch('lead_gen.extract_info')
    def test_process_single_lead(self, mock_extract):
        mock_extract.return_value = {"url": "http://test.com", "title": "A business title", "email": "info@test.com"}
        res = process_single_lead("http://test.com")
        self.assertEqual(res["url"], "http://test.com")
        self.assertEqual(res["qualification"], "High")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads_concurrency(self, mock_extract, mock_search):
        mock_search.return_value = ["http://lead1.com", "http://lead2.com"]
        mock_extract.side_effect = [
            {"url": "http://lead1.com", "title": "Lead One", "email": "lead1@test.com"},
            {"url": "http://lead2.com", "title": "Lead Two", "email": "lead2@test.com"}
        ]

        leads = generate_leads("Dentist", "Miami", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "http://lead1.com")
        self.assertEqual(leads[1]["url"], "http://lead2.com")

if __name__ == '__main__':
    unittest.main()
