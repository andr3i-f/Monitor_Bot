import requests


anchor = 50
headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-GB,en;q=0.9',
        'appid': 'com.nike.commerce.snkrs.web',
        'content-type': 'application/json; charset=UTF-8',
        'dnt': '1',
        'nike-api-caller-id': 'nike:snkrs:web:1.0',
        'origin': 'https://www.nike.com',
        'referer': 'https://www.nike.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
LOCATION = 'US'
LANGUAGE = 'en'

link = "https://api.nike.com/product_feed/threads/v3/?anchor=50&count=50&filter=marketplace%28US%29&filter=language%28en%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&filter=exclusiveAccess%28true%2Cfalse%29"

html = requests.get(link, headers=headers)
print(html.text)