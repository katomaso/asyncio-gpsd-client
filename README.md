# Asycio Gpsd Client

Fork of very well done asyncio-gpsd-client that was unfortunatelly quite out of date.
I just cleaned it up a bit and updated dependencies.

# Install

```shell
pip install gpsd-client-async
```

# Usage

```python
import asyncio

import gpsd_client_async as gpsd

async def main():
    async with gpsd.GpsdClient() as client:
        async for message in client:
            print(message)  # TPV or Sky message

asyncio.run(main())
```
