from flask import Blueprint, render_template, request, redirect, url_for, flash
from trading_portfolio.database.database import DataBase
from trading_portfolio.api.coin import KuCoin

def create_blueprint(cluster):
    user = Blueprint('user', __name__)

    db = cluster.db

    kucoin = KuCoin()

    @user.route('/')
    def index():
        return render_template('user/index.html')

    @user.route('/add', methods=['GET', 'POST'])
    def add_new():
        currency_pairs = kucoin.get_currencies()

        return render_template('user/form.html', currency_pairs=currency_pairs)

    @user.route('/add/<string:currency_pair>', methods=['GET'])
    def currency_info(currency_pair):
        currency_pairs = kucoin.get_currencies()
        tickers = kucoin.get_each_currency(currency_pair)
        current_price = tickers['price']

        return render_template('user/form.html', currency_pairs=currency_pairs, currency_pair=currency_pair, current_price=current_price)

    @user.route('/add/submit', methods=['POST'])
    def add_currency():
        coin_name = request.form["coin-name"]
        coin_quantity = request.form["coin-quantity"]
        coin_buy_price = request.form["buy-price"]
        

        data = {
            "coin name": coin_name,
            "coin quantity": coin_quantity,
            "coin buy price": coin_buy_price   
        }

        DataBase.add_pair(data)

        return redirect(url_for('user.add_new'))

    return user