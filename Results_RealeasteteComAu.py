# p = PriceRange()
# listings_for_all_postcodes = []
# list_of_postcodes = ['3000', '3001', '3002', '3003', '3004', '3005', '3006', '3008', '3010', '3011', '3012', '3013', '3015', '3016', '3018', '3019', '3020', '3021', '3022', '3023', '3024', '3025', '3026', '3027', '3028', '3029', '3030', '3031', '3032', '3033', '3034', '3036', '3037', '3038', '3039', '3040', '3041', '3042', '3043', '3044', '3045', '3046', '3047', '3048', '3049', '3050']

# for code in list_of_postcodes: 
#     pass

# import re
# from realestate_data import Search, Locality, PriceRange, Filters, paged_results

# l = Locality()
# l.locality = 'Melbourne'
# l.subdivision = Locality.SUBDIVISION_VIC
# l.postcode = '3000'

# f = Filters()
# f.surrounding_suburbs = True

# s = Search()
# s.channel = Search.CHANNEL_RENT
# s.localities = [l]
# s.filters = f

# paged_data = [page['tieredResults'] for page in paged_results(s)]
# all_data = []

# for page in paged_data:
#     if page[0]['count'] > 0:
#         for listing in page[0]['results']:
#             if any(char.isdigit() for char in listing['price']['display']):
#                 extract_number = int(re.findall('[\d,]+', listing['price']['display'].replace(',', ''))[0])
#                 listing['price'] = extract_number
#                 all_data.append(listing)
#     elif len(page) > 1 and page[1]['count'] > 0:
#         for listing in page[1]['results']:
#             if any(char.isdigit() for char in listing['price']['display']):
#                 extract_number = int(re.findall('[\d,]+', listing['price']['display'].replace(',', ''))[0])
#                 listing['price'] = extract_number
#                 all_data.append(listing)
#     else:
#         pass



import re
from realestate_data import Search, Locality, PriceRange, Filters, paged_results

class RealEstateComAu:
    
    def __init__(self):
        self.p = PriceRange()
        self.listings_for_all_postcodes = []
        self.list_of_postcodes = ['3000', '3001', '3002', '3003', '3004', '3005', '3006', '3008', '3010', '3011', '3012', '3013', '3015', '3016', '3018', '3019', '3020', '3021', '3022', '3023', '3024', '3025', '3026', '3027', '3028', '3029', '3030', '3031', '3032', '3033', '3034', '3036', '3037', '3038', '3039', '3040', '3041', '3042', '3043', '3044', '3045', '3046', '3047', '3048', '3049', '3050']
        self.all_data = []
        self.essential_info_dicts = []
        
    
    def fetch_data(self,locality, postcode):
        l = Locality()
        l.locality = locality
        l.subdivision = Locality.SUBDIVISION_VIC
        l.postcode = postcode

        f = Filters()
        f.surrounding_suburbs = True

        s = Search()
        s.channel = Search.CHANNEL_RENT
        s.localities = [l]
        s.filters = f

        paged_data = [page['tieredResults'] for page in paged_results(s)]

        for page in paged_data:
            if page[0]['count'] > 0:
                for listing in page[0]['results']:
                    if any(char.isdigit() for char in listing['price']['display']):
                        extract_number = int(re.findall('[\d,]+', listing['price']['display'].replace(',', ''))[0])
                        listing['price'] = extract_number
                        self.all_data.append(listing)
            elif len(page) > 1 and page[1]['count'] > 0:
                for listing in page[1]['results']:
                    if any(char.isdigit() for char in listing['price']['display']):
                        extract_number = int(re.findall('[\d,]+', listing['price']['display'].replace(',', ''))[0])
                        listing['price'] = extract_number
                        self.all_data.append(listing)
            else:
                pass

        return self.all_data
    
    def generate_esential_info_dicts(self):
        for listing in self.all_data:
            
            self.essential_info_dicts.append({
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