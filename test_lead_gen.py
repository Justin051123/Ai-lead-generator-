import unittest
from unittest.mock import patch, MagicMock
import time
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <head><title> Test Business </title></head>
            <body>
                <p>Contact us at info@example.com or support@example.com</p>
                <img src="logo.png" />
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Test Business")
        self.assertIn(info["email"], ["info@example.com", "support@example.com"])

    def test_qualify_lead(self):
        lead = {"url": "https://example.com", "email": "test@example.com", "title": "A Very Good Business Name"}
        qualified = lead_gen.qualify_lead(lead)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

        lead_no_email = {"url": "https://example.com", "email": "N/A", "title": "Short"}
        qualified_no_email = lead_gen.qualify_lead(lead_no_email)
        self.assertEqual(qualified_no_email["ai_score"], 0)
        self.assertEqual(qualified_no_email["qualification"], "Low")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads_order_and_performance(self, mock_extract_info, mock_search):
        mock_search.return_value = [f"https://example{i}.com" for i in range(5)]

        def delayed_extract(url):
            time.sleep(0.1)  # Simulate network latency
            return {"url": url, "email": f"contact@{url.split('//')[1]}", "title": f"Title for {url}"}

        mock_extract_info.side_effect = delayed_extract

        start_time = time.time()
        leads = lead_gen.generate_leads("Plumbers", "London", num_results=5)
        elapsed = time.time() - start_time

        # Ensure correct order
        self.assertEqual(len(leads), 5)
        for i, lead in enumerate(leads):
            self.assertEqual(lead["url"], f"https://example{i}.com")

        print(f"\nGenerated 5 leads in {elapsed:.4f} seconds.")

if __name__ == "__main__":
    unittest.main()
