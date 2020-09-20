from horton.database.connect import mongo_db


class BaseMongoCRUD:
    db = mongo_db
    collection = NotImplemented

    @classmethod
    async def find_one(cls, query: dict):
        return await cls.db[cls.collection].find_one(
            filter=query,
        )

    @classmethod
    async def find_many(cls, query: dict, options: dict = None, sort: list = None):
        items = cls.db[cls.collection].find(query, options)

        if sort:
            items.sort(sort)

        return [i async for i in items]

    @classmethod
    async def insert_one(cls, payload: dict, options: dict = None):
        return await cls.db[cls.collection].insert_one(payload, options)

    @classmethod
    async def insert_many(cls, payload: list, options: dict = None):
        return await cls.db[cls.collection].insert_many(
            payload,
            options,
        )

    @classmethod
    async def update_one(
        cls, query: dict, payload: dict, with_set_option: bool = True, **kwargs
    ):
        payload = {"$set": payload} if with_set_option else payload
        return await cls.db[cls.collection].update_one(query, payload, **kwargs)

    @classmethod
    async def update_many(
        cls, query: dict, payload: dict, with_set_option: bool = True, **kwargs
    ):
        payload = {"$set": payload} if with_set_option else payload
        return [
            i
            async for i in cls.db[cls.collection].update_many(
                query,
                payload,
                **kwargs,
            )
        ]

    @classmethod
    async def delete_one(cls, query: dict, **kwargs):
        return await cls.db[cls.collection].delete_one(query, **kwargs)

    @classmethod
    async def delete_many(cls, query: dict, **kwargs):
        return await cls.db[cls.collection].delete_many(query, **kwargs)

    @classmethod
    async def aggregate(cls, pipeline: list, **kwargs):
        return [i async for i in cls.db[cls.collection].aggregate(pipeline, **kwargs)]
