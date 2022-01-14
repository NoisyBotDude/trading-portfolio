import datetime

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from trading_portfolio.api.coin import KuCoin
from trading_portfolio.database.database import CoinDatabase
from trading_portfolio.database.user import User
from werkzeug.security import check_password_hash, generate_password_hash

from ..utils.authentication import logged_in
from bson import ObjectId
from pymongo import MongoClient


def create_blueprint(cluster):
    user = Blueprint('user', __name__)

    db = cluster.db

    kucoin = KuCoin()

    @user.route('/')
    def index():
        if "username" in session:
            user_data = User.find_username(session["username"])
            user_coins = CoinDatabase.get_user_data(user_data)
            return render_template('user/home.html', user_coins=user_coins)

        return render_template('user/index.html')

    @user.route('/register', methods=['GET'])
    def register_page():
        if "username" in session:
            flash("Username is already logged in", category='duplicate')
            return redirect(url_for('user.index'))

        return render_template('user/register.html')

    @user.route('/register-user', methods=['POST'])
    def register_user():
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            flash('Passwords do not match', category='fail')
            return redirect(url_for('user.register_page'))

        else:
            hash_and_salted_password = generate_password_hash(
                password,
                method="pbkdf2:sha256",
                salt_length=8
            )
            user = {
                "username": username,
                "email": email,
                "password": hash_and_salted_password
            }

            User.register(user)
            session['username'] = username

            return redirect(url_for('user.index'))

    @user.route('/login', methods=['GET'])
    def login_page():
        if "username" in session:
            flash("Username is already logged in", category='duplicate')
            return redirect(url_for('user.index'))

        return render_template('user/login.html')

    @user.route('/login-user', methods=['POST'])
    def login_user():
        email = request.form['email-username']
        password = request.form['password']
        user_data = User.find_user(email)

        user_info = User.is_registered(email)

        if user_info:
            if check_password_hash(user_data["password"], password) == True:
                session['username'] = user_data["username"]
                return redirect(url_for('user.index'))
            else:
                flash('Incorrect password', category='fail')
                return redirect(url_for('user.login_page'))

        else:
            flash('User does not exist', category='fail')
            return redirect(url_for('user.login_page'))

    @user.route('/logout', methods=['GET'])
    def logout_user():
        session.pop('username', None)
        return redirect(url_for('user.index'))

    @user.route('/my-profile')
    def profile_page():
        return render_template('user/profile.html')

    @user.route('/add', methods=['GET', 'POST'])
    @logged_in
    def add_new():
        currency_pairs = kucoin.get_currencies()

        return render_template('user/form.html', currency_pairs=currency_pairs)

    @user.route('/add/<string:currency_pair>', methods=['GET'])
    def currency_info(currency_pair):
        currency_pairs = kucoin.get_currencies()
        tickers = kucoin.get_each_currency(currency_pair)
        current_price = tickers['price']

        return render_template('user/form.html',
                               currency_pairs=currency_pairs,
                               currency_pair=currency_pair,
                               current_price=current_price
                               )

    @user.route('/add/submit', methods=['POST'])
    def add_currency():
        coin_name = request.form["coin-name"]
        coin_quantity = request.form["coin-quantity"]
        coin_buy_price = float(request.form["buy-price"])
        invested = float(coin_buy_price) * float(coin_quantity)
        current_price = float(kucoin.get_each_currency(coin_name)['price'])
        current_value_in_usd = float(current_price) * float(coin_quantity)
        investment_in_usd = float(current_price) * float(coin_quantity)
        user_data = User.find_username(session['username'])

        data = {
            "coin name": coin_name,
            "coin quantity": coin_quantity,
            "coin buy ppprice": coin_buy_price,
            "coin purchase date": datetime.datetime.now(),
            "coin current price": current_price,
            "invested": invested,
            "current value in USD": current_value_in_usd,
            "Investment in USD": investment_in_usd,
            "changes": (current_price - coin_buy_price)/coin_buy_price * 100,
            "user data": user_data
        }

        CoinDatabase.add_pair(data)

        return redirect(url_for('user.add_new'))

    return user
