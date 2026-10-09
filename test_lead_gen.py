import unittest
from unittest.mock import patch, MagicMock
import lead_gen


class TestLeadGen(unittest.TestCase):

    @patch("lead_gen.search_businesses")
    @patch("lead_gen.get_thread_session")
    def test_generate_leads_concurrent(self, mock_get_session, mock_search):
        mock_search.return_value = [
            "http://example1.com",
            "http://example2.com",
            "http://example3.com",
        ]

        mock_session = MagicMock()
        mock_get_session.return_value = mock_session

        def mock_get(url, **kwargs):
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            if "example1" in url:
                mock_resp.text = "<html><head><title>Plumber One Services</title></head><body>Email: contact@plumber1.com</body></html>"
            elif "example2" in url:
                mock_resp.text = "<html><head><title>Plumber Two Solutions</title></head><body>No email here</body></html>"
            else:
                mock_resp.text = "<html><head><title>Short</title></head><body>Email: sales@plumber3.com <img src='logo.png'/></body></html>"
            return mock_resp

        mock_session.get.side_effect = mock_get

        leads = lead_gen.generate_leads("Plumbers", "London", num_results=3)

        self.assertEqual(len(leads), 3)

        # Check order preservation and correctness
        self.assertEqual(leads[0]["url"], "http://example1.com")
        self.assertEqual(leads[0]["title"], "Plumber One Services")
        self.assertEqual(leads[0]["email"], "contact@plumber1.com")
        self.assertEqual(leads[0]["ai_score"], 70)
        self.assertEqual(leads[0]["qualification"], "High")

        self.assertEqual(leads[1]["url"], "http://example2.com")
        self.assertEqual(leads[1]["title"], "Plumber Two Solutions")
        self.assertEqual(leads[1]["email"], "N/A")
        self.assertEqual(leads[1]["ai_score"], 20)
        self.assertEqual(leads[1]["qualification"], "Medium")

        self.assertEqual(leads[2]["url"], "http://example3.com")
        self.assertEqual(leads[2]["title"], "Short")
        self.assertEqual(leads[2]["email"], "sales@plumber3.com")
        self.assertEqual(leads[2]["ai_score"], 50)
        self.assertEqual(leads[2]["qualification"], "Medium")

    def test_extract_info_no_email_or_title(self):
        with patch("lead_gen.get_thread_session") as mock_get_session:
            mock_session = MagicMock()
            mock_get_session.return_value = mock_session
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.text = "<html><body>No title or email</body></html>"
            mock_session.get.return_value = mock_resp

            info = lead_gen.extract_info("http://example.com")
            self.assertEqual(info["email"], "N/A")
            self.assertEqual(info["title"], "N/A")


if __name__ == "__main__":
    unittest.main()
