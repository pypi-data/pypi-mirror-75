from mongoengine import StringField, IntField, BooleanField, \
                        DateTimeField, ListField, FloatField,\
                        EmbeddedDocumentField, EmbeddedDocumentListField, \
                        DictField, EmbeddedDocument, connect \

from mongoengine.connection import disconnect
import os

class MongoSettings():
    def __init__(self, db_name=None, host=None, port=None):
        self.mongo_user = os.environ.get("MONGO_USER")
        self.mongo_pass = os.environ.get("MONGO_PASS")
        self.mongo_port = port if port!=None else os.environ.get("MONGO_PORT", 27017)
        self.mongo_host = host if host!=None else os.environ.get("MONGO_HOST","host.docker.internal")
        self.mongo_db = db_name if db_name!=None else os.environ.get("MONGO_DB", "topograph_db")
        self.host = f"mongodb://{self.mongo_host}:{self.mongo_port}"

    def connect(self):
        self.client = connect(self.mongo_db, host=self.host, port=self.mongo_port, connect=False)
        return self.client

    def close(self):
        disconnect()
