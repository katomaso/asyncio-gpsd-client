import asyncio
import json


class GpsdClient:
    POLL = b"?POLL;\r\n"

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

        self.writer.write('?WATCH={"enable":true}\n'.encode())

        self.version = json.loads(await self.reader.readline())
        self.devices = json.loads(await self.reader.readline())
        self.watch = json.loads(await self.reader.readline())

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.writer.close()

    async def poll(self):
        self.writer.write(self.POLL)
        return json.loads(await self.reader.readline())

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self.poll()
