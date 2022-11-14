from comparer import Compare
import ShopifyMonitor
import SupremeMonitor
import FootLockerMonitor
import gui
import webhooks
import json


class MonitorMain:
    """Class to manage the behavior and initiations of all monitors"""
    def __init__(self):
        self.delay = 1
        self.notify_bot = webhooks.DiscordNotify()
        self.comparer = Compare(self.notify_bot)

        with open("config/shopify_websites.json") as f:
            # Get all websites to monitor from config shopify_websites file
            websites = json.load(f)

        with open("config/keywords.json") as f:
            # Get all keywords that monitors will use
            keywords = json.load(f)

        with open("config/unwanted.json") as f:
            # Get all unwanted words that monitors will not include
            unwanted = json.load(f)

        self.active_monitors = []
        for website in websites:
            # Create objects for all the websites in the config file
            self.active_monitors.append(
                ShopifyMonitor.Monitor(website['link'],
                                       website['name'],
                                       website['collections'],
                                       keywords, unwanted,
                                       self.comparer, self.notify_bot)
            )

        self.active_monitors.append(SupremeMonitor.SupremeMonitor("Supreme", 
                                    self.notify_bot, 3))
        self.active_monitors.append(FootLockerMonitor.FootLockerMonitor("Footlocker",
                                    self.notify_bot, keywords, 3))

        # Initialize gui
        self.gui = gui.Gui(self.comparer, self.active_monitors,
                           self.delay, self.notify_bot)

    def run(self):
        self.gui.run()


def main():
    handler = MonitorMain()
    handler.run()


if __name__ == "__main__":
    main()
