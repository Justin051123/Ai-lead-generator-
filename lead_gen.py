import requests
from bs4 import BeautifulSoup
from googlesearch import search
import re
from concurrent.futures import ThreadPoolExecutor

# ⚡ Bolt Optimization: Pre-compile email regex to avoid recompiling it in every HTTP request.
# This saves precious CPU cycles when processing websites in batches.
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

def search_businesses(query, num_results=10):
    """Searches for businesses and returns a list of URLs."""
    urls = []
    try:
        for url in search(query, num_results=num_results):
            urls.append(url)
    except Exception as err:
        print(f"Error during search: {err}")
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
                info["title"] = soup.title.string.strip()

            # ⚡ Bolt Optimization: Use pre-compiled regex for fast pattern matching.
            emails = EMAIL_REGEX.findall(response.text)
            if emails:
                # Basic filtering to avoid common false positives
                filtered_emails = [email for email in set(emails) if not email.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg'))]
                if filtered_emails:
                    info["email"] = filtered_emails[0]

    except Exception as err:
        print(f"Error extracting info from {url}: {err}")
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
    """
    ⚡ Bolt Optimization: Modularized single-lead processing.
    Processes a single lead: extracts information and qualifies it.
    This enables concurrent execution across threads.
    """
    print(f"Processing {url}...")
    info = extract_info(url)
    return qualify_lead(info)

def generate_leads(niche, location, num_results=10):
    """
    Main function to generate leads.

    ⚡ Bolt Optimization: Parallelized web scraping using ThreadPoolExecutor.
    Instead of sequentially scraping each website and adding artificial delays,
    we fetch websites concurrently using a pool of worker threads.

    We use executor.map to ensure that we preserve the original order of search results
    (which are ranked by relevance by Google Search).
    """
    query = f"{niche} in {location}"
    urls = search_businesses(query, num_results)

    # Run requests concurrently using up to 10 workers
    max_workers = min(len(urls), 10) if urls else 1
    if max_workers > 0:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            leads = list(executor.map(process_single_lead, urls))
    else:
        leads = []

    return leads

if __name__ == "__main__":
    # Test
    leads = generate_leads("Plumbers", "London", num_results=3)
    print(leads)
