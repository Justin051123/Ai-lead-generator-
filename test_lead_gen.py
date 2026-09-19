import unittest
from unittest.mock import MagicMock, patch
import lead_gen


class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["http://example1.com", "http://example2.com"]
        urls = lead_gen.search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(urls, ["http://example1.com", "http://example2.com"])
        mock_search.assert_called_once_with("Plumbers in London", num_results=2)

    @patch("requests.Session")
    def test_extract_info_success(self, mock_session_cls):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Business - Plumbing Services</title></head><body>Contact us at info@testbusiness.com</body></html>"
        mock_session.get.return_value = mock_response

        info = lead_gen.extract_info("http://example.com", session=mock_session)
        self.assertEqual(info["url"], "http://example.com")
        self.assertEqual(info["title"], "Test Business - Plumbing Services")
        self.assertEqual(info["email"], "info@testbusiness.com")

    @patch("requests.Session")
    def test_extract_info_filters_images(self, mock_session_cls):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test</title></head><body><img src='logo@2x.png'>contact@business.org</body></html>"
        mock_session.get.return_value = mock_response

        info = lead_gen.extract_info("http://example.com", session=mock_session)
        self.assertEqual(info["email"], "contact@business.org")

    def test_qualify_lead(self):
        info_high = {"url": "http://a.com", "email": "a@a.com", "title": "A Very Long Business Title Here"}
        qualified = lead_gen.qualify_lead(info_high)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

        info_low = {"url": "http://b.com", "email": "N/A", "title": "Short"}
        qualified_low = lead_gen.qualify_lead(info_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads_parallel_and_ordering(self, mock_extract, mock_search):
        mock_search.return_value = [f"http://example{i}.com" for i in range(5)]

        def side_effect(url, session=None):
            idx = url.replace("http://example", "").replace(".com", "")
            return {"url": url, "email": f"user{idx}@example.com", "title": f"Business Title Number {idx}"}

        mock_extract.side_effect = side_effect

        leads = lead_gen.generate_leads("Dentists", "NYC", num_results=5)
        self.assertEqual(len(leads), 5)
        # Verify order is preserved
        for i, lead in enumerate(leads):
            self.assertEqual(lead["url"], f"http://example{i}.com")
            self.assertEqual(lead["email"], f"user{i}@example.com")
            self.assertEqual(lead["qualification"], "High")


if __name__ == "__main__":
    unittest.main()
