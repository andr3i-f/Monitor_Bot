from comparer import Compare
import ShopifyMonitor
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

        self.active_monitors = []
        for website in websites:
            # Create objects for all the websites in the config file
            self.active_monitors.append(
                ShopifyMonitor.Monitor(website['link'],
                                       website['name'],
                                       website['collections'],
                                       keywords,
                                       self.comparer)
            )

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
