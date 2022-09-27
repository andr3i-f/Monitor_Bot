import threading
import time
import json


class Action(threading.Thread):
    def __init__(self, thread_id, name, monitors, bot):
        super(Action, self).__init__()
        self.thread_id = thread_id
        self.name = name

        self.monitors = monitors
        self.bot = bot

        self.daemon = True

        self.stop_event = threading.Event()

    def run(self):
        print(f"Starting thread: {self.name}")

        while not self.stop_event.is_set():
            if self.stop_event.is_set():
                break

            print('Checking')

            for monitor in self.monitors:

                monitor.search_wanted_items()
                
                if self.stop_event.is_set():
                    break

                print(f"Done with monitor: {monitor.name}\n")

        print(f"Exiting thread: {self.name}")


