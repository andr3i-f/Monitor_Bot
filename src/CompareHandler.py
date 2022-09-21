import json
from DiscordBot import NotifyBot


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

                    if item['NAME'] != self.previous_items[idx]['NAME']:
                        self.bot.send_alert(f"{item['NAME']} has changed names, "
                                            f"previous: {self.previous_items[idx]['NAME']}",
                                            item['LINK'],
                                            0xf705cb)

                    elif item['PRICE'] != self.previous_items[idx]['PRICE']:
                        self.bot.send_alert(f"{item['NAME']} has changed prices! Possible restock!",
                                            item['LINK'],
                                            0x29e342)

                    elif item['IN-STOCK'] != self.previous_items[idx]['IN-STOCK']:
                        if item['IN-STOCK'].lower() == 'buy':
                            self.bot.send_alert(f"{item['NAME']} has restocked!",
                                                item['LINK'],
                                                0xedf500)

                    elif item['LINK'] != self.previous_items[idx]['LINK']:
                        self.bot.send_alert(f"{item['NAME']} has changed links! New link below!",
                                            item['LINK'],
                                            0x006ef5)

        except IndexError:
            if len(self.current_items) > len(self.previous_items):
                # Something was added
                name_list = [i['NAME'] for i in self.previous_items]
                link_list = [i['LINK'] for i in self.previous_items]
                for item in self.current_items:
                    if item['NAME'] not in name_list and item['LINK'] not in link_list:
                        self.bot.send_alert(f"{item['NAME']} has just been added!",
                                            item['LINK'],
                                            0xf50000)

            elif len(self.current_items) < len(self.previous_items):
                # Something was removed
                pass

