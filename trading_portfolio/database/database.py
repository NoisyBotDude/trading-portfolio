from tkinter.messagebox import NO


class CoinDatabase:
    db = None

    @staticmethod
    def initialize(cluster):
        CoinDatabase.db = cluster.db

    @staticmethod
    def add_pair(data):
        CoinDatabase.db.info.insert_one(data)

    @staticmethod
    def get_pair(pair):
        return CoinDatabase.db.info.find_one({ "coin name": pair}, {"_id" : 0})

    @staticmethod
    def get_user_data(user_data):
        return CoinDatabase.db.info.find_one({"user data": user_data}, {"_id" : 0})

    