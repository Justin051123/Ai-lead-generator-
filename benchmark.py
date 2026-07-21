import time
from unittest.mock import patch
import lead_gen

# A mock response to simulate a webpage with title and email
class MockResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code

def mock_requests_get(url, *args, **kwargs):
    # Simulate a network latency of 0.2 seconds
    time.sleep(0.2)
    html_content = f"""
    <html>
        <head><title>Business Title {url}</title></head>
        <body>
            <p>Contact us at info@{url.split('//')[-1]} or support@{url.split('//')[-1]}.</p>
        </body>
    </html>
    """
    return MockResponse(html_content)

def mock_search(query, num_results=10):
    return [f"https://example{i}.com" for i in range(num_results)]

def run_benchmark():
    print("--- Running Benchmark ---")

    # Mock both requests.get and googlesearch.search
    with patch("requests.get", side_effect=mock_requests_get), \
         patch("lead_gen.search_businesses", side_effect=mock_search):

        start_time = time.perf_counter()
        leads = lead_gen.generate_leads("Plumbers", "London", num_results=5)
        end_time = time.perf_counter()

        elapsed = end_time - start_time
        print(f"Leads extracted: {len(leads)}")
        for lead in leads:
            print(f"- {lead['url']}: {lead['title']} (Email: {lead['email']}, AI Score: {lead['ai_score']})")
        print(f"Total processing time: {elapsed:.4f} seconds")
        return elapsed

if __name__ == "__main__":
    run_benchmark()
