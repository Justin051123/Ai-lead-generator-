import unittest
from unittest.mock import patch, MagicMock
import time
from lead_gen import (
    extract_info,
    qualify_lead,
    generate_leads,
    EMAIL_PATTERN
)

class TestLeadGen(unittest.TestCase):

    def test_email_pattern(self):
        text = "Contact us at info@example.com or support@domain.co.uk"
        emails = EMAIL_PATTERN.findall(text)
        self.assertEqual(emails, ["info@example.com", "support@domain.co.uk"])

    def test_qualify_lead(self):
        lead_info = {"url": "http://example.com", "email": "test@example.com", "title": "A Great Business Title"}
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

        low_lead = {"url": "http://example.com", "email": "N/A", "title": "Short"}
        qualified_low = qualify_lead(low_lead)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch("lead_gen._get_session")
    def test_extract_info(self, mock_get_session):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Sample Business</title></head><body>Email: hello@biz.com</body></html>"

        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_get_session.return_value = mock_session

        info = extract_info("http://testbiz.com")
        self.assertEqual(info["title"], "Sample Business")
        self.assertEqual(info["email"], "hello@biz.com")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads_concurrency_and_ordering(self, mock_extract_info, mock_search):
        urls = [f"http://example{i}.com" for i in range(1, 6)]
        mock_search.return_value = urls

        def mock_extract(url):
            # Simulate latency
            time.sleep(0.05)
            return {"url": url, "email": f"contact@{url.split('//')[1]}", "title": f"Title for {url}"}

        mock_extract_info.side_effect = mock_extract

        start_time = time.time()
        leads = generate_leads("Plumbers", "London", num_results=5, max_workers=5)
        elapsed = time.time() - start_time

        # Verify order is preserved
        extracted_urls = [lead["url"] for lead in leads]
        self.assertEqual(extracted_urls, urls)

        # Elapsed time should be close to 0.05s (parallel) rather than 0.25s+ (sequential)
        self.assertLess(elapsed, 0.2)

if __name__ == "__main__":
    unittest.main()
