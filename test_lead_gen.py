import unittest
from unittest.mock import patch, MagicMock
import lead_gen


class TestLeadGen(unittest.TestCase):

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html><head><title>  Best Plumber London  </title></head><body>Contact us at info@bestplumber.com or sales@bestplumber.com</body></html>'
        mock_get.return_value = mock_response

        url = "http://bestplumber.com"
        info = lead_gen.extract_info(url)

        self.assertEqual(info["url"], url)
        self.assertEqual(info["title"], "Best Plumber London")
        self.assertIn(info["email"], ["info@bestplumber.com", "sales@bestplumber.com"])

    @patch('lead_gen.requests.get')
    def test_extract_info_error(self, mock_get):
        mock_get.side_effect = Exception("Connection error")

        url = "http://badlink.com"
        info = lead_gen.extract_info(url)

        self.assertEqual(info["url"], url)
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead(self):
        lead_info = {"url": "http://example.com", "email": "test@example.com", "title": "Great Company Title Here"}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

        lead_info_low = {"url": "http://example.com", "email": "N/A", "title": "Short"}
        qualified_low = lead_gen.qualify_lead(lead_info_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.requests.get')
    def test_generate_leads_parallel(self, mock_get, mock_search):
        urls = [f"http://example{i}.com" for i in range(5)]
        mock_search.return_value = urls

        def side_effect(url, **kwargs):
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            idx = url.replace("http://example", "").replace(".com", "")
            mock_resp.text = f"<html><head><title>Company Title {idx}</title></head><body>contact{idx}@example.com</body></html>"
            return mock_resp

        mock_get.side_effect = side_effect

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=5)

        self.assertEqual(len(leads), 5)
        # Verify ordering is preserved by executor.map
        for i, lead in enumerate(leads):
            self.assertEqual(lead["url"], f"http://example{i}.com")
            self.assertEqual(lead["email"], f"contact{i}@example.com")


if __name__ == "__main__":
    unittest.main()
