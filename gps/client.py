import asyncio
import json
from gps.models import WatchConfig

POLL = "?POLL;\r\n"
WATCH = "?WATCH={}\r\n"


class GpsdClient:
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter

    def __init__(self, host: str, port: int, watch_config: WatchConfig = WatchConfig()):
        self.host = host
        self.port = port

        self.watch_config = watch_config

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

        self.writer.write(WATCH.format(self.watch_config.json(by_alias=True)).encode())

        self.version = json.loads(await self.reader.readline())
        self.devices = json.loads(await self.reader.readline())
        self.watch = json.loads(await self.reader.readline())

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()

    def begin_polling(self):
        self.writer.write(POLL.encode())

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    def __aiter__(self):
        self.begin_polling()
        return self

    async def __anext__(self):
        result = json.loads(await self.reader.readline())
        if result["class"] == "TPV":
            return result
        if result["class"] == "SKY":
            self.sky = result
        return await self.__anext__()
