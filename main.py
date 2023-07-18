import json
import multiprocessing
import os
import threading
import config

import redis

from midjounery_manager import distribute_task, manage_clients


redis_client = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD,
    db=config.REDIS_DB,
)


def send_message(message_id, message):
    message = json.dumps(message)
    print("Send message to Redis", message)
    redis_client.rpush(config.REDIS_NOTIFY_CHANNEL, message)


def listen_to_redis(ready_event, task_queues):
    # Wait for the signal that clients are ready
    ready_event.wait()

    while True:
        _, task = redis_client.blpop(config.REDIS_TASK_CHANNEL)
        print("get task from Redis", task)
        task = json.loads(task.decode("utf-8"))
        for task_queue in task_queues:
            distribute_task(task_queue, task)


if __name__ == "__main__":
    # Event to signal that clients are ready
    clients_ready_event = threading.Event()

    # Start managing client processes and get the list of task queues
    task_queues = manage_clients(send_message, clients_ready_event)

    # Thread for listening to Redis and distributing tasks
    redis_listener_thread = threading.Thread(
        target=listen_to_redis, args=(clients_ready_event, task_queues)
    )
    redis_listener_thread.start()

    # Wait for Redis listener thread to finish
    redis_listener_thread.join()
