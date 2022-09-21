
# from documentMongoDB import *
from bson import ObjectId


class Document:
    def __init__(self, connection):
        self.cluster = connection  # MongoDB connection to cluster
        self.db = None
        self.collection = None
        self.doc_name = None
        # mydb = self.cluster.list_database_names()  # nazwy baz danych

        # print(mydb)
# ---------- db config -------------------------

    def create_db(self, name):
        self.db = self.cluster[f"{name}"]

    def set_db(self, db):
        try:
            if isinstance(db, str):
                self.db = self.cluster[f"{db}"]
            else:
                raise TypeError
        except:
            print("-----Wrong variable type for db name-----")


# ----------------------- operations on collection --------------


    def set_collection(self, collection):
        if isinstance(collection, str):
            self.collection = self.db[f"{collection}"]

    def create_collection_in_db(self, collection):
        if isinstance(collection, str):

            self.collection = self.db[f"{collection}"]

    def drop_collection(self, collection):
        if isinstance(collection, str):

            collection = self.db[f"{collection}"]
            collection.drop()

    def show_collection_names(self):
        collection = self.db.list_collection_names()
        return collection

# ---------------------- operation on docs---------------------------

    def insert_many_doc(self, document):
        self.collection.insert_many(document)

    def insert_one_doc(self, document):
        # print(document)
        try:
            if isinstance(document, dict):
                if ObjectId.is_valid(str(document["_id"])):
                    # print(document)
                    self.collection.insert_one(document)
                else:
                    document["_id"] = self._set_id()
                    self.collection.insert_one(document)
            else:
                
                raise TypeError
        except Exception as e:
            print(e)

    def _set_id(self):
        _id = ObjectId()
        return _id

    def _take_id(self, id):
        try:
            _id = ObjectId(id)

            return _id
        except Exception:
            print("podaj poprawne id")

    def update_doc(self, id, patch):
        try:
            if isinstance(patch, dict):
                _id = self._take_id(id)
                self.collection.update_one({"_id": _id}, patch)
        except:
            pass

    def delete_doc(self, id, config):
        try:
            if isinstance(config, dict):
                _id = self._take_id(id)
                self.collection.delete_one({"_id": _id}, config)
        except:
            pass

    def change_values_doc(self, id, keys={}):
        try:
            if isinstance(keys, dict):
                _id = self._take_id(id)
                self.collection.replace_one({"_id": _id}, keys)
        except:
            pass

    def show_doc(self, config={}):
        if isinstance(config, dict):
            data = self.collection.find_one(config)
            return data

    def count_in_doc(self, config={}):
        if isinstance(config, dict):
            count = self.collection.count_documents(filter=config)
            return count
