import requests
import json
import time
import random
from fp.fp import FreeProxy

import webhooks

class SNKRSMonitor:
    def __init__(self, name, webhook_bot, keywords, delay=3):
        self.name = name
        self.webhook_bot = webhook_bot
        self.delay = delay

        self.keywords = keywords
        self.anchor = 0
        self.link = f"https://api.nike.com/product_feed/threads/v3/?anchor={self.anchor}&count=50&filter=marketplace%28US%29&filter=language%28en%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&filter=exclusiveAccess%28true%2Cfalse%29"
        
        self.set_up_flag = True
        self.blocked_flag = False
        self.timeout_timer = 0

        self.current_products = []
        self.previous_products = []

        with open('config/user_agents.json') as f:
            self.user_agents = json.load(f)
            
    def search_wanted_items(self):
        self.anchor = 0
        self.current_products = []

        while self.anchor < 160:

            if not self.blocked_flag:
                self.link = f"https://api.nike.com/product_feed/threads/v3/?anchor={self.anchor}&count=50&filter=marketplace%28US%29&filter=language%28en%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&filter=exclusiveAccess%28true%2Cfalse%29"
                headers = {'User-Agent': random.choice(self.user_agents)}
                req_url = requests.get(self.link, headers=headers)

                if req_url.status_code != 200:
                    self.blocked_flag = True
                    self.timeout_timer = time.time()
            
            if self.blocked_flag:
                while True:
                    headers = {'User-Agent': random.choice(self.user_agents)}
                    proxies = {'https': FreeProxy(rand=True, country_id=['US']).get()}
                    self.link = f"https://api.nike.com/product_feed/threads/v3/?anchor={self.anchor}&count=50&filter=marketplace%28US%29&filter=language%28en%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&filter=exclusiveAccess%28true%2Cfalse%29"
                    req_url = requests.get(self.link, headers=headers, proxies=proxies)

                    if req_url.status_code == 200:
                        break
                
                if time.time() - self.timeout_timer > 360:
                    self.blocked_flag = False

            all_info = json.loads(req_url.text)['objects']

            for x in all_info:
                try:
                    product = {}
                    title = x['productInfo'][0]['productContent']['fullTitle']
                    color = x['productInfo'][0]['productContent']['colorDescription']
                    price = f"${x['productInfo'][0]['merchPrice']['fullPrice']}"
                    launch_date = x['productInfo'][0]['launchView']['startEntryDate'][:10]
                    sku = x['productInfo'][0]['availableGtins'][0]['styleColor']
                    image = x['publishedContent']['properties']['coverCard']['properties']['squarishURL']
                    prod_link = f"https://www.nike.com/launch/t/{x['publishedContent']['properties']['seo']['slug']}"
                    
                    product['title'] = title
                    product['color'] = color
                    product['price'] = price
                    product['launch_date'] = launch_date[5:]
                    product['sku'] = sku
                    product['image'] = image
                    product['link'] = prod_link

                    self.current_products.append(product)

                    if self.set_up_flag:
                        self.previous_products.append(product)

                except KeyError:  # Found something that's not a product
                    pass
                    
               

            self.anchor += 50
            time.sleep(self.delay)
        
        if self.set_up_flag:
            self.set_up_flag = False

        if self.previous_products != self.current_products:
            self.compare_items()
            
    def compare_items(self):
        try:
            if len(self.current_products) != len(self.previous_products):
                raise IndexError
            
            elif len(self.current_products) == len(self.previous_products):
                for item in self.current_products:

                    if item not in self.previous_products:
                        self.webhook_bot.send_alert_SNKRS(
                            item['title'],
                            item['color'],
                            item['price'],
                            item['launch_date'],
                            item['sku'],
                            item['image'],
                            item['link']
                        )
                        
        
        except IndexError:
            if len(self.current_products) > len(self.previous_products):
                # Something was added

                for item in self.current_products:
                    if item not in self.previous_products:
                        # Send alert here
                        self.webhook_bot.send_alert_SNKRS(
                            item['title'],
                            item['color'],
                            item['price'],
                            item['launch_date'],
                            item['sku'],
                            item['image'],
                            item['link']
                        )

            elif len(self.current_products) < len(self.previous_products):
                # Something was removed
                self.set_up_flag = True


def main():
    notify = webhooks.DiscordNotify()
    bot = SNKRSMonitor('hi', notify, 'hi', 3)
    bot.search_wanted_items()

if __name__ == "__main__":
    main()