# -* coding:UTF-8 -*
# !/usr/bin/env python
import json
import os
import pprint

import redis
import config

pp = pprint.PrettyPrinter(depth=4)


redis_client = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD,
    db=config.REDIS_DB,
)


def start_imagine():
    task1 = {"cmd": "imagine", "args": ["a little boy and girl"]}
    print("imagine", task1)
    redis_client.rpush(config.REDIS_TASK_CHANNEL, json.dumps(task1))
    # task2 = {
    #    "cmd": "interact",
    #    "channel_id": "1099614488631726142",
    #    "args": ["1104986052114001931", "U1"],
    # }
    # print("interact", task2)
    # redis_client.rpush(config.REDIS_TASK_CHANNEL, json.dumps(task2))


def main():
    start_imagine()


if __name__ == "__main__":
    main()
