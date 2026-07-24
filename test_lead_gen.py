import unittest
from unittest.mock import patch
import lead_gen

class TestLeadGen(unittest.TestCase):
    def test_qualify_lead(self):
        # High lead
        lead = {"url": "http://test.com", "email": "test@test.com", "title": "A Very Long Title For Business"}
        qualified = lead_gen.qualify_lead(lead)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

        # Medium lead
        lead_med = {"url": "http://test.com", "email": "test@test.com", "title": ""}
        qualified_med = lead_gen.qualify_lead(lead_med)
        self.assertEqual(qualified_med["ai_score"], 50)
        self.assertEqual(qualified_med["qualification"], "Medium")

        # Low lead
        lead_low = {"url": "http://test.com", "email": "N/A", "title": ""}
        qualified_low = lead_gen.qualify_lead(lead_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch('requests.get')
    def test_extract_info_success(self, mock_get):
        # Mock HTML response
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.text = "<html><title>My Plumbing Business</title><body>Contact us at: hello@plumbing.co.uk</body></html>"

        info = lead_gen.extract_info("http://plumbing.co.uk")
        self.assertEqual(info["url"], "http://plumbing.co.uk")
        self.assertEqual(info["title"], "My Plumbing Business")
        self.assertEqual(info["email"], "hello@plumbing.co.uk")

    @patch('requests.get')
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection timed out")
        info = lead_gen.extract_info("http://unreachable.com")
        self.assertEqual(info["url"], "http://unreachable.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    @patch('lead_gen.search_businesses')
    @patch('requests.get')
    def test_generate_leads_parallel(self, mock_get, mock_search):
        # Mock Search returning 3 URLs
        mock_search.return_value = ["http://u1.com", "http://u2.com", "http://u3.com"]

        # Mock Get responses
        mock_resp = mock_get.return_value
        mock_resp.status_code = 200
        mock_resp.text = "<html><title>Plumber Business</title>office@u1.com</html>"

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=3)
        self.assertEqual(len(leads), 3)
        self.assertEqual(leads[0]["email"], "office@u1.com")
        self.assertEqual(leads[0]["title"], "Plumber Business")

if __name__ == '__main__':
    unittest.main()
