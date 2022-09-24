import threading
import time
import json


class Action(threading.Thread):
    def __init__(self, thread_id, name, comparer, monitors, delay=3):
        super(Action, self).__init__()
        self.thread_id = thread_id
        self.name = name

        self.monitors = monitors
        self.comparer = comparer
        self.delay = delay

        self.daemon = True

        self.stop_event = threading.Event()

    def run(self):
        print(f"Starting thread: {self.name}")

        while not self.stop_event.is_set():
            print('Checking')

            if True in [val.stop_monitor for val in self.monitors]:
                break

            for monitor in self.monitors:
                try:
                    monitor.search_wanted_items()
                    self.comparer.compare_items(monitor)
                    time.sleep(self.delay)

                except json.JSONDecodeError:  # Incase server stops allowing requests
                    break

        print(self.is_alive())
        print(f"Exiting thread: {self.name}")


