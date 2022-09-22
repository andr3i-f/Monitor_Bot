import PySimpleGUI as sg
import time
import datetime
from Threads import ActionThread


class Gui:
    def __init__(self, monitor, comparer, active_monitors, delay):
        # initializing other required objects
        self.monitor = monitor
        self.comparer = comparer
        self.delay = delay

        self.layout = [
            [sg.Text("Active Monitors Below")],
            [sg.Text("\n".join(active_monitors))],
            [sg.Text("Broadcast a message:"), sg.InputText(key="broadcastMSG")],
            [sg.Text("STATUS"), sg.Text("NOT RUNNING", key="-status-", background_color='red')],
            [sg.Button("Run"), sg.Button("Stop", disabled=True), sg.Exit(button_text='Exit')]]

        sg.theme('DarkBlue2')

        self.window = sg.Window("Monitors by Andrei", self.layout, size=(300, 150), finalize=True)
        self.window['broadcastMSG'].bind("<Return>", "_Enter")

    def run(self):
        start = 0
        action_thread = None
        while True:
            event, values = self.window.read()
            # print(event, values)

            if event in (sg.WIN_CLOSED, "Exit"):
                break

            if event == "broadcastMSG" + "_Enter" and values['broadcastMSG']:
                self.comparer.bot.broadcast("Developer Update", values['broadcastMSG'])

            if event == "Run":
                action_thread = ActionThread.Action(1, "Thread1", self.monitor, self.comparer, self.delay)
                start = time.time()
                action_thread.start()

                log = "```"
                log += f"Setting up at: \n{datetime.datetime.now()}"
                log += "```"
                self.comparer.bot.update_log(log)

                self.window['-status-'].update("RUNNING", background_color='green')
                self.window['Run'].update(disabled=True)
                self.window['Stop'].update(disabled=False)
                self.window['Exit'].update(disabled=True)

            if event == "Stop":
                action_thread.stop_event.set()
                end = time.time()

                log = "```"
                log += f'Ending task at: \n{datetime.datetime.now()} \nRan for {end - start} seconds.'
                log += "```"

                self.comparer.bot.update_log(log)
                self.window['-status-'].update("NOT RUNNING", background_color='red')
                self.window['Run'].update(disabled=False)
                self.window['Stop'].update(disabled=True)
                self.window['Exit'].update(disabled=False)



