import unittest
from unittest.mock import patch, MagicMock
from lead_gen import extract_info, qualify_lead, generate_leads


class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Best Plumbing Services in Town</title></head><body>Contact us at info@plumbing.com</body></html>"
        mock_get.return_value = mock_response

        info = extract_info("https://example.com")
        self.assertEqual(info["url"], "https://example.com")
        self.assertEqual(info["title"], "Best Plumbing Services in Town")
        self.assertEqual(info["email"], "info@plumbing.com")

    def test_qualify_lead(self):
        lead_info = {
            "url": "https://example.com",
            "title": "Best Plumbing Services in Town",
            "email": "info@plumbing.com",
        }
        qualified = qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.process_single_lead")
    def test_generate_leads_parallel(self, mock_process, mock_search):
        mock_search.return_value = [
            "https://site1.com",
            "https://site2.com",
            "https://site3.com",
        ]
        mock_process.side_effect = lambda url: {
            "url": url,
            "email": f"contact@{url.split('//')[1]}",
            "title": "Sample Title For Business",
            "ai_score": 70,
            "qualification": "High",
        }

        leads = generate_leads("Plumbers", "London", num_results=3)

        self.assertEqual(len(leads), 3)
        self.assertEqual(leads[0]["url"], "https://site1.com")
        self.assertEqual(leads[1]["url"], "https://site2.com")
        self.assertEqual(leads[2]["url"], "https://site3.com")


if __name__ == "__main__":
    unittest.main()
