import json

with open("config/webhooks.json") as f:
    all_webhooks = json.load(f)

shopify_webhooks = []

for dict in all_webhooks['shopify']:
    for x in dict.values():
        shopify_webhooks.append(x)

print(shopify_webhooks)