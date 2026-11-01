import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.search')
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        urls = lead_gen.search_businesses("plumbers in London", num_results=2)
        self.assertEqual(urls, ["https://example1.com", "https://example2.com"])
        mock_search.assert_called_once_with("plumbers in London", num_results=2)

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Acme Plumbing</title></head><body>Contact us: info@acme.com and logo.png</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://acme.com")
        self.assertEqual(info["url"], "https://acme.com")
        self.assertEqual(info["title"], "Acme Plumbing")
        self.assertEqual(info["email"], "info@acme.com")

    @patch('lead_gen.requests.get')
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection timeout")
        info = lead_gen.extract_info("https://bad-url.com")
        self.assertEqual(info["url"], "https://bad-url.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead(self):
        lead_high = {"url": "https://a.com", "email": "a@a.com", "title": "A Very Long Business Name"}
        res_high = lead_gen.qualify_lead(lead_high)
        self.assertEqual(res_high["ai_score"], 70)
        self.assertEqual(res_high["qualification"], "High")

        lead_med = {"url": "https://b.com", "email": "N/A", "title": "A Very Long Business Name"}
        res_med = lead_gen.qualify_lead(lead_med)
        self.assertEqual(res_med["ai_score"], 20)
        self.assertEqual(res_med["qualification"], "Medium")

        lead_low = {"url": "https://c.com", "email": "N/A", "title": "Short"}
        res_low = lead_gen.qualify_lead(lead_low)
        self.assertEqual(res_low["ai_score"], 0)
        self.assertEqual(res_low["qualification"], "Low")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ["https://site1.com", "https://site2.com"]
        mock_extract.side_effect = [
            {"url": "https://site1.com", "email": "contact@site1.com", "title": "Site 1 Business"},
            {"url": "https://site2.com", "email": "contact@site2.com", "title": "Site 2 Business"},
        ]

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[0]["qualification"], "High")
        self.assertEqual(leads[1]["url"], "https://site2.com")
        self.assertEqual(leads[1]["qualification"], "High")

if __name__ == "__main__":
    unittest.main()
