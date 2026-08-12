import unittest
from unittest.mock import patch, MagicMock
from lead_gen import (
    search_businesses,
    extract_info,
    qualify_lead,
    process_single_lead,
    generate_leads
)

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        # Mock googlesearch.search output
        mock_search.return_value = ["http://example1.com", "http://example2.com"]
        urls = search_businesses("Dentists in NYC", num_results=2)
        self.assertEqual(urls, ["http://example1.com", "http://example2.com"])
        mock_search.assert_called_once_with("Dentists in NYC", num_results=2)

    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get):
        # Mock requests.get response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <head><title>Best Plumbers LLC</title></head>
            <body>
                <p>Contact us at info@bestplumbers.com</p>
                <p>Fake email image: button@bestplumbers.png</p>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        info = extract_info("http://bestplumbers.com")
        self.assertEqual(info["url"], "http://bestplumbers.com")
        self.assertEqual(info["title"], "Best Plumbers LLC")
        self.assertEqual(info["email"], "info@bestplumbers.com")

    @patch("lead_gen.requests.get")
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        info = extract_info("http://badsite.com")
        self.assertEqual(info["url"], "http://badsite.com")
        self.assertEqual(info["email"], "N/A")
        self.assertEqual(info["title"], "N/A")

    def test_qualify_lead(self):
        # Case 1: High Score (Email present, Title > 10 chars)
        lead_high = {"url": "http://test.com", "email": "test@test.com", "title": "A Very Long Page Title"}
        result_high = qualify_lead(lead_high)
        self.assertEqual(result_high["ai_score"], 70)
        self.assertEqual(result_high["qualification"], "High")

        # Case 2: Medium Score (Email present, Title <= 10 chars)
        lead_med = {"url": "http://test.com", "email": "test@test.com", "title": "Short"}
        result_med = qualify_lead(lead_med)
        self.assertEqual(result_med["ai_score"], 50)
        self.assertEqual(result_med["qualification"], "Medium")

        # Case 3: Low Score (Email N/A, Title <= 10 chars)
        lead_low = {"url": "http://test.com", "email": "N/A", "title": "Short"}
        result_low = qualify_lead(lead_low)
        self.assertEqual(result_low["ai_score"], 0)
        self.assertEqual(result_low["qualification"], "Low")

    @patch("lead_gen.extract_info")
    def test_process_single_lead(self, mock_extract):
        mock_extract.return_value = {"url": "http://site.com", "email": "hello@site.com", "title": "My Company Site"}
        result = process_single_lead("http://site.com")
        self.assertEqual(result["url"], "http://site.com")
        self.assertEqual(result["email"], "hello@site.com")
        self.assertEqual(result["qualification"], "High")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.process_single_lead")
    def test_generate_leads_concurrency(self, mock_process, mock_search):
        mock_search.return_value = ["http://a.com", "http://b.com", "http://c.com"]
        mock_process.side_effect = lambda url: {"url": url, "email": "contact@test.com", "title": "Site", "ai_score": 50, "qualification": "Medium"}

        leads = generate_leads("Plumbers", "London", num_results=3)
        self.assertEqual(len(leads), 3)
        self.assertEqual(leads[0]["url"], "http://a.com")
        self.assertEqual(leads[1]["url"], "http://b.com")
        self.assertEqual(leads[2]["url"], "http://c.com")
        self.assertEqual(mock_process.call_count, 3)

if __name__ == "__main__":
    unittest.main()
