import faust


class CollectSecurityOverview(faust.Record):
    symbol: str
    exchange: str
