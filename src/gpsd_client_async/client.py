import asyncio
from typing import Union

from .messages import TPV, Devices, Response, Sky, Version, Watch, GSPD_MESSAGE

POLL = "?POLL;\r\n"
WATCH = "?WATCH={}\r\n"


class GpsdClient:
    devices: Devices
    watch: Watch
    version: Version

    _host: str
    _port: int
    _reader: asyncio.StreamReader
    _writer: asyncio.StreamWriter

    def __init__(self, host: str = "127.0.0.1", port: int = 2947, watch_config: Watch = Watch()):
        self._host = host
        self._port = port
        self.watch_config = watch_config

    async def connect(self):
        self._reader, self._writer = await asyncio.open_connection(self._host, self._port)

        self._writer.write(WATCH.format(self.watch_config.json(by_alias=True, exclude={"class_"})).encode())
        await self._writer.drain()

        self.version = await self.get_result()
        self.devices = await self.get_result()
        self.watch = await self.get_result()

    async def close(self):
        self._writer.close()
        await self._writer.wait_closed()

    async def get_result(self) -> GSPD_MESSAGE:
        return Response.parse_raw(await self._reader.readline()).message

    async def poll(self) -> GSPD_MESSAGE:
        self._writer.write(POLL.encode())
        await self._writer.drain()
        return await self.get_result()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    def __aiter__(self):
        return self

    async def __anext__(self) -> Union[TPV, Sky]:
        return await self.get_result()
