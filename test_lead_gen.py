import unittest
from unittest.mock import patch, MagicMock
from lead_gen import search_businesses, extract_info, qualify_lead, generate_leads


class TestLeadGen(unittest.TestCase):
    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example.com/1", "https://example.com/2"]
        results = search_businesses("Dentists in London", num_results=2)
        self.assertEqual(results, ["https://example.com/1", "https://example.com/2"])
        mock_search.assert_called_once_with("Dentists in London", num_results=2)

    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            "<html><head><title>Best Plumbers</title></head>"
            "<body>Contact us at contact@bestplumbers.com or ignore info@image.png</body></html>"
        )
        mock_get.return_value = mock_response

        info = extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Best Plumbers")
        self.assertEqual(info["email"], "contact@bestplumbers.com")

    @patch("lead_gen.requests.get")
    def test_extract_info_failure(self, mock_get):
        mock_get.side_effect = Exception("Connection timeout")
        info = extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["email"], "N/A")
        self.assertEqual(info["title"], "N/A")

    def test_qualify_lead(self):
        lead_high = {"url": "https://example.com", "title": "A Very Long Business Name Here", "email": "test@example.com"}
        qualified_high = qualify_lead(lead_high)
        self.assertEqual(qualified_high["ai_score"], 70)
        self.assertEqual(qualified_high["qualification"], "High")

        lead_medium = {"url": "https://example.com", "title": "Short", "email": "test@example.com"}
        qualified_medium = qualify_lead(lead_medium)
        self.assertEqual(qualified_medium["ai_score"], 50)
        self.assertEqual(qualified_medium["qualification"], "Medium")

        lead_low = {"url": "https://example.com", "title": "Short", "email": "N/A"}
        qualified_low = qualify_lead(lead_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        mock_extract.side_effect = [
            {"url": "https://example1.com", "title": "Plumber 1", "email": "p1@example.com"},
            {"url": "https://example2.com", "title": "Plumber 2", "email": "p2@example.com"},
        ]

        leads = generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://example1.com")
        self.assertEqual(leads[1]["url"], "https://example2.com")
        self.assertEqual(leads[0]["qualification"], "Medium")


if __name__ == "__main__":
    unittest.main()
