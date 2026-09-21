import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re
import threading
from concurrent.futures import ThreadPoolExecutor

# Bolt Optimization: Pre-compile email regex pattern once globally to avoid overhead per request
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

# Thread-local storage for HTTP sessions to ensure thread safety while reusing connections
_thread_local = threading.local()

def get_thread_session():
    """Returns a thread-local requests.Session instance for connection reuse within the thread."""
    if not hasattr(_thread_local, "session"):
        _thread_local.session = requests.Session()
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

def extract_info(url, session=None):
    """Extracts email and title from a website URL. Accepts an optional requests.Session for connection reuse."""
    info = {"url": url, "email": "N/A", "title": "N/A"}
    try:
        requester = session if session is not None else get_thread_session()
        response = requester.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract title
            if soup.title and soup.title.string:
                info["title"] = soup.title.string.strip()

            # Extract email using pre-compiled regex
            emails = EMAIL_PATTERN.findall(response.text)
            if emails:
                # Basic filtering to avoid common false positives
                filtered_emails = [e for e in set(emails) if not e.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg'))]
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

def generate_leads(niche, location, num_results=10, max_workers=10):
    """
    Main function to generate leads.
    Bolt Optimization: Uses ThreadPoolExecutor with thread-local requests.Session instances to process
    I/O bound lead extraction concurrently and safely while preserving search result order.
    """
    query = f"{niche} in {location}"
    urls = search_businesses(query, num_results)
    if not urls:
        return []

    def process_single_lead(url):
        print(f"Processing {url}...")
        info = extract_info(url)
        return qualify_lead(info)

    workers = min(max_workers, len(urls))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # executor.map maintains original order of search results
        leads = list(executor.map(process_single_lead, urls))

    return leads

if __name__ == "__main__":
    # Test
    leads = generate_leads("Plumbers", "London", num_results=3)
    print(leads)
