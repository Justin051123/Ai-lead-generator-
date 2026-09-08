import unittest
from unittest.mock import patch, MagicMock
from lead_gen import (
    extract_info,
    qualify_lead,
    process_single_lead,
    generate_leads,
    EMAIL_PATTERN
)


class TestLeadGen(unittest.TestCase):

    def test_email_pattern(self):
        sample_text = "Contact us at contact@example.com or support@company.org, image: logo.png"
        matches = EMAIL_PATTERN.findall(sample_text)
        self.assertIn("contact@example.com", matches)
        self.assertIn("support@company.org", matches)

    @patch('lead_gen.requests.get')
    def test_extract_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            "<html><head><title>Best Plumbing Services in Town</title></head>"
            "<body><p>Email: info@plumbingbest.com</p></body></html>"
        )
        mock_get.return_value = mock_response

        url = "http://plumbingbest.com"
        info = extract_info(url)

        self.assertEqual(info["url"], url)
        self.assertEqual(info["title"], "Best Plumbing Services in Town")
        self.assertEqual(info["email"], "info@plumbingbest.com")

    @patch('lead_gen.requests.get')
    def test_extract_info_filters_images(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = (
            "<html><head><title>Test Page</title></head>"
            "<body><p>Image link: avatar.png@2x.png and contact: real@domain.com</p></body></html>"
        )
        mock_get.return_value = mock_response

        info = extract_info("http://example.com")
        self.assertEqual(info["email"], "real@domain.com")

    @patch('lead_gen.requests.get')
    def test_extract_info_handles_exception(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        info = extract_info("http://invalid-url.local")
        self.assertEqual(info["url"], "http://invalid-url.local")
        self.assertEqual(info["email"], "N/A")
        self.assertEqual(info["title"], "N/A")

    def test_qualify_lead(self):
        lead_info_high = {"url": "http://example.com", "email": "test@example.com", "title": "A long descriptive title"}
        qualified_high = qualify_lead(lead_info_high)
        self.assertEqual(qualified_high["ai_score"], 70)
        self.assertEqual(qualified_high["qualification"], "High")

        lead_info_low = {"url": "http://example.com", "email": "N/A", "title": "Short"}
        qualified_low = qualify_lead(lead_info_low)
        self.assertEqual(qualified_low["ai_score"], 0)
        self.assertEqual(qualified_low["qualification"], "Low")

    @patch('lead_gen.extract_info')
    def test_process_single_lead(self, mock_extract):
        mock_extract.return_value = {"url": "http://example.com", "email": "hello@test.com", "title": "Great Company Page"}
        lead = process_single_lead("http://example.com")
        self.assertEqual(lead["email"], "hello@test.com")
        self.assertEqual(lead["qualification"], "High")

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.extract_info')
    def test_generate_leads_concurrent(self, mock_extract, mock_search):
        mock_search.return_value = ["http://lead1.com", "http://lead2.com", "http://lead3.com"]
        mock_extract.side_effect = lambda url: {
            "url": url,
            "email": f"contact@{url.split('//')[1]}",
            "title": f"Title for {url}"
        }

        leads = generate_leads("Plumbers", "Miami", num_results=3)

        self.assertEqual(len(leads), 3)
        self.assertEqual(leads[0]["url"], "http://lead1.com")
        self.assertEqual(leads[1]["url"], "http://lead2.com")
        self.assertEqual(leads[2]["url"], "http://lead3.com")
        self.assertEqual(leads[0]["email"], "contact@lead1.com")
        self.assertEqual(leads[1]["email"], "contact@lead2.com")
        self.assertEqual(leads[2]["email"], "contact@lead3.com")

    @patch('lead_gen.search_businesses')
    def test_generate_leads_empty_urls(self, mock_search):
        mock_search.return_value = []
        leads = generate_leads("Unknown", "Nowhere", num_results=5)
        self.assertEqual(leads, [])


if __name__ == "__main__":
    unittest.main()
