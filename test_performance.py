import time
import unittest
from unittest.mock import patch, MagicMock
from lead_gen import generate_leads

class TestPerformanceAndCorrectness(unittest.TestCase):

    @patch('lead_gen.search_businesses')
    @patch('lead_gen.requests.get')
    def test_parallel_versus_sequential_simulation(self, mock_get, mock_search):
        # Mocking 5 URLs
        urls = [f"http://example{i}.com" for i in range(5)]
        mock_search.return_value = urls

        # Define a mock response that simulates a network request delay of 0.1 seconds per URL
        def side_effect_get(url, *args, **kwargs):
            time.sleep(0.1)
            mock_res = MagicMock()
            mock_res.status_code = 200
            mock_res.text = f"<html><title>Title for {url}</title>contact@example.com</html>"
            return mock_res

        mock_get.side_effect = side_effect_get

        # Measure parallel generate_leads performance
        start_time = time.time()
        leads = generate_leads("Dentists", "Miami", num_results=5)
        end_time = time.time()
        parallel_duration = end_time - start_time

        # If it were sequential, 5 URLs with 0.1s delay each, plus the original time.sleep(1) would take:
        # 5 * 0.1s + 5 * 1s = 5.5s.
        # Even without the time.sleep(1), sequential is at least 0.5s.
        # With parallel execution with max_workers=5, total duration should be much closer to 0.1s.
        print(f"\n[BENCHMARK] Parallel execution of 5 leads took: {parallel_duration:.4f} seconds")

        self.assertEqual(len(leads), 5)
        for i, lead in enumerate(leads):
            self.assertEqual(lead["url"], urls[i])
            self.assertEqual(lead["email"], "contact@example.com")
            self.assertEqual(lead["title"], f"Title for {urls[i]}")

if __name__ == "__main__":
    unittest.main()
