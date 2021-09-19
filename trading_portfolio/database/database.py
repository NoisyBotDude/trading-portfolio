class Database:
    db = None

    @staticmethod
    def initialize(cluster):
        Database.db = cluster.db