import random
import requests
import json
import time
import logging
from fp.fp import FreeProxy


class Monitor:
    """Class to initiate and manage the behavior of the monitor"""
    def __init__(self, url, name, collections, keywords, unwanted, bot, delay=3):
        self.name = name
        self.collections = collections

        self.url = url

        self.bot = bot

        self.keywords = keywords
        self.unwanted = unwanted

        self.wanted_items = []
        self.previous_items = []

        self.all_previous_items = []

        self.set_up_flag = True
        self.reset_flag = False

        self.blocked = False
        self.timeout_timer = None

        self.delay = delay

        with open('config/user_agents.json') as f:
            self.user_agents = json.load(f)

    def search_wanted_items(self):
        """Adds all the products that has a key-word in its title"""
        for idx, collection in enumerate(self.collections):
            self.wanted_items = []
            page = 1

            while True:  # Will go through all the pages a shopify website has to offer
                if not self.blocked:
                    headers = {'User-Agent': random.choice(self.user_agents)}
                    req_url = requests.get(f"{self.url}/collections/{collection}/"
                                           f"products.json?limit=250&page={page}", headers=headers)

                    if req_url.status_code == 430:  # Dealing with blocked requests, switch to free proxies (safe as long as we don't send important info I'm pretty sure)
                        self.bot.update_log(f"```{self.name} has blocked our requests, switching to free proxies for the time being```")
                        self.blocked = True
                        self.timeout_timer = time.time()

                if self.blocked:  # If server blocked our requests, switch to free proxies for a period of time (default is 6 minutes to be safe before trying again)
                    while True:
                        headers = {'User-Agent': random.choice(self.user_agents)}
                        proxies = {
                            'https' : FreeProxy(rand=True, country_id=['US']).get()
                        }
                        req_url = requests.get(f"{self.url}/collections/{collection}/products.json?limit=250&page={page}", headers=headers, proxies=proxies)

                        if req_url.status_code == 200:
                            break

                    if time.time() - self.timeout_timer > 360:
                        self.blocked = False
                        self.bot.update_log(f"```Switching away from free proxies```")

                #print(self.name, req_url.status_code)
                all_products = json.loads(req_url.text)['products']


                if not all_products:  # Checks if we reached a page that doesn't have products
                    break

                for product in all_products:
                    w_item = {}
                    if any(substring in product['title'].lower() for substring in self.keywords) \
                            and not any(substring in product['title'].lower() for substring in self.unwanted):
                        try:
                            w_item['NAME'] = product['title']
                            w_item['AVAIL_SIZES'] = [size['title'] for size in product['variants'] if size['available']]
                            w_item['IMG'] = product['images'][0]['src']
                            w_item['LINK'] = f"{self.url}products/{product['handle']}"
                        except IndexError:  # Incase there is an issue with grabbing item details
                            if not product['title']:
                                w_item['NAME'] = "Product Name - [Website Issue]"  # General name incase name can't be grabbed
                            else:
                                w_item['NAME'] = product['title']

                            if not product['IMG']:
                                w_item['IMG'] = "https://via.placeholder.com/705x450.png"  # Placeholder image incase image can't be grabbed
                            else:
                                w_item['IMG'] = product['images'][0]['src']

                            if not product['handle']:
                                w_item['LINK'] = f"{self.url}{collection}/"  # General link incase item link can't be grabbed
                            else:
                                w_item['LINK'] = f"{self.url}products/{product['handle']}"

                            if not [size['title'] for size in product['variants'] if size['available']]:
                                w_item['AVAIL_SIZES'] = "0"  # General answer incase sizes can't be grabbed
                            else:
                                w_item['AVAIL_SIZES'] = [size['title'] for size in product['variants'] if size['available']]

                            #print(f'An item in {self.name} has an issue with "IndexError"')  # Debug

                        self.wanted_items.append(w_item)
                        #print(self.name, len(self.wanted_items))
                page += 1
                time.sleep(self.delay)  # Delay per each page as half a second is the minimum delay for requests for shopify

            if self.set_up_flag:  # Copies items to previous items when initiating program to be able to compare later
                self.previous_items = self.wanted_items[:]
                self.all_previous_items.append(self.previous_items)

            # Call for comparison here
            #print(len(self.wanted_items), len(self.all_previous_items[idx]))  # Debug
            self.reset_flag = self.compare_items(self.wanted_items, self.all_previous_items[idx])

            if self.reset_flag:
                self.all_previous_items[idx] = self.wanted_items[:]
                self.reset_flag = False

        if self.set_up_flag:
            self.set_up_flag = False


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
