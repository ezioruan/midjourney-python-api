import multiprocessing
import random
import threading

from config import ACCOUNT_LIST
from midjounery import MidjouneryClient


def get_random_channel_id():
    account = random.choice(ACCOUNT_LIST)
    return account["channel_id"]


def handle_task(client, task_queue):
    print("start handle_task in client", client)
    while True:
        task = task_queue.get()
        print("get task from queue", task)
        client.handle_task(task)
        print("handle_task done", task)


def start_client(account, message_handler, task_queue):
    client = MidjouneryClient(**account, message_handler=message_handler)
    client_run_thread = threading.Thread(target=client.run)
    client_run_thread.start()
    client_handle_task_thread = threading.Thread(
        target=handle_task, args=(client, task_queue)
    )
    client_handle_task_thread.start()
    client_run_thread.join()
    client_handle_task_thread.join()


def distribute_task(task_queue, task):
    channel_id = task.get("channel_id")
    if not channel_id:
        channel_id = get_random_channel_id()
        task["channel_id"] = channel_id
    print("distribute_task", task)
    task_queue.put(task)


def manage_clients(message_handler, clients_ready_event):
    # Start client processes and store client objects
    task_queues = []
    for account in ACCOUNT_LIST:
        task_queue = multiprocessing.Queue()
        p = multiprocessing.Process(
            target=start_client, args=(account, message_handler, task_queue)
        )
        p.start()
        task_queues.append(task_queue)

    # Signal that clients are ready
    clients_ready_event.set()
    return task_queues
