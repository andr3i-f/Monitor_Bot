import threading
import time


class Action(threading.Thread):
    def __init__(self, thread_id, name, monitor, comparer, delay=3):
        super(Action, self).__init__()
        self.thread_id = thread_id
        self.name = name

        self.monitor = monitor
        self.comparer = comparer
        self.delay = delay

        self.daemon = True

        self.stop_event = threading.Event()

    def run(self):
        print(f"Starting thread: {self.name}")

        while not self.stop_event.is_set():
            print('Checking')
            self.monitor.find_shoes()
            self.comparer.handler()
            time.sleep(self.delay)
        print(self.is_alive())
        print(f"Exiting thread: {self.name}")


