import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        urls = lead_gen.search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(len(urls), 2)
        self.assertEqual(urls[0], "https://example1.com")
        mock_search.assert_called_once_with("Plumbers in London", num_results=2)

    @patch("lead_gen.get_thread_session")
    def test_extract_info_success(self, mock_get_session):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <head><title>Acme Plumbing Co.</title></head>
            <body>Contact: info@acmeplumbing.com</body>
        </html>
        """
        mock_session.get.return_value = mock_response
        mock_get_session.return_value = mock_session

        info = lead_gen.extract_info("https://acmeplumbing.com")
        self.assertEqual(info["url"], "https://acmeplumbing.com")
        self.assertEqual(info["title"], "Acme Plumbing Co.")
        self.assertEqual(info["email"], "info@acmeplumbing.com")

    def test_qualify_lead(self):
        lead_info = {
            "url": "https://acmeplumbing.com",
            "title": "Acme Plumbing Co.",
            "email": "info@acmeplumbing.com"
        }
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads_parallel(self, mock_extract_info, mock_search_businesses):
        mock_search_businesses.return_value = [
            f"https://example{i}.com" for i in range(5)
        ]

        def fake_extract(url):
            idx = url.replace("https://example", "").replace(".com", "")
            return {
                "url": url,
                "title": f"Business {idx} Long Title",
                "email": f"contact{idx}@example.com"
            }

        mock_extract_info.side_effect = fake_extract

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=5)
        self.assertEqual(len(leads), 5)
        # Verify ordering is preserved
        for i in range(5):
            self.assertEqual(leads[i]["url"], f"https://example{i}.com")
            self.assertEqual(leads[i]["qualification"], "High")

if __name__ == "__main__":
    unittest.main()
