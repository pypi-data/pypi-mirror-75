import aiohttp
import asyncio
from aio_osservaprezzi.api import API

loop = asyncio.get_event_loop()

SAMPLE = {"town": "Santa Maria Imbaro", "region": "Abruzzo", "province": "CH"}


async def test():
    async with aiohttp.ClientSession() as session:
        api = API(loop, session, data=SAMPLE,)

        data_by_id = await api.get_data_by_id(47715)
        print(data_by_id)


loop.run_until_complete(test())
loop.close()
