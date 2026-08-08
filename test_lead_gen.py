from unittest.mock import MagicMock, patch

import lead_gen


def test_search_businesses():
    with patch("lead_gen.search") as mock_search:
        mock_search.return_value = ["http://example1.com", "http://example2.com"]
        urls = lead_gen.search_businesses("Roofers in Miami", num_results=2)
        assert urls == ["http://example1.com", "http://example2.com"]
        mock_search.assert_called_once_with("Roofers in Miami", num_results=2)

def test_extract_info_success():
    with patch("lead_gen.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><head><title>Test Business</title></head><body>Contact us at contact@example.com or image@example.png</body></html>"
        mock_get.return_value = mock_response

        info = lead_gen.extract_info("http://example.com")
        assert info["url"] == "http://example.com"
        assert info["title"] == "Test Business"
        assert info["email"] == "contact@example.com"  # Filtered out .png email

def test_qualify_lead():
    lead_high = {"email": "contact@example.com", "title": "A Very Long Business Name"}
    qualified_high = lead_gen.qualify_lead(lead_high)
    assert qualified_high["ai_score"] == 70
    assert qualified_high["qualification"] == "High"

    lead_low = {"email": "N/A", "title": ""}
    qualified_low = lead_gen.qualify_lead(lead_low)
    assert qualified_low["ai_score"] == 0
    assert qualified_low["qualification"] == "Low"

def test_generate_leads():
    with patch("lead_gen.search_businesses") as mock_search, \
         patch("lead_gen.extract_info") as mock_extract:

        mock_search.return_value = ["http://example1.com", "http://example2.com"]

        # Mock extract_info for each URL
        def side_effect(url):
            if url == "http://example1.com":
                return {"url": url, "email": "info@example1.com", "title": "Example One Title"}
            return {"url": url, "email": "N/A", "title": "Example Two"}

        mock_extract.side_effect = side_effect

        leads = lead_gen.generate_leads("Roofers", "Miami", num_results=2)
        assert len(leads) == 2

        assert leads[0]["url"] == "http://example1.com"
        assert leads[0]["ai_score"] == 70
        assert leads[0]["qualification"] == "High"

        assert leads[1]["url"] == "http://example2.com"
        assert leads[1]["ai_score"] == 20
        assert leads[1]["qualification"] == "Medium"
