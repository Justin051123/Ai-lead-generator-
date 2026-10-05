import unittest
from unittest.mock import patch, MagicMock
import lead_gen

class TestLeadGen(unittest.TestCase):

    def test_qualify_lead(self):
        lead_info = {"url": "http://example.com", "email": "test@example.com", "title": "A Very Long Title For Business"}
        qualified = lead_gen.qualify_lead(lead_info)
        self.assertEqual(qualified["ai_score"], 70)
        self.assertEqual(qualified["qualification"], "High")

        lead_info_low = {"url": "http://example.com", "email": "N/A", "title": "Short"}
        qualified_low = lead_gen.qualify_lead(lead_info_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch("lead_gen.get_thread_session")
    def test_extract_info(self, mock_get_session):
        mock_sess = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = """
        <html>
            <head><title> Acme Plumbing Services </title></head>
            <body>Contact us at info@acmeplumbing.com</body>
        </html>
        """
        mock_sess.get.return_value = mock_resp
        mock_get_session.return_value = mock_sess

        info = lead_gen.extract_info("http://acmeplumbing.com")
        self.assertEqual(info["url"], "http://acmeplumbing.com")
        self.assertEqual(info["title"], "Acme Plumbing Services")
        self.assertEqual(info["email"], "info@acmeplumbing.com")

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.extract_info")
    def test_generate_leads(self, mock_extract, mock_search):
        mock_search.return_value = ["http://site1.com", "http://site2.com"]
        mock_extract.side_effect = [
            {"url": "http://site1.com", "email": "contact@site1.com", "title": "Site One Title"},
            {"url": "http://site2.com", "email": "N/A", "title": "Site Two Title Long"}
        ]

        leads = lead_gen.generate_leads("Plumbers", "Miami", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "http://site1.com")
        self.assertEqual(leads[0]["email"], "contact@site1.com")
        self.assertEqual(leads[1]["url"], "http://site2.com")

if __name__ == "__main__":
    unittest.main()
