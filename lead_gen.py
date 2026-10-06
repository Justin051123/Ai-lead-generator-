import concurrent.futures
import re
import threading
import requests
from bs4 import BeautifulSoup
from googlesearch import search

# Pre-compiled regex pattern for efficient email extraction across requests
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

# Thread-local storage for reusing requests.Session per thread (connection pooling)
_thread_local = threading.local()


def get_thread_session():
    """Returns a thread-local requests.Session instance for connection pooling."""
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
    """Extracts email and title from a website URL using connection pooling and pre-compiled regex."""
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
                filtered_emails = [
                    e for e in set(emails)
                    if not e.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg'))
                ]
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
    """Extracts info and qualifies a single lead url."""
    print(f"Processing {url}...")
    info = extract_info(url)
    return qualify_lead(info)


def generate_leads(niche, location, num_results=10, max_workers=10):
    """
    Main function to generate leads concurrently.
    Uses ThreadPoolExecutor to process URLs in parallel while preserving order.
    """
    query = f"{niche} in {location}"
    urls = search_businesses(query, num_results)
    if not urls:
        return []

    # Parallelize extraction and qualification while keeping result order
    workers = min(max_workers, len(urls))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        leads = list(executor.map(process_single_lead, urls))

    return leads


if __name__ == "__main__":
    # Test
    leads = generate_leads("Plumbers", "London", num_results=3)
    print(leads)
