import unittest
from unittest.mock import patch, MagicMock
import time
from lead_gen import (
    EMAIL_REGEX,
    extract_info,
    qualify_lead,
    process_single_lead,
    generate_leads
)

# Mock response generator that simulates network latency
def mock_requests_get(url, *args, **kwargs):
    # Simulate a realistic network delay of 100ms
    time.sleep(0.1)

    mock_response = MagicMock()
    mock_response.status_code = 200

    if "site1" in url:
        mock_response.text = "<html><title>First Plumbing</title><body>Contact: info@firstplumbing.com or fake@img.png</body></html>"
    elif "site2" in url:
        mock_response.text = "<html><title>Second Plumbing</title><body>Reach us at contact@secondplumbing.com</body></html>"
    elif "site3" in url:
        mock_response.text = "<html><title>Third Plumbing</title><body>No emails here, call us!</body></html>"
    else:
        mock_response.text = "<html><title>Generic Site</title><body>admin@generic.com</body></html>"

    return mock_response

class TestLeadGeneratorPerformance(unittest.TestCase):

    def test_email_regex_filtering(self):
        """Test that EMAIL_REGEX finds valid emails and filters out image extensions correctly."""
        text = "Hello contact@lead.com, and check out image@test.png and logo@site.jpg"
        emails = EMAIL_REGEX.findall(text)
        self.assertIn("contact@lead.com", emails)

        # Filter logic from extract_info
        filtered_emails = [email for email in set(emails) if not email.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg'))]
        self.assertIn("contact@lead.com", filtered_emails)
        self.assertNotIn("image@test.png", filtered_emails)
        self.assertNotIn("logo@site.jpg", filtered_emails)

    @patch('requests.get', side_effect=mock_requests_get)
    def test_extract_info(self, mock_get):
        """Test the extract_info function with mocked web pages."""
        info1 = extract_info("http://site1.com")
        self.assertEqual(info1["title"], "First Plumbing")
        self.assertEqual(info1["email"], "info@firstplumbing.com")

        info3 = extract_info("http://site3.com")
        self.assertEqual(info3["title"], "Third Plumbing")
        self.assertEqual(info3["email"], "N/A")

    def test_qualify_lead(self):
        """Test qualify_lead scoring and qualification labels."""
        lead_with_email = {"title": "A Very Long Title for a Lead", "email": "info@test.com"}
        qualified_lead = qualify_lead(lead_with_email)
        self.assertEqual(qualified_lead["ai_score"], 70)  # 50 (email) + 20 (title length > 10)
        self.assertEqual(qualified_lead["qualification"], "High")

        lead_no_email = {"title": "Short", "email": "N/A"}
        qualified_lead_no_email = qualify_lead(lead_no_email)
        self.assertEqual(qualified_lead_no_email["ai_score"], 0)
        self.assertEqual(qualified_lead_no_email["qualification"], "Low")

    @patch('requests.get', side_effect=mock_requests_get)
    def test_process_single_lead(self, mock_get):
        """Test process_single_lead integrates extraction and qualification."""
        result = process_single_lead("http://site2.com")
        self.assertEqual(result["title"], "Second Plumbing")
        self.assertEqual(result["email"], "contact@secondplumbing.com")
        self.assertEqual(result["qualification"], "High")

    @patch('lead_gen.search_businesses')
    @patch('requests.get', side_effect=mock_requests_get)
    def test_benchmark_and_verification(self, mock_get, mock_search):
        """
        Benchmark performance: Compare simulated original sequential execution vs optimized parallel execution.
        """
        urls = [f"http://site{i}.com" for i in range(1, 6)]
        mock_search.return_value = urls

        # --- 1. Simulate Sequential Execution (Original Code) ---
        # The original code processed each URL, qualified it, and then called time.sleep(1).
        print("\n--- Running Simulated Sequential Lead Generation (Original) ---")
        start_seq = time.time()
        sequential_leads = []
        for url in urls:
            info = extract_info(url)
            sequential_leads.append(qualify_lead(info))
            time.sleep(1.0)  # Simulating original polite sleep
        duration_seq = time.time() - start_seq
        print(f"Sequential duration for {len(urls)} leads: {duration_seq:.4f} seconds")

        # --- 2. Run Parallel Execution (Optimized Code) ---
        print("\n--- Running Optimized Parallel Lead Generation ---")
        start_par = time.time()
        parallel_leads = generate_leads("Plumbers", "London", num_results=5)
        duration_par = time.time() - start_par
        print(f"Parallel duration for {len(urls)} leads: {duration_par:.4f} seconds")

        # Verify results are identical and order is preserved
        self.assertEqual(len(sequential_leads), len(parallel_leads))
        for seq_lead, par_lead in zip(sequential_leads, parallel_leads):
            self.assertEqual(seq_lead["url"], par_lead["url"])
            self.assertEqual(seq_lead["title"], par_lead["title"])
            self.assertEqual(seq_lead["email"], par_lead["email"])
            self.assertEqual(seq_lead["ai_score"], par_lead["ai_score"])
            self.assertEqual(seq_lead["qualification"], par_lead["qualification"])

        speedup = duration_seq / duration_par
        print(f"⚡ Bolt Performance Speedup: {speedup:.2f}x faster!")

        # Verify parallel execution is significantly faster
        # Sequential: 5 leads * (0.1s net + 1s sleep) = ~5.5s
        # Parallel: 5 leads * 0.1s net = ~0.1s - 0.2s
        self.assertLess(duration_par, duration_seq)
        self.assertGreater(speedup, 5.0)

if __name__ == '__main__':
    unittest.main()
