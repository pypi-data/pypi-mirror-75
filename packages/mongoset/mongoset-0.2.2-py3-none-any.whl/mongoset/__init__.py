from mongoset.database import Database

__version__ = "0.1.0"


def connect(uri: str, db_name: str = "database") -> Database:
    return Database(uri, db_name)
