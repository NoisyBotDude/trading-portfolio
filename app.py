from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add')
def add_new():
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)