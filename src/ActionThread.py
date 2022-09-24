import threading
import time
import json


class Action(threading.Thread):
    def __init__(self, thread_id, name, monitors, delay=3):
        super(Action, self).__init__()
        self.thread_id = thread_id
        self.name = name

        self.monitors = monitors
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

                except json.JSONDecodeError:  # Incase server stops allowing requests
                    print('blocked')
                    self.stop_event.set()

                if self.stop_event.is_set():
                    break

                print(f"Done with monitor: {monitor.name}")

        print(f"Exiting thread: {self.name}")


