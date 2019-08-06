test_list = [
    {
        "date": "2010-03",
        "price": 2000
    },
    {
        "date": "2010-04",
        "price": 1950
    },
    {
        "date": "2010-05",
        "price": 1850
    }]

maxPricedItem = max(test_list, key=lambda x: x['date'])
minPricedItem = min(test_list, key=lambda x: x['date'])
print(minPricedItem)
print(maxPricedItem)
