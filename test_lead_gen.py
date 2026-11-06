import unittest
from unittest.mock import MagicMock, patch
import lead_gen


class TestLeadGen(unittest.TestCase):
    def test_search_businesses_success(self):
        with patch("lead_gen.search", return_value=["https://example1.com", "https://example2.com"]):
            results = lead_gen.search_businesses("Roofers in Miami", num_results=2)
            self.assertEqual(results, ["https://example1.com", "https://example2.com"])

    def test_search_businesses_exception_handled(self):
        with patch("lead_gen.search", side_effect=Exception("API error")):
            results = lead_gen.search_businesses("Roofers in Miami", num_results=2)
            self.assertEqual(results, [])

    def test_extract_info_success(self):
        html_content = """
        <html>
            <head><title>Acme Roofing Co</title></head>
            <body>
                <p>Contact us at info@acmeroofing.com or image@acme.png</p>
            </body>
        </html>
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = html_content

        with patch("requests.get", return_value=mock_response):
            info = lead_gen.extract_info("https://acmeroofing.com")
            self.assertEqual(info["url"], "https://acmeroofing.com")
            self.assertEqual(info["title"], "Acme Roofing Co")
            self.assertEqual(info["email"], "info@acmeroofing.com")

    def test_extract_info_no_email_and_no_title(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>No details here</body></html>"

        with patch("requests.get", return_value=mock_response):
            info = lead_gen.extract_info("https://notitle.com")
            self.assertEqual(info["url"], "https://notitle.com")
            self.assertEqual(info["title"], "N/A")
            self.assertEqual(info["email"], "N/A")

    def test_extract_info_network_error(self):
        with patch("requests.get", side_effect=Exception("Connection timed out")):
            info = lead_gen.extract_info("https://error.com")
            self.assertEqual(info["url"], "https://error.com")
            self.assertEqual(info["title"], "N/A")
            self.assertEqual(info["email"], "N/A")

    def test_qualify_lead(self):
        high_lead = {"url": "https://test.com", "email": "test@test.com", "title": "A long business title"}
        qualified_high = lead_gen.qualify_lead(high_lead)
        self.assertEqual(qualified_high["ai_score"], 70)
        self.assertEqual(qualified_high["qualification"], "High")

        med_lead = {"url": "https://test.com", "email": "N/A", "title": "A long business title"}
        qualified_med = lead_gen.qualify_lead(med_lead)
        self.assertEqual(qualified_med["ai_score"], 20)
        self.assertEqual(qualified_med["qualification"], "Medium")

        low_lead = {"url": "https://test.com", "email": "N/A", "title": "Short"}
        qualified_low = lead_gen.qualify_lead(low_lead)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    def test_generate_leads_empty(self):
        with patch("lead_gen.search_businesses", return_value=[]):
            leads = lead_gen.generate_leads("niche", "location")
            self.assertEqual(leads, [])

    def test_generate_leads_preserves_order(self):
        urls = [f"https://company{i}.com" for i in range(5)]

        def mock_process_single(url):
            return {
                "url": url,
                "title": f"Title for {url}",
                "email": f"contact@{url.split('//')[1]}",
                "ai_score": 70,
                "qualification": "High",
            }

        with patch("lead_gen.search_businesses", return_value=urls):
            with patch("lead_gen.process_single_lead", side_effect=mock_process_single):
                leads = lead_gen.generate_leads("roofers", "miami", num_results=5, max_workers=3)
                self.assertEqual(len(leads), 5)
                # Verify that order of URLs is strictly preserved
                for index, lead in enumerate(leads):
                    self.assertEqual(lead["url"], urls[index])


if __name__ == "__main__":
    unittest.main()
