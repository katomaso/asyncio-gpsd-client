import asyncio
import json

POLL = b"?POLL;\r\n"
WATCH = b'?WATCH={"enable":true,"json":true}\r\n'


class GpsdClient:
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

        self.writer.write(WATCH)

        self.version = json.loads(await self.reader.readline())
        self.devices = json.loads(await self.reader.readline())
        self.watch = json.loads(await self.reader.readline())

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    def __aiter__(self):
        self.writer.write(POLL)
        return self

    async def __anext__(self):
        return json.loads(await self.reader.readline())
