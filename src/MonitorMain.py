from CompareHandler import Compare
from Monitors import ShopifyMonitor
from GUI import GuiMain
from DiscordBot import NotifyBot

keywords = ["dunk", "off-white", "off white", "jordan", "jordan retro", "retro",
            "dunk low", "dunk high", "jordan-retro", "yeezy"]


class MonitorMain:
    """Class to manage the behavior and initiations of all monitors"""
    def __init__(self, delay=2):
        self.delay = delay
        self.notify_bot = NotifyBot.DiscordNotify()

        self.off_white = ShopifyMonitor.Monitor("https://gallery.canary---yellow.com/",
                                                "Canary-Yellow", keywords)
        self.undefeated = ShopifyMonitor.Monitor("https://undefeated.com/",
                                                 "Undefeated", keywords)
        self.shoe_palace = ShopifyMonitor.Monitor("https://www.shoepalace.com/", "Shoe-Palace", keywords)

        self.off_white_comparer = Compare(self.off_white, self.notify_bot)
        self.undefeated_comparer = Compare(self.undefeated, self.notify_bot)
        self.shoe_palace_comparer = Compare(self.shoe_palace, self.notify_bot)

        self.active_monitors = [self.off_white, self.undefeated, self.shoe_palace]
        self.active_comparer = [self.off_white_comparer, self.undefeated_comparer, self.shoe_palace_comparer]

        # Initializing gui
        self.gui = GuiMain.Gui(self.active_comparer, self.active_monitors,
                               self.delay, self.notify_bot)

    def run(self):
        self.gui.run()


def main():
    handler = MonitorMain()
    handler.run()


if __name__ == "__main__":
    main()
