import email
from os import stat

class User:
    db = None

    @staticmethod
    def initialize(cluster):
        User.db = cluster.db

    @staticmethod
    def register(user):
        User.db.users.insert_one(user)

    @staticmethod
    def find_user(email):
        user_data = User.db.users.find_one(
            {"email": email}, {"username": 1, "email": 1, "password": 1, "_id": 0}
        )
        return user_data

    @staticmethod
    def is_registered(email):
        return User.db.users.find_one({'email': email}, {"_id" : 0})

    @staticmethod
    def find_username(username):
        user_data = User.db.users.find_one(
            {"username": username}, {"username": 1, "email": 1, "_id": 1}
        )
        return user_data