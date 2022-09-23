import json
from DiscordBot import NotifyBot


class Compare:
    """Manage the behavior and actions of comparing, and the response afterwards"""
    def __init__(self, monitor, notify_bot):
        self.monitor = monitor
        self.current_items = self.monitor.wanted_items
        self.previous_items = None
        self.set_up_flag = True

        self.bot = notify_bot

    def handler(self):
        self.set_up()
        self.compare_items()

    def set_up(self):
        """Initializes the first time set up"""
        self.current_items = self.monitor.wanted_items
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
        self.current_items = self.monitor.wanted_items

        if self.previous_items == self.current_items:
            print("All is well")
        elif self.previous_items != self.current_items:
            self.find_change()
            self.set_up_flag = True

    def find_change(self):
        """This will find what has changed from current to previous state"""
        try:
            if len(self.current_items) == len(self.previous_items):
                for idx, item in enumerate(self.current_items):
                    if item != self.previous_items[idx]:

                        if item['AVAIL_SIZES'] != self.previous_items[idx]['AVAIL_SIZES']:
                            avail_sizes = '\n'.join([size for size in item['AVAIL_SIZES']
                                                     if size not in self.previous_items[idx]['AVAIL_SIZES']])

                            self.bot.send_alert(f"{item['NAME']}",
                                                item['LINK'], f"Available Sizes:\n{avail_sizes}",
                                                item['IMG'],
                                                0x29e342)
            else:
                raise IndexError  # Throw this index error because lens are different

        except IndexError:
            if len(self.current_items) > len(self.previous_items):
                # Something was added
                name_list = [i['NAME'] for i in self.previous_items]
                print(name_list)

                for item in self.current_items:
                    if item['NAME'] not in name_list:
                        sizes = '\n'.join(item['AVAIL_SIZES'])
                        self.bot.send_alert(f"{item['NAME']}",
                                            item['LINK'],
                                            f"Available Sizes:\n{sizes}",
                                            item['IMG'],
                                            0xf50000)

            elif len(self.current_items) < len(self.previous_items):
                # Something was removed
                pass

