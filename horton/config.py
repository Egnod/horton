import os

from sitri import Sitri
from sitri.contrib.yaml import YamlConfigProvider

configurator = Sitri(
    config_provider=YamlConfigProvider(
        yaml_path=os.path.join(os.getcwd(), "config.yml")
    ),
    credential_provider=None,
)

KAFKA_BROKERS = configurator.get_config("kafka.servers", path_mode=True)

MONGO_DATABASE_URI = "mongodb://{username}:{password}@{host}:{port}"
MONGO_DATABASE_NAME = configurator.get_config("mongo.database", path_mode=True)
MONGO_DATABASE_USERNAME = configurator.get_config("mongo.username", path_mode=True)
MONGO_DATABASE_PASSWORD = configurator.get_config("mongo.password", path_mode=True)
MONGO_DATABASE_HOST = configurator.get_config("mongo.host", path_mode=True)
MONGO_DATABASE_PORT = configurator.get_config("mongo.port", path_mode=True)

MONGO_DATABASE_URI_WITH_AUTH = MONGO_DATABASE_URI.format(
    username=MONGO_DATABASE_USERNAME,
    password=MONGO_DATABASE_PASSWORD,
    host=MONGO_DATABASE_HOST,
    port=MONGO_DATABASE_PORT,
)

API_ENDPOINT = configurator.get_config("service.api_endpoint", path_mode=True)
API_KEY = configurator.get_config("service.api_key", path_mode=True)
