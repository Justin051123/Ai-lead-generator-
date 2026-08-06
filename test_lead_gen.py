import unittest
from unittest.mock import patch, MagicMock
from lead_gen import extract_info, qualify_lead, generate_leads

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Best Plumber</title></head><body>Contact us at contact@bestplumber.com</body></html>"
        mock_get.return_value = mock_response

        info = extract_info("http://example.com")
        self.assertEqual(info["url"], "http://example.com")
        self.assertEqual(info["title"], "Best Plumber")
        self.assertEqual(info["email"], "contact@bestplumber.com")

    @patch('lead_gen.requests.get')
    def test_extract_info_failure(self, mock_get):
        # Mock failed response or network error
        mock_get.side_effect = Exception("Network down")

        info = extract_info("http://example.com")
        self.assertEqual(info["url"], "http://example.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead(self):
        lead_info_high = {"url": "http://example.com", "title": "Plumber London", "email": "info@example.com"}
        qualified_high = qualify_lead(lead_info_high)
        self.assertEqual(qualified_high["ai_score"], 70)
        self.assertEqual(qualified_high["qualification"], "High")

        lead_info_medium = {"url": "http://example.com", "title": "Short", "email": "info@example.com"}
        qualified_medium = qualify_lead(lead_info_medium)
        self.assertEqual(qualified_medium["ai_score"], 50)
        self.assertEqual(qualified_medium["qualification"], "Medium")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads_parallel(self, mock_extract, mock_search):
        # Mock search results returning 3 URLs
        mock_search.return_value = ["http://site1.com", "http://site2.com", "http://site3.com"]

        # Mock extracting info
        def mock_extract_side_effect(url):
            if url == "http://site1.com":
                return {"url": url, "title": "Site One Title", "email": "one@site.com"}
            elif url == "http://site2.com":
                return {"url": url, "title": "Site Two Title", "email": "two@site.com"}
            else:
                return {"url": url, "title": "Site Three Title", "email": "N/A"}
        mock_extract.side_effect = mock_extract_side_effect

        leads = generate_leads("Plumbers", "London", num_results=3)
        self.assertEqual(len(leads), 3)
        self.assertEqual(leads[0]["url"], "http://site1.com")
        self.assertEqual(leads[0]["qualification"], "High")
        self.assertEqual(leads[1]["url"], "http://site2.com")
        self.assertEqual(leads[1]["qualification"], "High")
        self.assertEqual(leads[2]["url"], "http://site3.com")
        self.assertEqual(leads[2]["qualification"], "Medium")

if __name__ == '__main__':
    unittest.main()
