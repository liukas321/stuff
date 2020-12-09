from queue import Queue
from threading import Thread


def __ui_job(q: Queue):
    text = "Issue a command:\n"
    answer = input(text)
    q.put(answer)


def ui_worker(q: Queue = None) -> (Thread, Queue):
    q = q or Queue()
    worker = Thread(target=__ui_job, args=[q])
    worker.start()
    return worker, q
