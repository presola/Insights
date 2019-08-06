from django.shortcuts import render
from django.http import JsonResponse
from .models import Structure, Prices
from .serializers import PricesSerializer
from .functions.general import format_structures, format_date
import pandas as pd
import numpy as np
import statsmodels.api as sm
from datetime import datetime
import copy

'''
    Predict house prices
'''
def predict_prices(data, start, end):
    new_list = []
    try:
        for i in data:
            start_d = datetime.strptime(copy.deepcopy(i['end_date']), '%Y-%m')
            end_d = datetime.strptime(copy.deepcopy(end), '%Y-%m')
            date_rng = pd.date_range(start=start_d, end=end_d, freq='m')
            len_date_rng = len(date_rng)

            house_prices = i['HousePrices']
            df = pd.DataFrame(house_prices)
            df['datetime'] = pd.to_datetime(df['date'])
            df.drop(['date'], axis=1, inplace=True)
            df['date'] = df['datetime'] 
            df.drop(['datetime'], axis=1, inplace=True)
            df = df.set_index('date')
            mod = sm.tsa.statespace.SARIMAX(df,
                                    order=(1, 1, 1),
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)

            results = mod.fit()
            
            len_date_rng = len_date_rng + 1

            pred_uc = results.get_forecast(steps=len_date_rng)
            
            new_df = pd.DataFrame(pred_uc.predicted_mean)
            new_df.reset_index(inplace=True)
            new_df.columns = ['date', 'price']
            datetimes = [start, end]
            list_dates = pd.to_datetime(datetimes).tolist()
            new_df = new_df[(new_df['date'] >= list_dates[0]) & (new_df['date'] <= list_dates[1])]

            new_df['date'] = new_df['date'].map(lambda x: x.strftime('%Y-%m'))

            new_df['price'] = new_df['price'].round(2)
            new_prices = new_df.to_dict(orient='records')
            
            
            i['HousePrices'] = new_prices

            new_list.append(i)
    except Exception as e:
        print(e)

    return new_list

'''
    Filter or predict Structures
'''
def process_structure(request, id):
    parameters = request.data
    ignore_col = ['predict', 'start_date', 'end_date']
    if id != 'all':
        structure = Structure.objects.filter(id=id).get()
    else:
        structure = Structure.objects.all()

    keys = dict([(k, v) for k, v in parameters.items() if not v == 'all' and k not in ignore_col])

    price = Prices.objects.filter(structure=structure, **keys).all()
    serializer = PricesSerializer(price, many=True)
    result = format_structures(serializer.data)


    if 'predict' in parameters and parameters['predict']:
        new_list = []
        if len(result) > 0:
            new_list = predict_prices(list(result), parameters['start_date'], parameters['end_date'])
    else:
        new_list = format_date(result, parameters['start_date'], parameters['end_date'])
    
    return JsonResponse(new_list, safe=False, status=200)
