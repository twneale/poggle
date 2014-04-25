import asyncio
import logging
import asyncio_redis

from django.conf import settings


@asyncio.coroutine
def example():
    # Create connection
    connection = yield from asyncio_redis.Connection.create(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD)

    # Create subscriber.
    subscriber = yield from connection.start_subscribe()

    # Subscribe to channel.
    yield from subscriber.subscribe(['cowchan'])

    # Inside a while loop, wait for incoming events.
    while True:
        reply = yield from subscriber.next_published()
        print('Received: ', repr(reply.value), 'on channel', reply.channel)


if __name__ == '__main__':
    # Enable logging
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().setLevel(logging.INFO)

    # Run loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(example())






