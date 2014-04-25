import json
import asyncio
import logging

import websockets
import asyncio_redis
from django.conf import settings


RECIEVER_HOST = 'localhost'
RECIEVER_PORT = 8766

logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().setLevel(logging.INFO)


@asyncio.coroutine
def reciever(websocket, uri):

    connection = yield from asyncio_redis.Connection.create(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD)

    websocket_send = websocket.send
    asyncio_redis_Error = asyncio_redis.Error
    REDIS_CHANNEL = 'pos-channel'

    # Create subscriber.
    subscriber = yield from connection.start_subscribe()

    # Subscribe to channel.
    yield from subscriber.subscribe([REDIS_CHANNEL])

    # Inside a while loop, wait for incoming events.
    while True:
        reply = yield from subscriber.next_published()
        yield from websocket_send(reply.value)


def main():
    start_server = websockets.serve(reciever, RECIEVER_HOST, RECIEVER_PORT)
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(start_server)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("exiting...")
    finally:
        server.close()
        loop.close()
        print("...done.")


if __name__ == '__main__':
    main()