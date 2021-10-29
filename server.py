import asyncio

from functools import partial, wraps
from quart import Quart, websocket
from random import random


app = Quart(__name__)


SPEC = dict(light=4, humidity=17)
LOCK = asyncio.Lock()


@app.websocket('/data')
async def datasocket():
    data = {k: 0.5 for k in SPEC}
    while True:
        async with LOCK:
            data = {k: v + 0.05 * random() - 0.025 for k, v in data.items()}
            await websocket.send_json(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
