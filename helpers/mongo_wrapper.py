from typing import List
from classes.to_do_item import Item
from bson.objectid import ObjectId
from datetime import datetime
import pymongo
import os


class MongoWrapper:
    def __init__(self, database_name: str):
        client = self._create_client(database_name)
        self._db = client.db

    @staticmethod
    def _create_client(database_name: str):
        username = os.environ['USERNAME']
        password = os.environ['PASSWORD']
        mongo_url = os.environ['MONGO_URL']
        return pymongo.MongoClient(f"mongodb+srv://{username}:{password}@{mongo_url}/{database_name}?retryWrites=true&w=majority")

    def get_items(self) -> List[Item]:
        cards = self._get_cards()
        items = []
        for card in cards.find():
            item = Item(card)
            if not item.deleted:
                items.append(item)
        return items

    def _get_cards(self):
        return self._db.cards

    def create_new_item(self, title: str, description: str, due_date):
        new_card = {
            "name": title,
            "desc": description,
            "due": due_date,
            "deleted": False,
            "status": "To Do",
            "completedOn": ""
        }
        return self._db.cards.insert_one(new_card)

    def move_item_to_doing(self, item_id: int):
        new_value = {"$set": {"status": "Doing"}}
        return self._update_for_id(item_id, new_value)

    def move_item_to_done(self, item_id: int):
        new_value = {"$set": {"status": "Done", "completedOn": datetime.now()}}
        return self._update_for_id(item_id, new_value)

    def archive_item(self, item_id: int):
        new_value = {"$set": {"status": "Deleted", "deleted": True}}
        return self._update_for_id(item_id, new_value)

    def _update_for_id(self, item_id, new_values):
        query = {"_id": ObjectId(item_id)}
        print(item_id)
        return self._db.cards.update_one(query, new_values)

    def drop_database(self):
        self._db.cards.drop()

    @classmethod
    def create_database(cls, name: str) -> "MongoWrapper":
        return MongoWrapper(name)


if __name__ == "__main__":
    x = MongoWrapper("")
    x.create_database(name="test")
