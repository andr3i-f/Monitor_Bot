import requests
import json


class Monitor:
    """Class to initiate and manage the behavior of the monitor"""
    def __init__(self, url, name, keywords):
        self.name = name
        self.file = f"../Data/{self.name}_current_data.json"
        self.url = url
        self.json_url = url + "products.json?limit=250"
        self.keywords = keywords
        self.wanted_items = []
        self.set_up_flag = True

    def search_wanted_items(self):
        """Adds all the products that has a key-word in its title"""
        req_url = requests.get(self.json_url)
        all_products = json.loads(req_url.text)['products']
        self.wanted_items = []

        for product in all_products:
            w_item = {}
            if any(substring in product['title'].lower() for substring in self.keywords):
                w_item['NAME'] = product['title']
                w_item['AVAIL_SIZES'] = [size['title'] for size in product['variants'] if size['available']]
                w_item['IMG'] = product['images'][0]['src']
                w_item['LINK'] = f"{self.url}products/{product['handle']}"

                self.wanted_items.append(w_item)
