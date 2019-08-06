import pandas as pd
import os
from timeseries.models import Structure, Prices


print("loading data into db ...")
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

structure_filter = Structure.objects.filter(key=structures[0]['key'])
if structure_filter.count() < 1:
    for i in structures:
        structure = Structure.objects.create(**i)

        path = os.path.join("data/housecitydata/", i['csv_title'])
        data = pd.read_csv(path)
        # data.dropna()
        # data.fillna(0, inplace=True)
        new_data = data.dropna(axis=1, how='any')

        list_res = new_data.to_dict(orient='records')
        all_dates = []

        new_list_res = []
        for rec in list_res:
            all_keys = rec.keys()
            dates = [{'date': key, 'price': rec[key]} for key in all_keys if key not in ignore_columns]
            new_rec = dict([(k, v) for k, v in rec.items() if k in ignore_columns])
            new_rec['HousePrices'] = dates
            new_rec['start_date'] = min(dates, key=lambda x: x['date'])['date']
            new_rec['end_date'] = max(dates, key=lambda x: x['date'])['date']
            Prices.objects.create(structure=structure, **new_rec)
            all_dates.extend(dates)

        structure.start_date = min(all_dates, key=lambda x: x['date'])['date']
        structure.end_date = max(all_dates, key=lambda x: x['date'])['date']
        structure.save()

print("ended loading data into db ...")