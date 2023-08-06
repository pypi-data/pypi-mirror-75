from typing import List, Optional, Union

import pymongo
import pymongo.results
from bson import ObjectId


class Database:
    def __init__(self, uri="", db_name="database"):
        # write_concern = pymongo.write_concern.WriteConcern(w="majority", fsync=True)
        write_concern = pymongo.write_concern.WriteConcern(w=3, fsync=True)
        read_concern = pymongo.read_concern.ReadConcern(level="majority")

        self.client = pymongo.MongoClient(
            uri, w="majority", fsync=True, wTimeoutMS=0, readPreference="primary"
        )

        self.db_name = db_name

    def __getitem__(self, table):
        return Table(self.client, db_name=self.db_name, table_name=table)

    def drop(self):
        """
        Drops collection
        """
        self.client.drop_database(self.db_name)

class Table:
    def __init__(
        self,
        client: pymongo.MongoClient,
        db_name: str = "database",
        table_name: str = "table",
    ):
        self.client = client
        self.db_name = db_name
        self.table_name = table_name
        self.table = self.client[self.db_name][self.table_name]

    def insert(self, row: dict) -> Union[bool, str]:
        """
        Inserts row. Returns true if the write is acknowledged.
        """
        insert_response = self.table.insert_one(row)

        if insert_response.acknowledged:
            return str(insert_response.inserted_id)
        else:
            return False

    def upsert(self, row: dict, key: List[str] = None) -> bool:
        """
        Upserts a row. Returns the number of documents modified. By default, if _id is not passed, it'll attempt to insert. Will return 0 if a document was inserted.
        """
        row = self._convert_id_to_obj(row)
        if (not key) and "_id" in row:
            key = ["_id"]
        elif not key:
            raise ValueError("No key provided")

        f = {a: b for a, b in [(i, row[i]) for i in key]}

        # update_response = self.table.update_one(f, {"$set": row}, upsert=True)
        update_response = self.table.update_one(f, {"$set": row}, upsert=True)

        # if (not update_response.modified_count) and (not update_response.matched_count):
        #    return self.insert(row)
        # else:
        #     return update_response.modified_count

        return bool(update_response.modified_count)

    def update(self, row: dict, key: List[str] = None) -> bool:
        """
        Updates a row. Returns the number of documents modified. Good for locking and other sensitive operations.
        """
        row = self._convert_id_to_obj(row)
        if (not key) and "_id" in row:
            key = ["_id"]
        elif not key:
            raise ValueError("No key provided")

        f = {a: b for a, b in [(i, row[i]) for i in key]}

        # update_response = self.table.update_one(f, {"$set": row}, upsert=True)
        update_response = self.table.update_one(f, {"$set": row})

        return bool(update_response.modified_count)

    def find_one(self, projection=None, **filter_expr) -> dict:
        """
        Returns the first match
        """
        filter_expr = self._convert_id_to_obj(self._eval_filter_expr(filter_expr))
        response = self.table.find_one(filter_expr, projection)
        if response:
            return self._convert_id_to_str(dict(response))

        return None

    def find(self, projection=None, **filter_expr) -> List[dict]:
        """
        Searches. Does not support comparison operators yet.
        """
        filter_expr = self._convert_id_to_obj(self._eval_filter_expr(filter_expr))
        return [
            self._convert_id_to_str(dict(i))
            for i in self.table.find(filter_expr, projection)
        ]

    def all(self) -> List[dict]:
        """
        Returns everything in the table
        """
        return [dict(self._convert_id_to_str(i)) for i in self.table.find()]

    def delete(self, **filter_expr) -> int:
        """
        Deletes everything that matches. Returns the number of items deleted.
        """
        if not filter_expr:
            raise ValueError(
                "Error! Empty filter expression! Call db.clear() if you want to delete everything"
            )

        delete_response = self.table.delete_many(
            self._convert_id_to_obj(self._eval_filter_expr(filter_expr))
        )

        return delete_response.deleted_count

    def clear(self) -> int:
        """
        Clears the entire table. Returns the number of items that were deleted.
        """
        return self.table.delete_many({}).deleted_count

    def count(self, **filter_expr) -> int:
        """
        Counts the number of items that match the filter expression
        """
        return int(self.table.count_documents(self._eval_filter_expr(filter_expr)))

    def index(self, key: str, unique=True, index_type=pymongo.ASCENDING):
        """
        Creates an index on the collection. If unique is set to True, an unique index is created and enforced.
        """
        index = pymongo.operations.IndexModel((key), name=key + "_index", unique=unique)
        self.table.create_index(index)

    def deindex(self, key: str):
        """
        Removes an index in the collection.
        """
        self.table.drop_index(key + "_index")

    def deindex_all(self):
        """
        Deletes all indexes
        """
        self.table.drop_indexes()

    __len__ = count

    @staticmethod
    def _eval_filter_expr(filer_expr: dict) -> dict:
        for key, val in filer_expr.items():
            if isinstance(val, Expression):
                val = val.to_dict()
                filer_expr[key] = val

            if isinstance(val, tuple):
                new_val = dict()

                for expr in val:
                    assert isinstance(expr, Expression)
                    new_val.update(expr.to_dict())

                filer_expr[key] = new_val

        return filer_expr

    @staticmethod
    def _convert_id_to_str(data: dict) -> dict:
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return data

    @staticmethod
    def _convert_id_to_obj(data: dict) -> dict:
        if "_id" in data:
            data["_id"] = ObjectId(data["_id"])
        return data


class Expression:
    def __init__(self, key, val):
        self.key: str = key
        self.val: str = val

    def to_dict(self) -> dict:
        return {self.key: self.val}
