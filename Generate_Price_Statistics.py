import statistics

def generate_price_statistics(list_of_all_listings):
    # all bond prices
    bonds = []
    # all rent prices
    rents = []
    for listing in list_of_all_listings:
    # for listing in filtered_listings:
        if 'price' in listing:
            rents.append(listing['rent'])
        if 'bond' in listing:
            bonds.append(listing['bond'])

    return {
        'average_rent_value' : statistics.mean(rents),
        'median_rent_value' : statistics.median(rents),
        'average_bond_value' : statistics.mean(bonds),
        'median_bond_value' : statistics.median(bonds)
    }