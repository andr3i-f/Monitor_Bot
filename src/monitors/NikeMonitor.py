import random
import requests
import json
import time

class Monitor:
    def __init__(self, name, webhook_bot, keywords, delay=3):
        self.name = name
        self.webhook_bot = webhook_bot
        self.delay = delay

        self.keywords = keywords
        
        self.set_up_flag = True

        self.current_products = []
        self.previous_products = []

        with open('config/user_agents.json') as f:
            self.user_agents = json.load(f)
        
    def search_wanted_items(self):
        pass
    