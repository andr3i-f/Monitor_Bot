class Compare:
    """Manage the behavior and actions of comparing, and the response afterwards"""
    def __init__(self, notify_bot):
        self.bot = notify_bot

    def compare_items(self, current_items, previous_items):
        """Will compare the previous and current items together"""

        if previous_items == current_items:
            return False

        elif previous_items != current_items:
            self.find_change(current_items, previous_items)
            return True

    def find_change(self, current_items, previous_items):
        """This will find what has changed from current to previous state"""
        try:
            if len(current_items) == len(previous_items):
                for idx, item in enumerate(current_items):
                    if item != previous_items[idx]:

                        if item['AVAIL_SIZES'] != previous_items[idx]['AVAIL_SIZES'] and item['AVAIL_SIZES']:
                            avail_sizes = [size for size in item['AVAIL_SIZES']
                                           if size not in previous_items[idx]['AVAIL_SIZES']]

                            if avail_sizes:  # Makes sure that there are some sizes before it sends a notification
                                self.bot.send_alert_shopify(f"{item['NAME']}",
                                                    item['LINK'],
                                                    "Restock",
                                                    avail_sizes,
                                                    item['IMG'],
                                                    0x29e342)
            else:
                raise IndexError  # Throw index error bc. lens are different, it will raise an index error regardless

        except IndexError:
            if len(current_items) > len(previous_items):
                # Something was added
                name_list = [i['NAME'] for i in previous_items]

                for item in current_items:
                    if item['NAME'] not in name_list:
                        self.bot.send_alert_shopify(f"{item['NAME']}",
                                            item['LINK'],
                                            "New Item",
                                            item['AVAIL_SIZES'],
                                            item['IMG'],
                                            0xf50000)

            elif len(current_items) < len(previous_items):
                # Something was removed
                pass

