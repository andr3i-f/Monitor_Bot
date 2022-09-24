class Compare:
    """Manage the behavior and actions of comparing, and the response afterwards"""
    def __init__(self, notify_bot):
        self.bot = notify_bot

    def compare_items(self, monitor):
        """Will compare the previous and current items together"""
        print("comparing")
        if monitor.previous_items == monitor.wanted_items:
            print("All is well")
        elif monitor.previous_items != monitor.wanted_items:
            self.find_change(monitor)
            monitor.set_up_flag = True

    def find_change(self, monitor):
        """This will find what has changed from current to previous state"""
        try:
            if len(monitor.wanted_items) == len(monitor.previous_items):
                for idx, item in enumerate(monitor.wanted_items):
                    if item != monitor.previous_items[idx]:

                        if item['AVAIL_SIZES'] != monitor.previous_items[idx]['AVAIL_SIZES'] and item['AVAIL_SIZES']:
                            avail_sizes = '\n'.join([size for size in item['AVAIL_SIZES']
                                                     if size not in monitor.previous_items[idx]['AVAIL_SIZES']])

                            if avail_sizes:  # Makes sure that there are some sizes before it sends a notification
                                self.bot.send_alert(f"{item['NAME']}",
                                                    item['LINK'], f"Available Sizes:\n{avail_sizes}",
                                                    item['IMG'],
                                                    0x29e342)
            else:
                raise IndexError  # Throw index error bc. lens are different, it will raise an index error regardless

        except IndexError:
            if len(monitor.wanted_items) > len(monitor.previous_items):
                # Something was added
                name_list = [i['NAME'] for i in monitor.previous_items]
                print(name_list)

                for item in monitor.wanted_items:
                    if item['NAME'] not in name_list:
                        sizes = '\n'.join(item['AVAIL_SIZES'])
                        self.bot.send_alert(f"{item['NAME']}",
                                            item['LINK'],
                                            f"Available Sizes:\n{sizes}",
                                            item['IMG'],
                                            0xf50000)

            elif len(monitor.wanted_items) < len(monitor.previous_items):
                # Something was removed
                pass

