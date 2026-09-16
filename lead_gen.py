from concurrent.futures import ThreadPoolExecutor
import re
import requests
from bs4 import BeautifulSoup
from googlesearch import search

# Pre-compile email regex pattern to avoid re-compiling inside the loop for every URL
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

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
    """Extracts email and title from a website URL using optional pooled HTTP session."""
    info = {"url": url, "email": "N/A", "title": "N/A"}
    try:
        requester = session if session is not None else requests
        response = requester.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract title
            if soup.title and soup.title.string:
                info["title"] = soup.title.string.strip()

            # Extract email using pre-compiled regex
            emails = EMAIL_PATTERN.findall(response.text)
            if emails:
                # Basic filtering to avoid common false positives (e.g. image filenames)
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

def process_single_lead(url, session=None):
    """Processes a single URL: extracts website info and qualifies the lead."""
    info = extract_info(url, session=session)
    return qualify_lead(info)

def generate_leads(niche, location, num_results=10, max_workers=10):
    """Main function to generate leads concurrently."""
    query = f"{niche} in {location}"
    urls = search_businesses(query, num_results)
    if not urls:
        return []

    # Use ThreadPoolExecutor to scrape and process websites in parallel for I/O efficiency.
    # executor.map preserves the original order of URLs returned by search_businesses.
    session = requests.Session()
    with ThreadPoolExecutor(max_workers=min(max_workers, len(urls))) as executor:
        leads = list(executor.map(lambda url: process_single_lead(url, session=session), urls))

    return leads

if __name__ == "__main__":
    # Test
    leads = generate_leads("Plumbers", "London", num_results=3)
    print(leads)
