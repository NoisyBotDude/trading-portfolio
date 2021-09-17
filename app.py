from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from api.coin import KuCoin

app = Flask(__name__)

kucoin = KuCoin()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_new():
    currency_pairs = kucoin.get_currencies()

    return render_template('form.html', currency_pairs=currency_pairs)

@app.route('/add/<string:currency_pair>', methods=['GET', 'POST'])
def currency_info(currency_pair):
    currency_pairs = kucoin.get_currencies()
    tickers = kucoin.get_each_currency(currency_pair)
    current_price = tickers['price']

    return render_template('form.html', currency_pairs=currency_pairs, currency_pair=currency_pair, current_price=current_price)

if __name__ == '__main__':
    app.run(debug=True)