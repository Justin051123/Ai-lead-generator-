import unittest
from unittest.mock import MagicMock, patch
import lead_gen


class TestLeadGen(unittest.TestCase):
    def test_qualify_lead(self):
        lead_high = {"url": "https://example.com", "title": "A very long business title", "email": "test@example.com"}
        scored_high = lead_gen.qualify_lead(lead_high)
        self.assertEqual(scored_high["ai_score"], 70)
        self.assertEqual(scored_high["qualification"], "High")

        lead_medium = {"url": "https://example.com", "title": "A very long business title", "email": "N/A"}
        scored_medium = lead_gen.qualify_lead(lead_medium)
        self.assertEqual(scored_medium["ai_score"], 20)
        self.assertEqual(scored_medium["qualification"], "Medium")

        lead_low = {"url": "https://example.com", "title": "Short", "email": "N/A"}
        scored_low = lead_gen.qualify_lead(lead_low)
        self.assertEqual(scored_low["ai_score"], 0)
        self.assertEqual(scored_low["qualification"], "Low")

    @patch("lead_gen.requests.get")
    def test_extract_info(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = (
            "<html><head><title>Best Plumber Services</title></head>"
            "<body>Contact us: info@example.com or image@test.png</body></html>"
        )
        mock_get.return_value = mock_resp

        info = lead_gen.extract_info("https://plumbers.com")
        self.assertEqual(info["url"], "https://plumbers.com")
        self.assertEqual(info["title"], "Best Plumber Services")
        self.assertEqual(info["email"], "info@example.com")

    @patch("lead_gen.requests.get")
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection timeout")
        info = lead_gen.extract_info("https://timeout.com")
        self.assertEqual(info["url"], "https://timeout.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads_preserves_order_and_structure(self, mock_extract, mock_search):
        urls = [f"https://business{i}.com" for i in range(5)]
        mock_search.return_value = urls

        def fake_extract(url):
            return {
                "url": url,
                "title": f"Business Title for {url}",
                "email": f"contact@{url.split('//')[1]}",
            }

        mock_extract.side_effect = fake_extract

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=5, max_workers=3)
        self.assertEqual(len(leads), 5)
        # Verify order matches search result ranking
        for idx, lead in enumerate(leads):
            self.assertEqual(lead["url"], urls[idx])
            self.assertEqual(lead["qualification"], "High")

    @patch("lead_gen.search_businesses")
    def test_generate_leads_empty(self, mock_search):
        mock_search.return_value = []
        leads = lead_gen.generate_leads("Nowhere", "Empty", num_results=5)
        self.assertEqual(leads, [])


if __name__ == "__main__":
    unittest.main()
