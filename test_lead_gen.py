import time
import unittest
from unittest.mock import MagicMock, patch

from lead_gen import (
    EMAIL_PATTERN,
    extract_info,
    generate_leads,
    qualify_lead,
    search_businesses,
)


class TestLeadGen(unittest.TestCase):

    def test_email_regex_pattern(self):
        sample_text = "Contact us at info@example.com or support@test.co.uk. Ignore image@test.png"
        emails = EMAIL_PATTERN.findall(sample_text)
        self.assertIn("info@example.com", emails)
        self.assertIn("support@test.co.uk", emails)

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        urls = search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(urls, ["https://example1.com", "https://example2.com"])
        mock_search.assert_called_once_with("Plumbers in London", num_results=2)

    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <head><title>Best Plumbing Co</title></head>
            <body>Contact: contact@plumbing.com</body>
        </html>
        """
        mock_get.return_value = mock_response

        info = extract_info("https://plumbing.com")
        self.assertEqual(info["url"], "https://plumbing.com")
        self.assertEqual(info["title"], "Best Plumbing Co")
        self.assertEqual(info["email"], "contact@plumbing.com")

    def test_qualify_lead(self):
        lead_high = {"url": "https://a.com", "email": "a@a.com", "title": "A Very Long Business Title"}
        qualified_high = qualify_lead(lead_high)
        self.assertEqual(qualified_high["ai_score"], 70)
        self.assertEqual(qualified_high["qualification"], "High")

        lead_low = {"url": "https://b.com", "email": "N/A", "title": "Short"}
        qualified_low = qualify_lead(lead_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads_order_and_parallelism(self, mock_extract, mock_search):
        urls = [f"https://example{i}.com" for i in range(5)]
        mock_search.return_value = urls

        def mock_extract_impl(url):
            time.sleep(0.1)  # Simulate 100ms I/O delay
            idx = url.replace("https://example", "").replace(".com", "")
            return {
                "url": url,
                "email": f"user{idx}@example.com",
                "title": f"Business Title {idx} long description",
            }

        mock_extract.side_effect = mock_extract_impl

        start_time = time.time()
        leads = generate_leads("Roofers", "Miami", num_results=5)
        elapsed_time = time.time() - start_time

        # Order preservation check
        extracted_urls = [lead["url"] for lead in leads]
        self.assertEqual(extracted_urls, urls)

        # Performance check: 5 requests with 0.1s delay each would take ~0.5s sequentially,
        # but with ThreadPoolExecutor parallel execution should complete in ~0.15s
        self.assertLess(elapsed_time, 0.45)


if __name__ == "__main__":
    unittest.main()
