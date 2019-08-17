import pandas as pd
import os, json

print("loading data from CSV ...")
# Startup code

structures = [{"name": "1 Bedroom", "csv_title": "1Bedroom.csv", "key": "1bedroom"},
              {"name": "2 Bedroom", "csv_title": "2Bedroom.csv", "key": "2bedroom"},
              {"name": "3 Bedroom", "csv_title": "3Bedroom.csv", "key": "3bedroom"},
              {"name": "4 Bedroom", "csv_title": "4Bedroom.csv", "key": "4bedroom"},
              {"name": "5 Bedroom", "csv_title": "5Bedroom.csv", "key": "5bedroom"},
              {"name": "All Homes", "csv_title": "AllHomes.csv", "key": "allhomes"},
              {"name": "Condo", "csv_title": "Condo.csv", "key": "condo"},
              {"name": "Duplex Triplex", "csv_title": "DuplexTriplex.csv", "key": "duplextriplex"},
              {"name": "Mfr5Plus", "csv_title": "Mfr5Plus.csv", "key": "mfr5"},
              {"name": "Single Family Residential", "csv_title": "Sfr.csv", "key": "sfr"},
              {"name": "Studio", "csv_title": "Studio.csv", "key": "studio"}]

ignore_columns = ['RegionName', 'State', 'Metro', 'CountyName', 'SizeRank']

combined_list = []
new_list_prices = []
for index, i in enumerate(structures):
    struc_id = index + 1
    structure_info = {
        "model": "timeseries.structure",
        "pk": struc_id,
        "fields": {
            "name": i['name'],
            "csv_title": i['csv_title'],
            "key": i['key'],
            "start_date": "Michael B. Jordan",
            "end_date": "Michael B. Jordan"
        }
    }

    path = os.path.join("data/housecitydata/", i['csv_title'])
    data = pd.read_csv(path)

    new_data = data.dropna(axis=1, how='any')

    list_res = new_data.to_dict(orient='records')
    all_dates = []

    for index, rec in enumerate(list_res):
        price_id = index + 1
        all_keys = rec.keys()
        dates = [{'date': key, 'price': rec[key]} for key in all_keys if key not in ignore_columns]
        new_rec = dict([(k, v) for k, v in rec.items() if k in ignore_columns])
        new_rec['HousePrices'] = dates
        new_rec['structure'] = struc_id
        new_rec['start_date'] = min(dates, key=lambda x: x['date'])['date']
        new_rec['end_date'] = max(dates, key=lambda x: x['date'])['date']

        price_info = {
            "model": "timeseries.prices",
            "pk": price_id,
            "fields": new_rec
        }

        all_dates.extend(dates)
        new_list_prices.append(price_info)

    structure_info["fields"]['start_date'] = min(all_dates, key=lambda x: x['date'])['date']
    structure_info["fields"]['end_date'] = max(all_dates, key=lambda x: x['date'])['date']
    combined_list.append(structure_info)

combined_list.extend(new_list_prices)

json.dump(combined_list, open('sample_data.json', 'w'), indent=4)
print("ended saving data into json ...")
