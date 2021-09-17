from kucoin.client import Market

class KuCoin:
    def __init__(self):
        self.url = "https://api.kucoin.com"
        self.client = Market(self.url)

    def get_currencies(self):
        return self.client.get_symbol_list()

    def get_currencies_info(self):
        return self.client.get_all_tickers()

    def get_each_currency(self, currency_pair):
        return self.client.get_ticker(symbol=currency_pair)


