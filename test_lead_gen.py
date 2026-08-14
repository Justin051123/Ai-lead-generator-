import unittest
from unittest.mock import patch, MagicMock
import time

import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.search')
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["http://example1.com", "http://example2.com"]
        urls = lead_gen.search_businesses("Plumbers London", num_results=2)
        self.assertEqual(urls, ["http://example1.com", "http://example2.com"])
        mock_search.assert_called_once_with("Plumbers London", num_results=2)

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><title>Test Plumber</title><body>Contact us at info@testplumber.com or image@testplumber.png</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("http://testplumber.com")
        self.assertEqual(info["url"], "http://testplumber.com")
        self.assertEqual(info["title"], "Test Plumber")
        self.assertEqual(info["email"], "info@testplumber.com")

    @patch('lead_gen.requests.get')
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        info = lead_gen.extract_info("http://bad-url.com")
        self.assertEqual(info["url"], "http://bad-url.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead_high(self):
        lead_info = {"url": "http://test.com", "email": "info@test.com", "title": "A Very Long Page Title"}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    def test_qualify_lead_low(self):
        lead_info = {"url": "http://test.com", "email": "N/A", "title": "Short"}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 0)
        self.assertEqual(qualified["qualification"], "Low")

    @patch('lead_gen.search')
    @patch('lead_gen.requests.get')
    def test_generate_leads_end_to_end(self, mock_get, mock_search):
        mock_search.return_value = ["http://lead1.com", "http://lead2.com"]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><title>Lead Company</title><body>info@lead.com</body></html>"
        mock_get.return_value = mock_response

        with patch('time.sleep') as mock_sleep:
            leads = lead_gen.generate_leads("Plumbers", "London", num_results=2)
            self.assertEqual(len(leads), 2)
            self.assertEqual(leads[0]["url"], "http://lead1.com")
            self.assertEqual(leads[0]["email"], "info@lead.com")
            self.assertEqual(leads[0]["title"], "Lead Company")
            # In the parallelized version, we have completely removed sequential sleeping.
            # Thus, time.sleep should not be called at all.
            self.assertEqual(mock_sleep.call_count, 0)

def run_performance_benchmark():
    print("\n--- Running Performance Benchmark ---")
    urls = [f"http://example-{index}.com" for index in range(5)]

    def mock_get(url, *args, **kwargs):
        time.sleep(0.1)
        response = MagicMock()
        response.status_code = 200
        response.text = f"<html><title>Page {url}</title><body>contact@{url.split('//')[1]}</body></html>"
        return response

    with patch('lead_gen.search', return_value=urls), \
         patch('lead_gen.requests.get', side_effect=mock_get):

        start_time = time.perf_counter()
        leads = lead_gen.generate_leads("Niche", "Location", num_results=5)
        duration = time.perf_counter() - start_time

        print(f"Processed {len(leads)} leads in {duration:.4f} seconds.")
        return duration

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "benchmark":
        run_performance_benchmark()
    else:
        unittest.main()
