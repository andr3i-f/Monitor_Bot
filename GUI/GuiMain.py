import PySimpleGUI as sg
import time
import datetime


class Gui:
    def __init__(self, action_thread, comparer, active_monitors):
        # initializing other required objects
        self.comparer = comparer
        self.action_thread = action_thread

        self.layout = [
            [sg.Text("Active Monitors Below")],
            [sg.Text("\n".join(active_monitors))],
            [sg.Text("STATUS"), sg.Text("NOT RUNNING", key="-status-",
                                        background_color='red')],
            [sg.Button("Run"), sg.Button("Stop"), sg.Exit()]]

        sg.theme('DarkBlue2')

        self.window = sg.Window("Monitors by Andre1", self.layout, size=(250, 250))

    def run(self):
        start = 0
        while True:
            event, values = self.window.read()
            print(event, values)

            if event in (sg.WIN_CLOSED, "Exit"):
                break

            if event == "Run":
                start = time.time()
                self.action_thread.start()
                self.window['-status-'].update("RUNNING", background_color='green')

            if event == "Stop":
                self.action_thread.stop_event.set()
                end = time.time()
                log = f'ENDING TASK at {datetime.datetime.now()} \nRan for {end - start} seconds.'
                self.comparer.bot.update_log(log)
                self.window['-status-'].update("NOT RUNNING", background_color='red')



