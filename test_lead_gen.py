import time
import unittest
from unittest.mock import MagicMock, patch
from lead_gen import extract_info, qualify_lead, generate_leads

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Best Plumber</title></head><body>Contact us: info@plumber.com</body></html>"
        mock_get.return_value = mock_response

        info = extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Best Plumber")
        self.assertEqual(info["email"], "info@plumber.com")

    @patch('lead_gen.requests.get')
    def test_extract_info_image_email_filter(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><title>Demo</title><body>avatar@2x.png real@example.com</body></html>"
        mock_get.return_value = mock_response

        info = extract_info("https://example.com")
        self.assertEqual(info["email"], "real@example.com")

    @patch('lead_gen.requests.get')
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection timed out")
        info = extract_info("https://error-example.com")
        self.assertEqual(info["url"], "https://error-example.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead(self):
        lead_high = qualify_lead({"url": "http://a.com", "title": "A very long title that qualifies", "email": "a@a.com"})
        self.assertEqual(lead_high["ai_score"], 70)
        self.assertEqual(lead_high["qualification"], "High")

        lead_medium = qualify_lead({"url": "http://b.com", "title": "A very long title", "email": "N/A"})
        self.assertEqual(lead_medium["ai_score"], 20)
        self.assertEqual(lead_medium["qualification"], "Medium")

        lead_low = qualify_lead({"url": "http://c.com", "title": "Short", "email": "N/A"})
        self.assertEqual(lead_low["ai_score"], 0)
        self.assertEqual(lead_low["qualification"], "Low")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.requests.get')
    def test_generate_leads_parallel_and_ordered(self, mock_get, mock_search):
        urls = [f"https://business{i}.com" for i in range(5)]
        mock_search.return_value = urls

        def mock_fetch(url, *args, **kwargs):
            time.sleep(0.05)  # simulate network delay
            res = MagicMock()
            res.status_code = 200
            res.text = f"<html><title>Title {url}</title><body>contact@{url.split('//')[1]}</body></html>"
            return res

        mock_get.side_effect = mock_fetch

        start_time = time.perf_counter()
        leads = generate_leads("Plumbers", "London", num_results=5)
        duration = time.perf_counter() - start_time

        # 5 URLs with 0.05s sequential would take at least 0.25s (plus previous 5s if time.sleep(1) was present)
        # In parallel with max_workers=5, it takes ~0.05s-0.12s
        self.assertEqual(len(leads), 5)
        self.assertLess(duration, 0.20, f"Expected concurrent execution under 0.20s, got {duration:.4f}s")

        # Verify ordering is preserved
        for i, lead in enumerate(leads):
            self.assertEqual(lead["url"], urls[i])
            self.assertEqual(lead["title"], f"Title {urls[i]}")

    @patch('lead_gen.search_businesses')
    def test_generate_leads_empty(self, mock_search):
        mock_search.return_value = []
        leads = generate_leads("Empty", "Nowhere", num_results=5)
        self.assertEqual(leads, [])

if __name__ == "__main__":
    unittest.main()
