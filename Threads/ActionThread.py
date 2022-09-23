import threading
import time
import json


class Action(threading.Thread):
    def __init__(self, thread_id, name, compares, monitors, delay=3):
        super(Action, self).__init__()
        self.thread_id = thread_id
        self.name = name

        self.monitors = monitors
        self.compares = compares
        self.delay = delay

        self.daemon = True

        self.stop_event = threading.Event()

    def run(self):
        print(f"Starting thread: {self.name}")

        while not self.stop_event.is_set():
            print('Checking')

            for idx in range(len(self.monitors)):
                try:
                    self.monitors[idx].search_wanted_items()
                    self.compares[idx].handler()
                except json.JSONDecodeError:
                    pass

            time.sleep(self.delay)
        print(self.is_alive())
        print(f"Exiting thread: {self.name}")


