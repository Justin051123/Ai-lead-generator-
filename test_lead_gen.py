import unittest
from unittest.mock import patch, MagicMock
import lead_gen


class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            "<html><head><title>Best Plumbers</title></head>"
            "<body>Contact us at contact@plumbingcompany.com</body></html>"
        )
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("http://example.com")
        self.assertEqual(info["url"], "http://example.com")
        self.assertEqual(info["title"], "Best Plumbers")
        self.assertEqual(info["email"], "contact@plumbingcompany.com")

    @patch("lead_gen.requests.get")
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection error")

        info = lead_gen.extract_info("http://example-fail.com")
        self.assertEqual(info["url"], "http://example-fail.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead(self):
        lead_info = {
            "url": "http://example.com",
            "title": "A Very Long Title For Plumbers Service",
            "email": "info@example.com",
        }
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

        low_lead = {
            "url": "http://example2.com",
            "title": "Short",
            "email": "N/A",
        }
        qualified_low = lead_gen.qualify_lead(low_lead)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads_concurrent(self, mock_extract, mock_search):
        urls = [
            "http://biz1.com",
            "http://biz2.com",
            "http://biz3.com",
        ]
        mock_search.return_value = urls

        def fake_extract(url):
            idx = urls.index(url) + 1
            return {
                "url": url,
                "title": f"Business Title {idx}",
                "email": f"info@biz{idx}.com",
            }

        mock_extract.side_effect = fake_extract

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=3)

        self.assertEqual(len(leads), 3)
        self.assertEqual(leads[0]["url"], "http://biz1.com")
        self.assertEqual(leads[1]["url"], "http://biz2.com")
        self.assertEqual(leads[2]["url"], "http://biz3.com")
        self.assertEqual(mock_extract.call_count, 3)


if __name__ == "__main__":
    unittest.main()
