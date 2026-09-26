import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):
    def test_qualify_lead(self):
        lead_info = {"title": "A Very Long Business Title", "email": "test@example.com"}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

    def test_extract_info(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Title</title></head><body>info@domain.com</body></html>"

        mock_session = MagicMock()
        mock_session.get.return_value = mock_response

        with patch("lead_gen.get_thread_session", return_value=mock_session):
            info = lead_gen.extract_info("http://domain.com")
            self.assertEqual(info["title"], "Test Title")
            self.assertEqual(info["email"], "info@domain.com")

    def test_process_single_lead(self):
        mock_info = {"url": "http://domain.com", "email": "info@domain.com", "title": "Long Business Title Here"}
        with patch("lead_gen.extract_info", return_value=mock_info):
            lead = lead_gen.process_single_lead("http://domain.com")
            self.assertEqual(lead["ai_score"], 70)
            self.assertEqual(lead["qualification"], "High")

    def test_generate_leads_order_preserved(self):
        urls = ["http://a.com", "http://b.com", "http://c.com"]
        def mock_process(url):
            return {"url": url, "title": f"Title {url}", "email": "a@b.com", "ai_score": 70, "qualification": "High"}

        with patch("lead_gen.search_businesses", return_value=urls), \
             patch("lead_gen.process_single_lead", side_effect=mock_process):
            leads = lead_gen.generate_leads("Plumbers", "London", num_results=3)
            self.assertEqual(len(leads), 3)
            self.assertEqual([lead["url"] for lead in leads], urls)

if __name__ == "__main__":
    unittest.main()
