import json
from DiscordBot import NotifyBot
import datetime


class Compare:
    """Manage the behavior and actions of comparing, and the response afterwards"""
    def __init__(self, class_obj):
        self.monitor = class_obj
        self.current_items = class_obj.shoes
        self.previous_items = None
        self.set_up_flag = True

        self.bot = NotifyBot.DiscordNotify()

    def handler(self):
        self.set_up()
        self.compare_items()

    def set_up(self):
        """Initializes the first time set up"""
        if self.set_up_flag:
            # print("SETTING UP")
            with open(f'../Data/{self.monitor.name}_previous_data.json', 'w') as f:
                json.dump(self.current_items, f, indent=4)
            with open(f'../Data/{self.monitor.name}_previous_data.json', 'r') as f:
                self.previous_items = json.load(f)

            self.set_up_flag = False

    def set_up_testing(self):
        if self.set_up_flag:
            with open(f'../Data/{self.monitor.name}_previous_data.json', 'r') as f:
                self.previous_items = json.load(f)

            self.set_up_flag = False

    def compare_items(self):
        """Will compare the previous and current items together"""
        if self.previous_items == self.current_items:
            print("All is well")
        elif self.previous_items != self.current_items:
            self.find_change()
            self.set_up_flag = True

    def find_change(self):
        """This will find what has changed from current to previous state"""
        try:
            for idx, item in enumerate(self.current_items):
                if item != self.previous_items[idx]:
                    response = None
                    if item['NAME'] != self.previous_items[idx]['NAME']:
                        response = f"{self.previous_items[idx]['NAME']} has changed "
                        response += f"it's name to: {item['NAME']}"

                    elif item['PRICE'] != self.previous_items[idx]['PRICE']:
                        response = f"{self.previous_items[idx]['NAME']} has changed "
                        response += f"it's price to: {item['PRICE']}"

                    elif item['IN-STOCK'] != self.previous_items[idx]['IN-STOCK']:
                        if item['IN-STOCK'].lower() == 'buy':
                            response = f"{self.previous_items[idx]['NAME']} has restocked!"

                    elif item['LINK'] != self.previous_items[idx]['LINK']:
                        response = f"{self.previous_items[idx]['NAME']} has changed "
                        response += f"it's link to {item['LINK']}"

                    if response:
                        self.bot.send_alert(response)

        except IndexError:
            response = None
            if len(self.current_items) > len(self.previous_items):
                # Something was added
                for item in self.current_items:
                    if item not in self.previous_items:
                        response = f"{item['NAME']} has just been added!"
                        response += f"\nLink: {item['LINK']}"

            elif len(self.current_items) < len(self.previous_items):
                # Something was removed
                pass

            if response:
                self.bot.send_alert(response)
