import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title> Best Plumbing Services Ltd </title></head><body>Contact us at contact@plumbing.com</body></html>'
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Best Plumbing Services Ltd")
        self.assertEqual(info["email"], "contact@plumbing.com")

    def test_qualify_lead(self):
        lead_info = {"title": "Best Plumbing Services Ltd", "email": "contact@plumbing.com"}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

        low_lead_info = {"title": "Short", "email": "N/A"}
        qualified_low = lead_gen.qualify_lead(low_lead_info)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads_parallel(self, mock_extract_info, mock_search):
        mock_search.return_value = [
            "https://lead1.com",
            "https://lead2.com",
            "https://lead3.com"
        ]

        def side_effect(url):
            if "lead1" in url:
                return {"url": url, "title": "Lead One Business", "email": "info@lead1.com"}
            elif "lead2" in url:
                return {"url": url, "title": "Lead Two Business", "email": "info@lead2.com"}
            else:
                return {"url": url, "title": "Lead Three Business", "email": "N/A"}

        mock_extract_info.side_effect = side_effect

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=3)

        self.assertEqual(len(leads), 3)
        self.assertEqual(leads[0]["url"], "https://lead1.com")
        self.assertEqual(leads[1]["url"], "https://lead2.com")
        self.assertEqual(leads[2]["url"], "https://lead3.com")

        self.assertEqual(leads[0]["qualification"], "High")
        self.assertEqual(leads[1]["qualification"], "High")
        self.assertEqual(leads[2]["qualification"], "Medium")


if __name__ == "__main__":
    unittest.main()
