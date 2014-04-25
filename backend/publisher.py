#!/usr/bin/env python
import asyncio
import asyncio_redis
import logging

from django.conf import settings


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    # Enable logging
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.getLogger().setLevel(logging.INFO)

    def run():
        print('cow to Redis')
        connection = yield from asyncio_redis.Connection.create(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD)

        while True:
            # Get input (always use executor for blocking calls)
            text = yield from loop.run_in_executor(None, input, 'Enter message: ')

            # Publish value
            try:
                yield from connection.publish('cowchan', text)
                print('Published.')
            except asyncio_redis.Error as e:
                print('Published failed', repr(e))

    loop.run_until_complete(run())


