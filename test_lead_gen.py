import unittest
from unittest.mock import patch, MagicMock
from lead_gen import qualify_lead, process_single_lead


class TestLeadGen(unittest.TestCase):
    def test_qualify_lead_high(self):
        lead = {
            "url": "http://example.com",
            "email": "test@example.com",
            "title": "A Very Long Page Title",
        }
        qualified = qualify_lead(lead)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    def test_qualify_lead_medium(self):
        lead = {
            "url": "http://example.com",
            "email": "test@example.com",
            "title": "Short",
        }
        qualified = qualify_lead(lead)
        self.assertEqual(qualified["ai_score"], 50)
        self.assertEqual(qualified["qualification"], "Medium")

    def test_qualify_lead_low(self):
        lead = {"url": "http://example.com", "email": "N/A", "title": "Short"}
        qualified = qualify_lead(lead)
        self.assertEqual(qualified["ai_score"], 0)
        self.assertEqual(qualified["qualification"], "Low")

    @patch("requests.get")
    def test_process_single_lead(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Best Plumbers</title></head><body>Contact us: info@bestplumbers.com</body></html>"
        mock_get.return_value = mock_response

        lead = process_single_lead("http://bestplumbers.com")
        self.assertEqual(lead["title"], "Best Plumbers")
        self.assertEqual(lead["email"], "info@bestplumbers.com")
        self.assertEqual(lead["ai_score"], 70)
        self.assertEqual(lead["qualification"], "High")


if __name__ == "__main__":
    unittest.main()
