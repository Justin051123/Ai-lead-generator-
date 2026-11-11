import unittest
from unittest.mock import patch, MagicMock
import time
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
            <html>
                <head><title>Best Plumber Miami</title></head>
                <body>
                    <p>Contact us at info@bestplumber.com or support@bestplumber.com</p>
                    <img src="logo@2x.png" />
                </body>
            </html>
        """
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Best Plumber Miami")
        self.assertIn("@bestplumber.com", info["email"])
        self.assertFalse(info["email"].endswith('.png'))

    @patch('lead_gen.requests.get')
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        info = lead_gen.extract_info("https://broken.com")
        self.assertEqual(info["url"], "https://broken.com")
        self.assertEqual(info["email"], "N/A")
        self.assertEqual(info["title"], "N/A")

    def test_qualify_lead(self):
        high_lead = {"url": "https://example.com", "title": "A Great Business Title", "email": "hello@biz.com"}
        qualified = lead_gen.qualify_lead(high_lead)
        self.assertEqual(qualified["qualification"], "High")
        self.assertEqual(qualified["ai_score"], 70)

        low_lead = {"url": "https://example.com", "title": "Short", "email": "N/A"}
        qualified_low = lead_gen.qualify_lead(low_lead)
        self.assertEqual(qualified_low["qualification"], "Low")
        self.assertEqual(qualified_low["ai_score"], 0)

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ["https://site1.com", "https://site2.com"]
        mock_extract.side_effect = [
            {"url": "https://site1.com", "title": "Site 1 Title Extra Long", "email": "a@s1.com"},
            {"url": "https://site2.com", "title": "Site 2 Title Extra Long", "email": "b@s2.com"},
        ]

        leads = lead_gen.generate_leads("Dentists", "Dallas", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[1]["url"], "https://site2.com")
        self.assertEqual(leads[0]["qualification"], "High")
        self.assertEqual(leads[1]["qualification"], "High")


class BenchmarkLeadGen(unittest.TestCase):

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.requests.get')
    def test_simulated_workload_benchmark(self, mock_get, mock_search):
        num_urls = 5
        mock_search.return_value = [f"https://site{i}.com" for i in range(num_urls)]

        def delayed_response(url, *args, **kwargs):
            time.sleep(0.05)  # Simulate 50ms network I/O
            resp = MagicMock()
            resp.status_code = 200
            resp.text = f"<html><head><title>Title for {url}</title></head><body>contact@test.com</body></html>"
            return resp

        mock_get.side_effect = delayed_response

        start_time = time.perf_counter()
        leads = lead_gen.generate_leads("Plumbers", "Austin", num_results=num_urls)
        duration = time.perf_counter() - start_time

        print(f"\n[BENCHMARK] Processed {len(leads)} leads in {duration:.3f}s")
        self.assertEqual(len(leads), num_urls)


if __name__ == "__main__":
    unittest.main()
