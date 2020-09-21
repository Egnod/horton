import faust

from horton.config import KAFKA_BROKERS


def get_app():
    return faust.App("horton", broker=KAFKA_BROKERS)
