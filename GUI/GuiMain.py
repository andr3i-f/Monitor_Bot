import PySimpleGUI as sg
import time
import datetime

class Gui:
    def __init__(self, action_thread, comparer):
        self.layout = [
            [sg.Text("Placeholder Text Weweoweowo")],
            [sg.Button("Run"), sg.Button("Stop"), sg.Exit()]]

        self.window = sg.Window("Monitors by Andre1", self.layout)
        self.comparer = comparer
        self.action_thread = action_thread

    def run(self):
        while True:
            event, values = self.window.read()
            print(event, values)

            if event in (sg.WIN_CLOSED, "Exit"):
                break
            if event == "Run":
                start = time.time()
                self.action_thread.start()
            if event == "Stop":
                self.action_thread.stop_event.set()
                end = time.time()
                log = f'ENDING TASK at {datetime.datetime.now()} \nRan for {end - start} seconds.'
                self.comparer.bot.update_log(log)



