import random
import requests
import json
import time
from fp.fp import FreeProxy
from webhooks import DiscordNotify

class FootLockerMonitor:
    """Class to initiate and manage the behavior of this monitor"""
    def __init__(self, name, bot, keywords, delay):
        self.name = name
        self.bot = bot
        self.keywords = keywords

        self.current_items = []
        self.all_previous_items = ['a', 'b', 'c', 'd']

        self.set_up_flag = True

        self.blocked = False
        self.timeout_timer = None

        self.delay = delay

        self.idx = 0

        with open('config/user_agents.json') as f:
            self.user_agents = json.load(f)

        with open('config/footlocker_api.json') as f:
            self.api_urls = json.load(f)

    """
    SKU
    NAME
    PRICE
    IMAGE
    """
    
    def search_wanted_items(self):
        """Adds all products with keywords"""
        self.idx = 0
        for api in self.api_urls:
            self.current_items = []
            headers = {'User-Agent':random.choice(self.user_agents)}
            
            req_url = requests.get(api, headers=headers)

            #print(req_url.status_code)

            if (req_url.status_code == 529):
                return 0

            print(f"Footlocker Code = {req_url.status_code}")

            all_products = json.loads(req_url.text)['products']

            for product in all_products:
                self.w_item = {}
                self.w_item['SKU'] = product['sku']
                self.w_item['NAME'] = product['name']
                self.w_item['PRICE'] = product['price']['value']
                self.w_item['IMAGE'] = product['images'][0]['url']
                self.w_item['LINK'] = f"https://footlocker.com/product/~/{self.w_item['SKU']}.html"

                self.current_items.append(self.w_item)

                #print(self.w_item['NAME'])


                """self.bot.send_alert_footlocker(self.w_item['LINK'], self.w_item['IMAGE'],
                                self.w_item['SKU'], self.w_item['PRICE'],
                                self.w_item['NAME']) """  # debug

            if self.set_up_flag:
                self.all_previous_items[self.idx] = self.current_items[:]
                

            print(len(self.current_items), len(self.all_previous_items[self.idx]))
            if self.all_previous_items[self.idx] != self.current_items:
                # Something changed, look for error
                pass

            self.idx += 1

            time.sleep(self.delay)
            
        self.set_up_flag = False
    
    def compare_items(self):
        """Compares items to find change"""
        try:
            if len(self.current_items) != len(self.all_previous_items[self.idx]):
                raise IndexError  # Raise error because it will reach it eventually
            
            elif len(self.current_items) == len(self.all_previous_items[self.idx]):
                for item in self.current_items:

                    if item not in self.all_previous_items[self.idx]:
                        self.bot.send_alert_footlocker(item['LINK'], item['IMAGE'],
                                                        item['SKU'], item['PRICE'],
                                                        item['NAME'])
                        self.all_previous_items[self.idx] = self.current_items[:]
                        pass
        
        except IndexError:
            if len(self.current_items) > len(self.all_previous_items[self.idx]):
                # Something was added
                for item in self.current_items:

                    if item not in self.all_previous_items[self.idx]:
                        self.bot.send_alert_footlocker(item['LINK'], item['IMAGE'],
                                item['SKU'], item['PRICE'],
                                item['NAME'])
                        self.all_previous_items[self.idx] = self.current_items[:]
                        pass

            elif len(self.current_items) < len(self.all_previous_items[self.idx]):
                self.set_up_flag = True


if __name__ == "__main__":
    notify = DiscordNotify()
    bot = FootLockerMonitor('hi', notify, 'hi', 3)

    bot.search_wanted_items()