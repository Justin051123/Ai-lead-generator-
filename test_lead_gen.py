import unittest
from unittest.mock import patch, MagicMock
from lead_gen import search_businesses, extract_info, qualify_lead, generate_leads

class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search")
    def test_search_businesses(self, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        results = search_businesses("Plumbers in London", num_results=2)
        self.assertEqual(results, ["https://example1.com", "https://example2.com"])
        mock_search.assert_called_once_with("Plumbers in London", num_results=2)

    @patch("lead_gen.get_thread_session")
    def test_extract_info_success(self, mock_get_session):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <head><title>Best Plumber Service</title></head>
            <body>
                <p>Contact us at contact@plumber.com for details.</p>
                <img src="logo.png" />
            </body>
        </html>
        """
        mock_session.get.return_value = mock_response
        mock_get_session.return_value = mock_session

        info = extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Best Plumber Service")
        self.assertEqual(info["email"], "contact@plumber.com")

    def test_qualify_lead(self):
        info_high = {"url": "https://example.com", "title": "Best Plumber Service", "email": "contact@plumber.com"}
        qualified_high = qualify_lead(info_high)
        self.assertEqual(qualified_high["ai_score"], 70)
        self.assertEqual(qualified_high["qualification"], "High")

        info_low = {"url": "https://example.com", "title": "Short", "email": "N/A"}
        qualified_low = qualify_lead(info_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ["https://example1.com", "https://example2.com"]
        mock_extract.side_effect = [
            {"url": "https://example1.com", "title": "Plumber 1 Title Long", "email": "p1@example.com"},
            {"url": "https://example2.com", "title": "Plumber 2 Title Long", "email": "p2@example.com"}
        ]

        leads = generate_leads("Plumbers", "London", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "https://example1.com")
        self.assertEqual(leads[0]["qualification"], "High")
        self.assertEqual(leads[1]["url"], "https://example2.com")
        self.assertEqual(leads[1]["qualification"], "High")

if __name__ == "__main__":
    unittest.main()
