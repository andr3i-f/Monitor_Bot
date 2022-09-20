import requests
from bs4 import BeautifulSoup
import json


class OffWhiteMonitor:
    """Class to initiate and manage the behavior of this monitor"""
    def __init__(self, link="https://gallery.canary---yellow.com/", json_file="off_white_cy_data.json"):
        self.link = requests.get(link)
        self.name = "off_white_cy"
        self.file = json_file
        self.soup = BeautifulSoup(self.link.content, 'html.parser')
        self.shoes = []
        self.set_up_flag = True

    def find_shoes(self):
        """Adds all the shoes found as dictionaries into the shoes list"""

        """This will find all the items listed in the catalog and put it in the var items"""
        items = self.soup.find_all("li",
                                   class_="grid__item grid__item--featured-collections small--one-half medium-up--one-fifth")

        self.shoes.clear()  # Clear the list so the list doesn't append to itself on every call

        for item in items:
            shoe_dict = {}
            if "shoes" in item.text.lower():
                shoe_dict['NAME'] = item.find("div", class_="h4 grid-view-item__title product-card__title").text.strip()
                shoe_dict['PRICE'] = item.find("span", class_="price-item price-item--regular").text.strip()
                shoe_dict['IN-STOCK'] = item.find("div", class_="product-form__item product-form__item--submit").text\
                    .strip()
                shoe_dict['LINK'] = f"https://gallery.canary---yellow.com/{item.find('a')['href']}"

                self.shoes.append(shoe_dict)

        if self.set_up_flag:
            self.dump_data()
            self.set_up_flag = False

    def dump_data(self):
        """This will dump data into the JSON file"""

        with open(self.file, 'w') as f:
            json.dump(self.shoes, f, indent=4)

    def get_data(self):
        """This will read and return the data from the JSON file"""

        with open(self.file, 'r') as f:
            data = json.load(f)
        return data


off_w = OffWhiteMonitor()
off_w.find_shoes()
