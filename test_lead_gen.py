import unittest
from unittest.mock import patch, MagicMock
from lead_gen import (
    EMAIL_REGEX,
    extract_info,
    qualify_lead,
    process_single_lead,
    generate_leads
)

class TestLeadGen(unittest.TestCase):

    def test_email_regex_precompiled(self):
        """Test that the precompiled EMAIL_REGEX matches standard and complex emails."""
        self.assertIsNotNone(EMAIL_REGEX.match("test@example.com"))
        self.assertIsNotNone(EMAIL_REGEX.search("Contact us at contact.info_123@sub.domain.co.uk today!"))

        # Test finding all emails
        text = "Hello mail1@abc.com and mail2@xyz.org"
        matches = EMAIL_REGEX.findall(text)
        self.assertEqual(len(matches), 2)
        self.assertIn("mail1@abc.com", matches)
        self.assertIn("mail2@xyz.org", matches)

    @patch("requests.get")
    def test_extract_info_success(self, mock_get):
        """Test extract_info when request is successful."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><title>  Best Plumbers  </title><body>Email us: plumbing@test.com</body></html>"
        mock_get.return_value = mock_response

        info = extract_info("http://testplumbers.com")
        self.assertEqual(info["url"], "http://testplumbers.com")
        self.assertEqual(info["title"], "Best Plumbers")
        self.assertEqual(info["email"], "plumbing@test.com")

    @patch("requests.get")
    def test_extract_info_exclude_image_extensions(self, mock_get):
        """Test that false positive emails with image extensions are filtered out."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><title>Test Page</title><body>logo@2x.png, image@3x.jpg, hello@world.com</body></html>"
        mock_get.return_value = mock_response

        info = extract_info("http://testimages.com")
        self.assertEqual(info["email"], "hello@world.com")

    @patch("requests.get")
    def test_extract_info_failure(self, mock_get):
        """Test extract_info when request fails or returns non-200 status."""
        mock_get.side_effect = Exception("Connection Timeout")

        info = extract_info("http://bad-url.com")
        self.assertEqual(info["url"], "http://bad-url.com")
        self.assertEqual(info["title"], "N/A")
        self.assertEqual(info["email"], "N/A")

    def test_qualify_lead(self):
        """Test the AI lead qualification scoring helper."""
        lead_high = {"url": "http://test.com", "email": "test@test.com", "title": "A highly descriptive title"}
        qualified_high = qualify_lead(lead_high)
        self.assertEqual(qualified_high["ai_score"], 70)
        self.assertEqual(qualified_high["qualification"], "High")

        lead_medium = {"url": "http://test.com", "email": "test@test.com", "title": ""}
        qualified_medium = qualify_lead(lead_medium)
        self.assertEqual(qualified_medium["ai_score"], 50)
        self.assertEqual(qualified_medium["qualification"], "Medium")

        lead_low = {"url": "http://test.com", "email": "N/A", "title": ""}
        qualified_low = qualify_lead(lead_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch("requests.get")
    def test_process_single_lead(self, mock_get):
        """Test process_single_lead integrates extract_info and qualify_lead."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><title>Nice Company</title><body>info@nice.com</body></html>"
        mock_get.return_value = mock_response

        res = process_single_lead("http://nice.com")
        self.assertEqual(res["url"], "http://nice.com")
        self.assertEqual(res["title"], "Nice Company")
        self.assertEqual(res["email"], "info@nice.com")
        self.assertEqual(res["qualification"], "High")

    @patch("requests.get")
    @patch("lead_gen.search_businesses")
    def test_generate_leads_order_preserved(self, mock_search, mock_get):
        """Test that lead results preserve the exact order of returned search URLs under parallel execution."""
        mock_search.return_value = [
            "http://first.com",
            "http://second.com",
            "http://third.com"
        ]

        # Return a response corresponding to the request URL
        def side_effect_get(url, *args, **kwargs):
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            if "first" in url:
                mock_resp.text = "<title>First Page</title>"
            elif "second" in url:
                mock_resp.text = "<title>Second Page</title>"
            else:
                mock_resp.text = "<title>Third Page</title>"
            return mock_resp

        mock_get.side_effect = side_effect_get

        leads = generate_leads("Dentists", "Miami", num_results=3)
        self.assertEqual(len(leads), 3)
        self.assertEqual(leads[0]["url"], "http://first.com")
        self.assertEqual(leads[0]["title"], "First Page")
        self.assertEqual(leads[1]["url"], "http://second.com")
        self.assertEqual(leads[1]["title"], "Second Page")
        self.assertEqual(leads[2]["url"], "http://third.com")
        self.assertEqual(leads[2]["title"], "Third Page")

if __name__ == "__main__":
    unittest.main()
