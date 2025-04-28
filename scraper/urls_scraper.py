from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from requests import Session
from bs4 import BeautifulSoup
import pandas as pd
import random
from scraper.common import USER_AGENTS, MAX_THREADS


PROVINCES = ['antwerpen', 'brabant-flamand', 'west-flanders', 'east-flanders', 'hainaut', 'liege', 'limbourg', 'luxembourg', 'namur', 'bruxelles', 'walloon-brabant']

BASE_URL = "https://www.immoweb.be/fr/recherche/maison-et-appartement/a-vendre/{}/province?countries=BE&isAPublicSale=false&isALifeAnnuitySale=false&isAnInvestmentProperty=false&page={}"


def scrape_properties_urls(session):
    """ Scrape all real estate property URLs from the given listing URLs in parallel. """
    urls = []

    # Use ThreadPoolExecutor to fetch multiple province listings concurrently
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_province = {executor.submit(scrape_province_urls, session, province): province for province in PROVINCES}
        for future in as_completed(future_to_province):
            urls.extend(future.result())

    return urls

def scrape_province_urls(session, province):
    """Scrape listing pages for a given province and return all property URLs."""
    page = 1
    province_urls = []

    while True:
        u = BASE_URL.format(province, page)
        print(f"Fetching page {page} for province: {province}")
        r = session.get(u, headers={'User-Agent': random.choice(USER_AGENTS)})

        soup = BeautifulSoup(r.content, "html.parser")
        listings = soup.select("h2 > a.card__title-link")  # Avoid recommendations

        if not listings:
            print(f"No more properties for province: {province}")
            break

        province_urls.extend([elem.get("href") for elem in listings])
        page += 1

    return province_urls

def save_urls_to_csv(urls):
    """Save URLs to CSV file"""
    # Create DataFrame and save as CSV
    df = pd.DataFrame(urls, columns=["url"])
    df_uniques = df.drop_duplicates(subset='url', keep='first')
    df_uniques.to_csv("./data/urls/urls.csv", index=False)
    print(f"Saved {len(urls)} URLs")

def start_urls_scraping():
    with Session() as session:
        print("Starting to scrape property URLs...")
        start_time = time.time()
        property_urls = scrape_properties_urls(session)
        end_time = time.time()

        print(f"Found {len(property_urls)} property URLs in {end_time - start_time:.2f} seconds")
        save_urls_to_csv(property_urls)