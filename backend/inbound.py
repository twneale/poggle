import json
import asyncio
import logging

import websockets
import asyncio_redis
from django.conf import settings


RECIEVER_HOST = 'localhost'
RECIEVER_PORT = 8765

logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().setLevel(logging.INFO)


@asyncio.coroutine
def reciever(websocket, uri):

    connection = yield from asyncio_redis.Connection.create(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD)

    websocket_recv = websocket.recv
    asyncio_redis_Error = asyncio_redis.Error
    REDIS_CHANNEL = 'pos-channel'

    while True:
        text = yield from websocket_recv()
        try:
            yield from connection.publish(REDIS_CHANNEL, text)
        except asyncio_redis_Error as e:
            # Don't care if we lose a signal or two.
            pass


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