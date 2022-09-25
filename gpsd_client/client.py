import asyncio

from gpsd_client.schemas import Devices, Response, Version, WatchConfig

POLL = "?POLL;\r\n"
WATCH = "?WATCH={}\r\n"


class GpsdClient:
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    version: Version
    devices: Devices
    watch: WatchConfig

    def __init__(self, host: str, port: int, watch_config: WatchConfig = WatchConfig()):
        self.host = host
        self.port = port

        self.watch_config = watch_config

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

        self.writer.write(WATCH.format(self.watch_config.json(by_alias=True)).encode())
        await self.writer.drain()

        self.version = await self.get_result()
        self.devices = await self.get_result()
        self.watch = await self.get_result()

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()

    async def get_result(self):
        return Response.parse_raw(await self.reader.readline()).__root__

    async def poll(self):
        self.writer.write(POLL.encode())
        await self.writer.drain()
        return await self.get_result()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    def __aiter__(self):
        return self

    async def __anext__(self):
        result = await self.get_result()
        if result.class_ == "TPV":
            return result
        if result.class_ == "SKY":
            self.sky = result
        return await anext(self)
