# import pprint
# import json
import os
import pymongo
from bson.objectid import ObjectId
from app import config


class MediaItemsRepository:
    """A simple class"""

    attribute_names = [
        "id",  # mediaItem ID, not Mongo ID (which is _id)
        "filename",
        "mediaMetadata",
        "mimeType",
        "productUrl",
        "baseUrl",
    ]

    def __init__(self, user_id):
        if not user_id:
            raise Error("must provide a user_id")

        self.user_id = user_id

        client = pymongo.MongoClient(config.MONGODB_URI)
        self.db = client[config.DATABASE]
        self.collection = self.db.media_items

    def get(self, id: int):
        pass

    def create_or_update(self, attributes: dict):
        attributes = {
            k: v
            for (k, v) in attributes.items()
            if k in MediaItemsRepository.attribute_names
        }
        attributes |= {"userId": self.user_id}

        return self.collection.update_one(
            {"id": attributes["id"], "userId": self.user_id},
            {"$set": attributes},
            upsert=True,
        )

    def delete_all(self):
        return self.collection.delete_many({"userId": self.user_id})

    def all(self):
        return (
            self.collection.find({"userId": self.user_id})
            # Order by creationTime ascending, so we can easily identify
            #   the earliest created mediaItem as the original
            .sort("mediaMetadata.creationTime", 1)
        )

    def count(self):
        return self.collection.count_documents({"userId": self.user_id})


class Error(Exception):
    """Base class for exceptions in this module."""

    pass
