
from Results_RealeasteteComAu import RealEstateComAu
# from Results_FB_Marketplace import 
# from Results_FB_Groups import 

from Bulk_Mail_Sender import EmailSender
from DB_Class import RealEstateDB

Melbounre_RealestateComAu = RealEstateComAu()
all_data = Melbounre_RealestateComAu.fetch_data('Melbourne','3000')


def filter_bedrooms_and_price(listing):    
    # if listing['price'] <= 900 and listing['features']['general']['bedrooms'] >= 3:
    #     return True
    # elif listing['price'] <= 600 and listing['features']['general']['bedrooms'] >= 2:
    #     return True
    if listing['price'] <= 300 and listing['features']['general']['bedrooms'] >= 1:
        return True
    else:
        return False

filtered_listings_please_extract = filter(filter_bedrooms_and_price, all_data)
filtered_listings = list(filtered_listings_please_extract)



essential_info_dicts = []

# Generate Essential info dicts
for listing in filtered_listings:
    
    essential_info_dicts.append({
        'title': listing.get('title', 0),
        'type': listing.get('propertyType', 0),
        'address': listing.get('address', 0),
        'address_str': listing.get('address', 0).get('streetAddress') + ' in ' + listing.get('address', 0).get('locality'),
        'bed_rooms': listing.get('features',{}).get('general',{}).get('bedrooms',0),
        'bond': listing.get('bond', {}).get('value', 0),
        'rent': listing.get('price', 0),
        'rent_per_room': listing.get('price', 0)/listing.get('features',{}).get('general',{}).get('bedrooms',0),
        'agency': listing.get('agency', {}).get('name', 0),
        'agent_name': listing.get('lister', {}).get('name', 0),
        'agent_mail': listing.get('lister', {}).get('email', 0),
        # 'agent_mail': 'kilivoss@gmail.com',
        'url': listing.get('_links', {}).get('prettyUrl', {}).get('href', 0),
        'listing_id': listing['listingId']
    })

Bulk_Email_Instance = EmailSender()
# Generate Emails for each listing
Bulk_Email_Instance.generating_all_emails(essential_info_dicts)
# Save all of the above listings in a database#
# Create a new instance of the RealEstateDB class
db = RealEstateDB()
for listing in essential_info_dicts:
    db.insert_listing(listing)

# Bulk_Email_Instance.send_all_emails(essential_info_dicts)

L=0

