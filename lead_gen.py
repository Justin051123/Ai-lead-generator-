import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re
import concurrent.futures
import threading

# Pre-compile regex pattern at module level for efficiency
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

# Thread-local storage to reuse HTTP requests.Session across worker threads
_thread_local = threading.local()

def get_thread_session():
    """Gets or creates a thread-local HTTP session for connection pooling and reuse."""
    if not hasattr(_thread_local, "session"):
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0'})
        _thread_local.session = session
    return _thread_local.session

def search_businesses(query, num_results=10):
    """Searches for businesses and returns a list of URLs."""
    urls = []
    try:
        for url in search(query, num_results=num_results):
            urls.append(url)
    except Exception as e:
        print(f"Error during search: {e}")
    return urls

def extract_info(url):
    """Extracts email and title from a website URL using thread-local session."""
    info = {"url": url, "email": "N/A", "title": "N/A"}
    try:
        session = get_thread_session()
        response = session.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract title
            if soup.title and soup.title.string:
                info["title"] = soup.title.string.strip()

            # Extract email using pre-compiled regex
            emails = EMAIL_PATTERN.findall(response.text)
            if emails:
                # Basic filtering to avoid common false positives
                filtered_emails = [email for email in set(emails) if not email.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg'))]
                if filtered_emails:
                    info["email"] = filtered_emails[0]

    except Exception as e:
        print(f"Error extracting info from {url}: {e}")
    return info

def qualify_lead(lead_info):
    """
    Placeholder for AI qualification.
    In a real app, this would send the website content to an LLM.
    """
    # Simple heuristic as a placeholder
    score = 0
    if lead_info["email"] != "N/A":
        score += 50
    if len(lead_info["title"]) > 10:
        score += 20

    lead_info["ai_score"] = score
    lead_info["qualification"] = "High" if score > 50 else "Medium" if score > 0 else "Low"
    return lead_info

def process_single_lead(url):
    """Worker function to process and qualify a single lead URL."""
    print(f"Processing {url}...")
    info = extract_info(url)
    return qualify_lead(info)

def generate_leads(niche, location, num_results=10):
    """Main function to generate leads concurrently while preserving result order."""
    query = f"{niche} in {location}"
    urls = search_businesses(query, num_results)
    if not urls:
        return []

    # Process URLs concurrently using ThreadPoolExecutor.
    # executor.map preserves the original search result ordering.
    max_workers = min(10, len(urls))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        leads = list(executor.map(process_single_lead, urls))

    return leads

if __name__ == "__main__":
    # Test
    leads = generate_leads("Plumbers", "London", num_results=3)
    print(leads)
