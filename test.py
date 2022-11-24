import requests
from fp.fp import FreeProxy
import json
import time


HEADERS = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
        'authority':'www.footlocker.com',
        'method':'GET'
    }

proxies = {
    'https' : FreeProxy(rand=True, country_id=['US']).get()
}

link = f"https://www.footlocker.com/api/products/search?query=jordan%20retro%3Arelevance%3Agender%3ABoys%27%3Aage%3AGrade%20School%3Aproducttype%3AShoes&currentPage=&pageSize=48&timestamp=0"

x = requests.get(link, headers=HEADERS)
print('hi')
print(x.status_code)
