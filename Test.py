import re
import statistics
from realestate_data import Search, Locality, PriceRange, Filters, paged_results
p = PriceRange()

l = Locality()
l.locality = 'Melbourne'
l.subdivision = Locality.SUBDIVISION_VIC
l.postcode = '3000'

f = Filters()
f.surrounding_suburbs = True

s = Search()
s.channel = Search.CHANNEL_RENT
s.localities = [l]
s.filters = f

paged_data = [page['tieredResults'] for page in paged_results(s)]
all_data = []

for page in paged_data:
    if page[0]['count'] > 0:
        for listing in page[0]['results']:
            all_data.append(listing)
    elif len(page) > 1 and page[1]['count'] > 0:
        for listing in page[1]['results']:
            all_data.append(listing)
    else:
        pass

 # format price to int
formated_listings=[]
for index,listing in enumerate(all_data):
   
    if any(char.isdigit() for char in listing['price']['display']):
        # extract_number = int(re.findall('\d+', listing['price']['display'])[0])
        extract_number = int(re.findall('[\d,]+', listing['price']['display'].replace(',', ''))[0])
        
        listing['price'] = extract_number
        formated_listings.append(listing)

def filtaaa(listing):    
    max_price=900
    min_bedroom=3
    if listing['price'] <= max_price and listing['features']['general']['bedrooms'] >= min_bedroom:
        return True
    else:
        return False

filtered_listings_please_extract = filter(filtaaa, formated_listings)
filtered_listings = list(filtered_listings_please_extract)

def generate_price_statistics(list_of_all_listings):
    # all bond prices
    bonds = []
    # all rent prices
    rents = []
    for listing in list_of_all_listings:
    # for listing in filtered_listings:
        if 'price' in listing:
            rents.append(listing['price'])
        if 'bond' in listing:
            bonds.append(listing['bond']['value'])

    return {
        'average_rent_value' : statistics.mean(rents),
        'median_rent_value' : statistics.median(rents),
        'average_bond_value' : statistics.mean(bonds),
        'median_bond_value' : statistics.median(bonds)
    }

essential_info_dicts = []


# Generate Essential info dicts
# Titel
# Type
# Address
# RealEstate Agency
# Agent Name
# Agent Email/Profile
# Listing URL
for listing in filtered_listings:
    pass


# Save all of the above listings in a database

L=0

