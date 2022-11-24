import requests
from fp.fp import FreeProxy
import json
import time


D_val = 55

link = f"https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=F5D705D8A7A1693D9B087CB93EC981FF&country=us&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(0f64ecc7-d624-4e91-b171-b83a03dd8550%2C16633190-45e5-4830-a068-232ac7aea82c%2C498ac76f-4c2c-4b55-bbdc-dd37011887b1)%26anchor%3D{D_val}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=en&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D"\


all = requests.get(link)
items = json.loads(all.text)


print(len(items['data']['products']['products']))