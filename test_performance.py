import time
from unittest.mock import patch
from lead_gen import generate_leads

# Simulated list of URLs
MOCK_URLS = [
    f"http://example{i}.com" for i in range(5)
]

def mock_extract_info(url):
    # Simulate a network/scraping latency of 1 second per request
    time.sleep(1)
    return {"url": url, "email": f"contact@{url.split('//')[1]}", "title": f"Title of {url}"}

@patch('lead_gen.search_businesses')
@patch('lead_gen.extract_info')
def run_benchmark(mock_extract, mock_search):
    mock_search.return_value = MOCK_URLS
    mock_extract.side_effect = mock_extract_info

    # Time parallel lead generation (the optimized function)
    start_time = time.time()
    generate_leads("Test", "Benchmark", num_results=5)
    end_time = time.time()
    parallel_duration = end_time - start_time

    # Simulate how much time sequential would take with the 1s sleep + 1s request latency:
    # 5 leads * (1s requests.get + 1s time.sleep(1) sequential delay) = 10 seconds.
    # With ThreadPoolExecutor and no sleep, 5 requests are executed concurrently in ~1s total.
    sequential_duration = len(MOCK_URLS) * 2.0  # 1s mock request + 1s sequential politeness sleep

    print("====================================================")
    print("             ⚡ BOLT PERFORMANCE BENCHMARK           ")
    print("====================================================")
    print(f"Number of leads processed: {len(MOCK_URLS)}")
    print(f"Simulated sequential processing duration: {sequential_duration:.2f} seconds")
    print(f"Actual parallelized/optimized duration:   {parallel_duration:.2f} seconds")

    speedup = sequential_duration / parallel_duration
    print(f"Estimated performance speedup:            {speedup:.1f}x faster")
    print("====================================================")

if __name__ == "__main__":
    run_benchmark()
