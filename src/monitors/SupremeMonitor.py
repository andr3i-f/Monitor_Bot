import requests
import json
from fp.fp import FreeProxy
import time
import random
from bs4 import BeautifulSoup
import webhooks


class SupremeMonitor:
    """Class to initiate and manage behavior of Supreme Monitor"""
    def __init__(self, name, bot, delay):
        self.name = name
        
        self.url = "https://www.supremenewyork.com/shop/all"

        self.bot = bot

        self.current_items = []
        self.previous_items = []

        self.set_up_flag = True
        self.reset_flag = False

        self.blocked = False
        self.timeout_timer = None

        self.delay = delay

        with open('config/user_agents.json') as f:
            self.user_agents = json.load(f)

    def search_wanted_items(self):
        """Gets all current products from supremenewyork.com/shop/all"""

        self.current_items = []
        headers = {'User-Agent' : random.choice(self.user_agents)}
        req_url = requests.get(f"{self.url}", headers=headers)
        soup = BeautifulSoup(req_url.text, features='lxml')

        soup = soup.find("ul", class_="turbolink_scroller")
        all_items = soup.find_all("li")

        for item in all_items:
            w_item = {}
            w_item['LINK'] = f"https://supremenewyork.com{item.find('a', href=True)['href']}"
            w_item['IMAGE'] = f"https:{item.find('img')['src']}"
            
            self.current_items.append(w_item)
        
        #self.bot.send_alert_supreme(self.current_items[0]['LINK'], self.current_items[0]['IMAGE'])
  
        if self.set_up_flag:
            self.previous_items = self.current_items[:]
            self.set_up_flag = False
        time.sleep(self.delay)

        print(len(self.current_items), len(self.previous_items))
        
        if self.previous_items != self.current_items:
            self.compare_items()

    def compare_items(self):
        if self.set_up_flag == False:
            try:
                if self.previous_items != self.current_items:

                    if len(self.previous_items) != len(self.current_items):
                        raise IndexError  # Raise error because lens are different
                    
                    for item in self.current_items:
                        if item not in self.previous_items:
                            bot.send_alert_supreme(item['LINK'], item['IMAGE'])
                            self.set_up_flag = True
                            

                elif self.previous_items == self.current_items:
                    pass  # Nothing was changed

            
            except IndexError:
                if len(self.current_items) > len(self.previous_items):
                    # Something was added

                    for item in self.current_items:
                        if item not in self.previous_items:
                            bot.send_alert_supreme(item['LINK'], item['IMAGE'])
                            self.set_up_flag = True
                            
                    
                elif len(self.current_items) < len(self.previous_items):
                    # Something was removed
                    self.set_up_flag = True

        elif self.set_up_flag == True:
            pass

if __name__ == "__main__":
    notify = webhooks.DiscordNotify()
    bot = SupremeMonitor("Supreme", notify, 3)

    bot.search_wanted_items()


