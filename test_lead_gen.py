import unittest
from unittest.mock import patch, MagicMock
import time
from lead_gen import (
    search_businesses,
    extract_info,
    qualify_lead,
    process_single_lead,
    generate_leads
)

class TestLeadGenerator(unittest.TestCase):

    @patch('lead_gen.search')
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["http://test1.com", "http://test2.com"]
        urls = search_businesses("Dentist in NYC", num_results=2)
        self.assertEqual(urls, ["http://test1.com", "http://test2.com"])
        mock_search.assert_called_once_with("Dentist in NYC", num_results=2)

    @patch('lead_gen.requests.get')
    def test_extract_info_success_with_email(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Best Dentist</title></head><body>Contact us at contact@dentist.com or info@dentist.com</body></html>"
        mock_get.return_value = mock_response

        info = extract_info("http://dentist.com")
        self.assertEqual(info["url"], "http://dentist.com")
        self.assertEqual(info["title"], "Best Dentist")
        self.assertEqual(info["email"], "contact@dentist.com")  # Should extract first or one of them

    @patch('lead_gen.requests.get')
    def test_extract_info_success_filtering_false_positives(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Plumber</title></head><body>Image: logo@2x.png and email contact@plumber.com</body></html>"
        mock_get.return_value = mock_response

        info = extract_info("http://plumber.com")
        self.assertEqual(info["email"], "contact@plumber.com")

    @patch('lead_gen.requests.get')
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection Error")
        info = extract_info("http://bad-url.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead_high(self):
        lead_info = {"url": "http://test.com", "title": "A Very Long Page Title Indeed", "email": "info@test.com"}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    def test_qualify_lead_medium(self):
        lead_info = {"url": "http://test.com", "title": "Short", "email": "info@test.com"}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 50)
        self.assertEqual(qualified["qualification"], "Medium")

    def test_qualify_lead_low(self):
        lead_info = {"url": "http://test.com", "title": "Short", "email": "N/A"}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 0)
        self.assertEqual(qualified["qualification"], "Low")

    @patch('lead_gen.extract_info')
    def test_process_single_lead(self, mock_extract):
        mock_extract.return_value = {"url": "http://test.com", "title": "Best Plumber", "email": "info@test.com"}
        res = process_single_lead("http://test.com")
        self.assertEqual(res["ai_score"], 70)
        self.assertEqual(res["qualification"], "High")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.requests.get')
    def test_generate_leads_concurrency_and_performance(self, mock_get, mock_search):
        # We test that concurrent execution actually works and speeds up operations
        mock_search.return_value = [f"http://site{i}.com" for i in range(5)]

        # Simulate a 1-second delay for each requests.get call
        def slow_get(url, *args, **kwargs):
            time.sleep(1.0)
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.text = f"<html><head><title>Site {url}</title></head><body>info@{url.split('//')[1]}</body></html>"
            return mock_resp

        mock_get.side_effect = slow_get

        start_time = time.time()
        leads = generate_leads("Plumber", "Miami", num_results=5)
        duration = time.time() - start_time

        self.assertEqual(len(leads), 5)
        # Sequential execution with 5 sites and 1 second delay each would take >= 5 seconds.
        # With ThreadPoolExecutor and max_workers=5 (min of 10 and num_results=5), it should take around 1.0 - 1.5 seconds.
        self.assertLess(duration, 3.0)

        # Verify ordering is preserved
        for i, lead in enumerate(leads):
            self.assertEqual(lead["url"], f"http://site{i}.com")
            self.assertEqual(lead["email"], f"info@site{i}.com")

if __name__ == "__main__":
    unittest.main()
