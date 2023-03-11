import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url = "https://www.facebook.com/marketplace/"
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, "html.parser")

listings = []
for listing_elem in soup.find_all("div", class_="_fbn _5s2p")[:10]:
    title_elem = listing_elem.find("div", class_="_fbn _5s2p _2lcw _56be")
    price_elem = listing_elem.find("span", class_="_1svub _3-8er")

    title = title_elem.text.strip() if title_elem else None
    price_text = price_elem.text if price_elem else None
    price_match = re.search(r"\$(\d+(?:\.\d+)?)", price_text) if price_text else None
    price = float(price_match.group(1)) if price_match else None

    listings.append({"Title": title, "Price": price})

df = pd.DataFrame(listings)
df.to_csv("marketplace_listings.csv", index=False)