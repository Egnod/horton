import os

from sitri import Sitri
from sitri.contrib.system import SystemConfigProvider
from sitri.contrib.yaml import YamlConfigProvider
from sitri.strategy.index_priority import IndexPriorityStrategy

config_providers = (
    SystemConfigProvider(prefix="horton"),
    YamlConfigProvider(
        yaml_path=os.path.join(os.getcwd(), "config.yml"), default_separator="_"
    ),
)

configurator = Sitri(
    config_provider=IndexPriorityStrategy(config_providers),
    credential_provider=None,
)

KAFKA_BROKERS = configurator.get_config("kafka_servers", path_mode=True)

MONGO_DATABASE_URI = "mongodb://{username}:{password}@{host}:{port}"
MONGO_DATABASE_NAME = configurator.get_config("mongo_database", path_mode=True)
MONGO_DATABASE_USERNAME = configurator.get_config("mongo_username", path_mode=True)
MONGO_DATABASE_PASSWORD = configurator.get_config("mongo_password", path_mode=True)
MONGO_DATABASE_HOST = configurator.get_config("mongo_host", path_mode=True)
MONGO_DATABASE_PORT = configurator.get_config("mongo_port", path_mode=True)

MONGO_DATABASE_URI_WITH_AUTH = MONGO_DATABASE_URI.format(
    username=MONGO_DATABASE_USERNAME,
    password=MONGO_DATABASE_PASSWORD,
    host=MONGO_DATABASE_HOST,
    port=MONGO_DATABASE_PORT,
)

API_ENDPOINT = configurator.get_config("service_apiendpoint", path_mode=True)
API_KEY = configurator.get_config("service_apikey", path_mode=True)
