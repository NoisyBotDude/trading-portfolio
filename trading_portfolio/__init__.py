from flask import Flask
from os import environ, environb
from .config import Development, Production
from flask_pymongo import PyMongo
from .database.database import Database
from .routes import user_routes

def create_app():

    app = Flask(__name__)

    app.config.from_object(config.Development())

    cluster = PyMongo(app)
    Database.initialize(cluster)

    """Note: Blueprint is used to separate routes into different
             folders and files for better organization of files
    """

    app.register_blueprint(user_routes.create_blueprint(cluster))

    return app