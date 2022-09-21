from CompareHandler import Compare
from Monitors import CanaryYellowOFFW
from Threads import ActionThread
from GUI import GuiMain


class MonitorMain:
    """Class to manage the behavior and initiations of all monitors"""
    def __init__(self, delay=3):
        self.delay = delay
        self.off_white = CanaryYellowOFFW.OffWhiteMonitor()
        self.comparer = Compare(self.off_white)

        self.active_monitors = [self.off_white.name]

        self.action_thread = ActionThread.Action(1, "Thread1",
                                                 self.off_white,
                                                 self.comparer,
                                                 True, self.delay)

        # Initializing gui
        self.gui = GuiMain.Gui(self.action_thread, self.comparer,
                               self.active_monitors)

    def run(self):
        self.gui.run()


def main():
    handler = MonitorMain()
    handler.run()


if __name__ == "__main__":
    main()
