from os import stat


class User:
    db = None

    @staticmethod
    def initialize(cluster):
        User.db = cluster.db

    @staticmethod
    def register(user):
        User.db.users.insert_one(user)