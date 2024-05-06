import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pymongo import MongoClient

# Setup MongoDB connection
client = MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.0.0")
db = client['swiftsearch']  # Name of the database
collection = db['sites']  # Name of the collection
count = 0
def get_internal_links(url):
    """ Fetches a webpage and returns a list of links to internal pages. """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = set()
    
    for link_tag in soup.find_all('a', href=True):
        link = link_tag['href']
        full_link = urljoin(url, link)
        if urlparse(full_link).netloc == urlparse(url).netloc:
            links.add(full_link)
    
    return links

def scrape_site(url):
    """ Recursively scrapes all internal links of the website. """
    to_visit = get_internal_links(url)
    visited = set()
    
    while to_visit:
        current_url = to_visit.pop()
        if current_url not in visited:
            visited.add(current_url)
            ++count
            print(f"{count}. Scraping {current_url}")
            metadata = extract_metadata(current_url)
            # Save the metadata into MongoDB
            collection.insert_one(metadata)
            internal_links = get_internal_links(current_url)
            to_visit.update(internal_links - visited)

def extract_metadata(url):
    """ Extracts title, description, author, and publication date from a given URL. """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.find('title').text if soup.find('title') else "-"
    description = soup.find("meta", attrs={"name": "description"})['content'] if soup.find("meta", attrs={"name": "description"}) else "-"
    author = soup.find("meta", attrs={"name": "author"})['content'] if soup.find("meta", attrs={"name": "author"}) else "-"
    published_at = soup.find("p", class_="sdc-article-date__date-time").text if soup.find("p", class_="sdc-article-date__date-time") else "-"

    
    return {
        "url": url,
        "title": title,
        "description": description,
        "author": author,
        "published_at": published_at,
        "source": "Sky Sports"
    }

# Start scraping from a given URL
scrape_site("https://www.skysports.com")
