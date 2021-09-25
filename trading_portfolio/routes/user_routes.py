from flask import Blueprint, render_template, request, redirect, url_for, flash
from trading_portfolio.database.database import DataBase
from trading_portfolio.database.user import User
from trading_portfolio.api.coin import KuCoin
from flask_login import login_required, login_user, logout_user, current_user
import datetime

def create_blueprint(cluster):
    user = Blueprint('user', __name__)

    db = cluster.db

    kucoin = KuCoin()

    @user.route('/')
    def index():
        return render_template('user/index.html')

    @user.route('/register', methods=['GET'])
    def register_page():
        return render_template('user/register.html')

    @user.route('/register-user', methods=['POST'])
    def register_user():
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
            
        user = {
                "username": username,
                "email": email,
                "password": password,
                "confirm_password": confirm_password
        }

        User.register(user)

        return redirect(url_for('user.index'))

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
        coin_buy_price = float(request.form["buy-price"])
        invested = float(coin_buy_price) * float(coin_quantity)
        current_price = float(kucoin.get_each_currency(coin_name)['price'])
        current_value_in_usd = float(current_price) * float(coin_quantity)
        investment_in_usd = float(current_price) * float(coin_quantity)

        data = {
            "coin name": coin_name,
            "coin quantity": coin_quantity,
            "coin buy ppprice": coin_buy_price,
            "coin purchase date": datetime.datetime.now(),
            "coin current price": current_price,
            "invested": invested,
            "current value in USD": current_value_in_usd,
            "Investment in USD": investment_in_usd,
            "changes": (current_price - coin_buy_price)/coin_buy_price * 100
        }

        DataBase.add_pair(data)

        return redirect(url_for('user.add_new'))

    return user