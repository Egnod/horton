from typing import AsyncIterable

import aiohttp
from faust import StreamT
from loguru import logger

from horton.alphavantage import AlphaVantageClient
from horton.app import get_app
from horton.config import API_KEY
from horton.database.cruds.security import SecurityCRUD
from horton.records import CollectSecurityOverview

app = get_app()

collect_securities_topic = app.topic("collect_securities", internal=True, partitions=2)
collect_security_overview_topic = app.topic(
    "collect_security_overview", internal=True, value_type=CollectSecurityOverview
)


@app.agent(collect_security_overview_topic)
async def collect_security_overview(
    stream: StreamT[CollectSecurityOverview],
) -> AsyncIterable[bool]:
    async with aiohttp.ClientSession() as session:
        async for event in stream:
            logger.info(
                "Start collect security [{symbol}] overview", symbol=event.symbol
            )

            client = AlphaVantageClient(session, API_KEY)

            security_overview = await client.get_security_overview(event.symbol)

            await SecurityCRUD.update_one({"symbol": event.symbol, "exchange": event.exchange}, security_overview)

            yield True


@app.agent(collect_securities_topic)
async def collect_securities(stream: StreamT[None]) -> AsyncIterable[bool]:
    async with aiohttp.ClientSession() as session:
        async for _ in stream:
            logger.info("Start collect securities")

            client = AlphaVantageClient(session, API_KEY)

            securities = await client.get_securities()

            for security in securities:
                await SecurityCRUD.update_one(
                    {"symbol": security["symbol"], "exchange": security["exchange"]},
                    security,
                    upsert=True,
                )

                await collect_security_overview.cast(
                    CollectSecurityOverview(symbol=security["symbol"], exchange=security["exchange"])
                )

            yield True


@app.command()
async def start_collect_securities():
    """Collect securities and overview."""

    await collect_securities.cast()
