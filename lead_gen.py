import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re
import concurrent.futures

# Pre-compile regex for performance
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

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
    """Extracts email and title from a website URL."""
    info = {"url": url, "email": "N/A", "title": "N/A"}
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract title
            if soup.title:
                info["title"] = str(soup.title.string).strip() if soup.title.string else "N/A"

            # Extract email using pre-compiled regex
            emails = EMAIL_REGEX.findall(response.text)
            if emails:
                # Basic filtering to avoid common false positives
                filtered_emails = [e for e in set(emails) if not e.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.pdf'))]
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

def _process_url(url):
    """Internal helper to process a single URL."""
    print(f"Processing {url}...")
    info = extract_info(url)
    return qualify_lead(info)

def generate_leads(niche, location, num_results=10):
    """Main function to generate leads."""
    query = f"{niche} in {location}"
    urls = search_businesses(query, num_results)

    # Use ThreadPoolExecutor to parallelize I/O-bound web scraping.
    # This significantly improves performance compared to sequential processing.
    # We use executor.map to maintain the original order of search results.
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        leads = list(executor.map(_process_url, urls))

    return leads

if __name__ == "__main__":
    # Test
    leads = generate_leads("Plumbers", "London", num_results=3)
    print(leads)
