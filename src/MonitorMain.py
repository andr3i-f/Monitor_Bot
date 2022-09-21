from CompareHandler import Compare
from Monitors import CanaryYellowOFFW
from GUI import GuiMain


class MonitorMain:
    """Class to manage the behavior and initiations of all monitors"""
    def __init__(self, delay=3):
        self.delay = delay
        self.off_white = CanaryYellowOFFW.OffWhiteMonitor()
        self.comparer = Compare(self.off_white)

        self.active_monitors = [self.off_white.name]

        # Initializing gui
        self.gui = GuiMain.Gui(self.off_white, self.comparer, self.active_monitors,
                               self.delay)

    def run(self):
        self.gui.run()


def main():
    handler = MonitorMain()
    handler.run()


if __name__ == "__main__":
    main()
