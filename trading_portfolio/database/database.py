class DataBase:
    db = None

    @staticmethod
    def initialize(cluster):
        DataBase.db = cluster.db

    @staticmethod
    def add_pair(data):
        DataBase.db.info.insert_one(data)