import pandas as pd

'''
    validate start and end date
'''
def format_date(all, start, end):
    new_all = []
    for d in all:
        prices = d['HousePrices']
        new_list = []
        
        for i in prices:
            datetimes = [i['date'], start, end]
            list_dates = pd.to_datetime(datetimes).tolist()

            if list_dates[0] >= list_dates[1] and list_dates[0] <= list_dates[2]:
                new_list.append(i)
        d['HousePrices'] = new_list
        d['start_date'] = min(new_list, key=lambda x: x['date'])['date'] if len(new_list) > 0 else "2015-06"
        d['end_date'] = max(new_list, key=lambda x: x['date'])['date'] if len(new_list) > 0 else "2015-07"

        new_all.append(d)

    return new_all

def format_structures(structure_prices):
    new_list = []
    list_states = []
    for i in structure_prices:
        if i['State'] not in list_states:
            new_list.append(i)
            list_states.append(i['State'])
    return new_list