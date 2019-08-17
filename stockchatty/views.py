from yahoo_finance_api2 import share
from .models import StockModel

# Called from the GraphQL Query, function calls the retrieve function which uses the finance package
def get_data(kwargs):
    symbol = kwargs.get('symbol')
    days = kwargs.get('days')
    return retrieve(symbol, days)

# Calls the finance package to get data based on no of days and symbol of company
def retrieve(symbol, days):
    data = []
    try:
        # pass stock symbol of company to Share class
        yahoo = share.Share(symbol)

        # get historical yahoo data based on the number of days
        data = yahoo.get_historical(share.PERIOD_TYPE_DAY, days, share.FREQUENCY_TYPE_DAY, 1)

        # clean data to return model object declaration
        if 'volume' in data:
            new_data = [
                StockModel(**{'Volume': info, 'Symbol': symbol, 'High': data['high'][index], 'Low': data['low'][index],
                              'Close': data['close'][index], 'Open': data['open'][index],
                              'Date': data['timestamp'][index]}) for
                index, info in enumerate(data['volume'])]
            data = new_data
        else:
            data = []
    except Exception as ex:
        print("Failed to retrieve data.")
        print(ex)

    return data
