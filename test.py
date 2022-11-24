import requests
import json
import time


headers = {
        'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
LOCATION = 'US'
LANGUAGE = 'en'

anchor = 0

while anchor < 160:
    link = f"https://api.nike.com/product_feed/threads/v3/?anchor={anchor}&count=50&filter=marketplace%28US%29&filter=language%28en%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89d61%29&filter=exclusiveAccess%28true%2Cfalse%29"
    html = requests.get(link, headers=headers)

    html = json.loads(html.text)['objects']

    for x in html:
        try:
            product = {}
            title = x['productInfo'][0]['productContent']['fullTitle']
            color = x['productInfo'][0]['productContent']['colorDescription']
            price = f"${x['productInfo'][0]['merchPrice']['fullPrice']}"
            launch_date = x['productInfo'][0]['launchView']['startEntryDate'][:10]
            sku = x['productInfo'][0]['availableGtins'][0]['styleColor']
            image = x['publishedContent']['properties']['coverCard']['properties']['squarishURL']
            link = f"https://www.nike.com/launch/t/{x['publishedContent']['properties']['seo']['slug']}"
            
            product['title'] = title
            product['color'] = color
            product['price'] = price
            product['launch_date'] = launch_date
            product['sku'] = sku
            product['image'] = image
            product['link'] = link
            

            print(product['link'])


            #print(title, sku)
        except KeyError:
            pass
    
    anchor += 50
    time.sleep(3)