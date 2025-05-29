import requests
import urllib3
from bs4 import BeautifulSoup
import pandas as pd
import time

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Sector-wise URLs
urls = [
    "https://growthlist.co/e-commerce-startups/",
    "https://growthlist.co/travel-startups/",
    "https://growthlist.co/mental-health-startups/",
    "https://growthlist.co/ev-startups/",
    "https://growthlist.co/list-of-funded-music-startups-for-2025/",
    "https://growthlist.co/list-of-funded-sports-startups-for-2025/",
    "https://growthlist.co/list-of-funded-construction-startups-for-2025/",
    "https://growthlist.co/data-analytics-startups/",
    "https://growthlist.co/fashion-startups/",
    "https://growthlist.co/personal-finance-startups/"
]

# Correct headers for HTTP request
request_headers = {'User-Agent': 'Mozilla/5.0'}

all_data = []
column_headers = []

for url in urls:
    print(f"Scraping: {url}")
    response = requests.get(url, headers=request_headers, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')
    if not table:
        print(f"❌ No table found at: {url}")
        continue

    # Extract column headers once
    if not column_headers:
        column_headers = [th.text.strip() for th in table.find_all('th')]

    for tr in table.find_all('tr')[1:]:
        cells = tr.find_all('td')
        row = [cell.text.strip() for cell in cells]
        if row:
            all_data.append(row)

    time.sleep(2)  # Be polite

# Build DataFrame only if data was found
if all_data and column_headers:
    df = pd.DataFrame(all_data, columns=column_headers)
    df.to_excel("funded_startups_multiple_sectors_2025.xlsx", index=False)
    print("✅ Data saved successfully.")
else:
    print("⚠️ No data scraped.")
