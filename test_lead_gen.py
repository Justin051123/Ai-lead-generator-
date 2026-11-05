import unittest
from unittest.mock import patch, MagicMock
from lead_gen import extract_info, qualify_lead, generate_leads, EMAIL_PATTERN


class TestLeadGen(unittest.TestCase):
    def test_regex_pattern(self):
        text = "Hello contact me at test.user@example.co.uk or admin@sample.org image: icon@2x.png"
        matches = EMAIL_PATTERN.findall(text)
        self.assertIn("test.user@example.co.uk", matches)
        self.assertIn("admin@sample.org", matches)

    @patch("lead_gen.requests.get")
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>  Acme Plumbing  </title></head><body>Email: support@acme.com</body></html>"
        mock_get.return_value = mock_response

        info = extract_info("http://acme.com")
        self.assertEqual(info["url"], "http://acme.com")
        self.assertEqual(info["title"], "Acme Plumbing")
        self.assertEqual(info["email"], "support@acme.com")

    @patch("lead_gen.requests.get")
    def test_extract_info_filters_image_emails(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Photos</title></head><body>logo@2x.png test@photo.com</body></html>"
        mock_get.return_value = mock_response

        info = extract_info("http://photo.com")
        self.assertEqual(info["email"], "test@photo.com")

    @patch("lead_gen.requests.get")
    def test_extract_info_request_exception(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        info = extract_info("http://bad-url.com")
        self.assertEqual(info["url"], "http://bad-url.com")
        self.assertEqual(info["email"], "N/A")
        self.assertEqual(info["title"], "N/A")

    def test_qualify_lead(self):
        lead_high = {"email": "test@example.com", "title": "A long business title here"}
        self.assertEqual(qualify_lead(lead_high)["qualification"], "High")
        self.assertEqual(qualify_lead(lead_high)["ai_score"], 70)

        lead_medium = {"email": "N/A", "title": "A long business title here"}
        self.assertEqual(qualify_lead(lead_medium)["qualification"], "Medium")
        self.assertEqual(qualify_lead(lead_medium)["ai_score"], 20)

        lead_low = {"email": "N/A", "title": "Short"}
        self.assertEqual(qualify_lead(lead_low)["qualification"], "Low")
        self.assertEqual(qualify_lead(lead_low)["ai_score"], 0)

    @patch("lead_gen.requests.get")
    @patch("lead_gen.search_businesses")
    def test_generate_leads_parallel(self, mock_search, mock_get):
        mock_search.return_value = ["http://lead1.com", "http://lead2.com"]

        def mock_fetch(url, *args, **kwargs):
            resp = MagicMock()
            resp.status_code = 200
            name = "Lead1" if "lead1" in url else "Lead2"
            resp.text = f"<html><head><title>{name} Business</title></head><body>contact@{name.lower()}.com</body></html>"
            return resp

        mock_get.side_effect = mock_fetch

        leads = generate_leads("plumbing", "london", num_results=2)
        self.assertEqual(len(leads), 2)
        self.assertEqual(leads[0]["url"], "http://lead1.com")
        self.assertEqual(leads[0]["email"], "contact@lead1.com")
        self.assertEqual(leads[1]["url"], "http://lead2.com")
        self.assertEqual(leads[1]["email"], "contact@lead2.com")

    @patch("lead_gen.search_businesses")
    def test_generate_leads_empty(self, mock_search):
        mock_search.return_value = []
        leads = generate_leads("none", "none", num_results=5)
        self.assertEqual(leads, [])


if __name__ == "__main__":
    unittest.main()
