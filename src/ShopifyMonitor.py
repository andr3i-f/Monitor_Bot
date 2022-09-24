import random
import requests
import json
import time


class Monitor:
    """Class to initiate and manage the behavior of the monitor"""
    def __init__(self, url, name, collections, keywords, unwanted, comparer):
        self.name = name
        self.collections = collections

        self.comparer = comparer

        self.url = url

        self.keywords = keywords
        self.unwanted = unwanted

        self.wanted_items = []
        self.previous_items = []

        self.all_previous_items = []

        self.set_up_flag = True
        self.reset_flag = False

        self.stop_monitor = False

        with open('config/user_agents.json') as f:
            self.user_agents = json.load(f)

    def search_wanted_items(self):
        """Adds all the products that has a key-word in its title"""
        for idx, collection in enumerate(self.collections):
            self.wanted_items = []
            page = 1

            while True:  # Will go through all the pages a shopify website has to offer
                headers = {'User-Agent': random.choice(self.user_agents)}
                req_url = requests.get(f"{self.url}/collections/{collection}/"
                                       f"products.json?limit=250&page={page}", headers=headers)

                all_products = json.loads(req_url.text)['products']

                if req_url.status_code == 430:
                    self.stop_monitor = True

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
                        except IndexError:
                            print(f'An item in {self.name} has an issue with "IndexError"')

                        self.wanted_items.append(w_item)
                page += 1
                time.sleep(1)  # Delay per each page as half a second is the minimum delay for requests for shopify

            if self.set_up_flag:  # Copies items to previous items when initiating program to be able to compare later
                self.previous_items = self.wanted_items[:]
                self.all_previous_items.append(self.previous_items)

            # Call for comparison here
            print(len(self.wanted_items), len(self.all_previous_items[idx]))
            self.reset_flag = self.comparer.compare_items(self.wanted_items, self.all_previous_items[idx])

            if self.reset_flag:
                self.all_previous_items[idx] = self.wanted_items[:]
                self.reset_flag = False

        if self.set_up_flag:
            self.set_up_flag = False
