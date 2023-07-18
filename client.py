# -* coding:UTF-8 -*
# !/usr/bin/env python
import json
import os
import pprint
import time
import traceback
import config

import redis

pp = pprint.PrettyPrinter(depth=4)


redis_client = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD,
    db=config.REDIS_DB,
)

print(f"connect to redis {config.REDIS_HOST} success, start to listen")


def start_imagine():
    task = {"cmd": "imagine", "args": ["a little cat"]}
    redis_client.rpush(config.REDIS_TASK_CHANNEL, json.dumps(task))


def main():
    # Connect to Redis

    while True:
        # Block until a message is available
        _, message = redis_client.blpop(config.REDIS_NOTIFY_CHANNEL)
        print("message", message)

        # Extract message id and content
        try:
            message_decoded = json.loads(message.decode("utf-8"))
            pp.pprint(message_decoded)
        except Exception:
            print("message decode error")
            traceback.print_exc()


if __name__ == "__main__":
    main()
