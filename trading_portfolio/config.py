from os import path, environ
from dotenv import load_dotenv

BASE_URL = path.abspath(path.dirname(__file__))

"""
    Loading all the key value pair specified in
    .env file into the environment
"""
load_dotenv(path.join(BASE_URL,'.env'))

""" Keep all the configurations here"""


class Config:
    SECRET_KEY = environ.get("SECRET_KEY")
    TESTING = False

class Development(Config):
    DEBUG = True
    ENV = 'development'
    MONGO_URI = environ.get("DEV_MONGO_URI")

class Production(Config):
    DEBUG = False
    ENV = "production"
    MONGO_URI = environ.get("PROD_MONGO_URI")