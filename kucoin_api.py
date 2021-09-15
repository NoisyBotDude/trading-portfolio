#  MarketData
from kucoin.client import Market
client = Market(url='https://api.kucoin.com')
# client = Market()

# 1st PART
currencies = client.get_symbol_list()

for i in currencies:
    print(i["symbol"])

# 2nd PART
tickers = client.get_all_tickers()

ticker = tickers["ticker"]

for i in ticker:
    symbol = i["symbol"]
    if symbol == "BTC-USDT":
        print(symbol)
        print(i["buy"])
        print(i["sell"])

