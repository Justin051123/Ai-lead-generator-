import unittest
from unittest.mock import patch, MagicMock
from lead_gen import extract_info, qualify_lead, generate_leads

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        # Mock successful response with standard HTML
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Title</title></head><body>Contact us at contact@test.com and test.png</body></html>"
        mock_get.return_value = mock_response

        info = extract_info("http://test.com")
        self.assertEqual(info["title"], "Test Title")
        self.assertEqual(info["email"], "contact@test.com")

    @patch('lead_gen.requests.get')
    def test_extract_info_no_email(self, mock_get):
        # Mock response without emails
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Title No Email</title></head><body>No emails here!</body></html>"
        mock_get.return_value = mock_response

        info = extract_info("http://testnoemail.com")
        self.assertEqual(info["title"], "Test Title No Email")
        self.assertEqual(info["email"], "N/A")

    @patch('lead_gen.requests.get')
    def test_extract_info_failure(self, mock_get):
        # Mock failing request
        mock_get.side_effect = Exception("Connection error")

        info = extract_info("http://badurl.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead_high(self):
        lead_info = {"url": "http://test.com", "email": "test@test.com", "title": "A Very Long Title indeed"}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    def test_qualify_lead_medium(self):
        lead_info = {"url": "http://test.com", "email": "N/A", "title": "A Very Long Title"}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 20)
        self.assertEqual(qualified["qualification"], "Medium")

    def test_qualify_lead_low(self):
        lead_info = {"url": "http://test.com", "email": "N/A", "title": "Short"}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 0)
        self.assertEqual(qualified["qualification"], "Low")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads_parallel(self, mock_extract, mock_search):
        mock_search.return_value = ["http://site1.com", "http://site2.com"]
        mock_extract.side_effect = [
            {"url": "http://site1.com", "email": "contact1@site1.com", "title": "Site One Super Title"},
            {"url": "http://site2.com", "email": "N/A", "title": "Site Two Super Title"}
        ]

        leads = generate_leads("niche", "location", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "http://site1.com")
        self.assertEqual(leads[1]["url"], "http://site2.com")
        self.assertEqual(leads[0]["qualification"], "High")
        self.assertEqual(leads[1]["qualification"], "Medium")

if __name__ == '__main__':
    unittest.main()
