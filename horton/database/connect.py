from motor import motor_asyncio

from horton.config import MONGO_DATABASE_NAME, MONGO_DATABASE_URI_WITH_AUTH


class Mongo:
    def __init__(self):
        self._client = motor_asyncio.AsyncIOMotorClient(
            MONGO_DATABASE_URI_WITH_AUTH, connect=True, maxPoolSize=200
        )

        self._db = self._client[MONGO_DATABASE_NAME]

    @property
    def db(self):
        return self._db

    @property
    def client(self):
        return self._client

    def close(self):
        self._client.close()


mongo_instanse = Mongo()
mongo_client = mongo_instanse.client
mongo_db = mongo_instanse.db
