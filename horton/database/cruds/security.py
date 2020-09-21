from horton.database.cruds.base import BaseMongoCRUD


class SecurityCRUD(BaseMongoCRUD):
    collection = "securities"
