from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import time
from requests import Session
from bs4 import BeautifulSoup
import pandas as pd
import random
import json
import re
from scraper.model import PropertyRecord
from scraper.common import USER_AGENTS, MAX_THREADS


# Batch size for saving records
BATCH_SIZE = 1000

def scrape_properties(session, properties_urls):
    properties = []
    total_count = 0
    batch_number = 1
    start_time = time.time()  

    # Scrape details for each property in parallel *MAX_THREADS
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_url = {executor.submit(scrape_details, session, url): url for url in properties_urls}
        for future in as_completed(future_to_url):
            try:
                property_record = future.result()
                if property_record:
                    print(property_record)

                    properties.append(property_record.__dict__)
                    total_count += 1
                    
                    # Save every BATCH_SIZE records
                    if len(properties) >= BATCH_SIZE:
                        save_batch_to_csv(properties, batch_number)
                        batch_number += 1
                        properties = []  # Reset the list

                print_state(total_count, properties_urls, start_time)
                    
            except Exception as e:
                print(f"Error scraping property: {e}")

    # Save final batch if there are any remaining properties
    if properties:
        save_batch_to_csv(properties, 9999) 

    return total_count

def scrape_details(session, url):
    """ Scrape the details of a real estate property. """

    r = session.get(
        url, 
        headers={'User-Agent': random.choice(USER_AGENTS)},
    )

    json_object = get_json_data(r)

    if json_object is None:
        return None

    return PropertyRecord.from_json(json_object)

def get_json_data(r):
    """Extract JSON data from the response content."""
    soup = BeautifulSoup(r.content, "html.parser")
    classified_div = soup.select_one("#plato\\.immo + .classified script")

    if classified_div:
        script_content = classified_div.string.strip()
        # Use regex to remove prefix : `window.classified = ` and suffix : `; window.hasVirtualStaging = false;`
        json_string = re.sub(r'^window\.classified = (.*?);\s*window\.hasVirtualStaging = .*;\s*$', r'\1', script_content, flags=re.DOTALL).strip()
        
        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            print("Failed to decode JSON")
            return None

    return None


def load_urls():
    """Load URLs from CSV file"""
    try:
        df = pd.read_csv("./data/urls/urls.csv")
        return df["url"].tolist()
    except FileNotFoundError:
        print("Error: urls.csv not found. Please run urls_scraper.py first.")
        return []
    
def save_batch_to_csv(properties, batch_number):
    """Save a batch of properties to a CSV file"""
    # Create DataFrame and save as CSV
    df = pd.DataFrame(properties)
    
    # If it's the first batch, write with headers, otherwise append without headers
    mode = 'w' if batch_number == 1 else 'a'
    header = batch_number == 1
    
    df.to_csv("./data/properties/data.csv", mode=mode, header=header, index=False)
    print(f"Saved batch {batch_number} with {len(properties)} records")

def print_state(total_count, all_property_urls, start_time): 
    os.system('cls' if os.name == 'nt' else 'clear')
                        
    #Thanks GPT for the calculation of ETA :D
    if total_count > 0:
        elapsed_time = time.time() - start_time
        avg_time_per_location = elapsed_time / total_count
        remaining_locations = len(all_property_urls) - total_count
        eta_seconds = avg_time_per_location * remaining_locations
        eta_minutes = eta_seconds / 60
        
        print(f"Properties fetched: {total_count} / {len(all_property_urls)} - ETA: {eta_minutes:.2f} minutes")
    else:
        print(f"Properties fetched: {total_count} / {len(all_property_urls)}")


def start_properties_scraping():
    print("Loading property URLs...")
    properties_urls = load_urls()
    
    if not properties_urls:
        print("No property URLs found. Please run urls_scraper.py first.")
        return
    
    print(f"Starting to scrape details for {len(properties_urls)} properties...")
    with Session() as session:
        start_time = time.time()
        total_count = scrape_properties(session, properties_urls)
        end_time = time.time() 
        
        print(f"Scraping completed in {end_time - start_time:.2f} seconds. Total records: {total_count}")