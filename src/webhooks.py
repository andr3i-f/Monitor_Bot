import discord
import json


class DiscordNotify:
    """Manages the messages that are being sent to the discord"""
    def __init__(self):
        with open("config/webhooks.json") as f:
            x = json.load(f)

        self.shopify_webhooks = import_webhooks('shopify')
        self.footlocker_webhooks = import_webhooks('footlocker')
        self.supreme_webhooks = import_webhooks('supreme')
        self.nike_webhooks = import_webhooks('nike')
        self.snkrs_webhooks = import_webhooks('snkrs')

        self.webhook_logs = discord.SyncWebhook.from_url("https://discord.com/api/webhooks/1021259923516043314/d67D6x8V-kbGtX4xyVkf0-TlCNDJZbZkZYw3jBkdRJvWUV3BagM6mLabs839H6P-94sR")

    def send_alert_shopify(self, title, link, state, sizes, img, color=0xf705cb):
        embed_var = discord.Embed(title=title, color=color, url=link)
        embed_var.set_image(url=img)
        embed_var.set_author(name="andr3i monitors", url="https://github.com/andr3i-f/")

        embed_var.add_field(name="Event", value=state, inline=False)

        # Below is just for formatting the discord embed alert based on amount of sizes given
        if len(sizes) > 4:
            if len(sizes) % 2 == 0:  # If it's even, split up the sizes evenly
                embed_var.add_field(name="Available Sizes", value="\n".join([size for size in sizes[0:int(len(sizes) / 2)]]),
                                    inline=True)
                embed_var.add_field(name="\u200b", value="\n".join([size for size in sizes[int(len(sizes) / 2):]]),
                                    inline=True)
            elif len(sizes) % 2 != 0:  # If it's odd, make sure the left side has the one extra size
                embed_var.add_field(name="Sizes", value="\n".join([size for size in sizes[0:int(len(sizes) / 2) + 1]]),
                                    inline=True)
                embed_var.add_field(name="\u200b", value="\n".join([size for size in sizes[int(len(sizes) / 2) + 1:]]),
                                    inline=True)
        elif len(sizes) <= 4:
            embed_var.add_field(name="Available Sizes", value="\n".join([size for size in sizes]))

        try:
            send_alerts(self.shopify_webhooks, embed_var)
        except discord.errors.HTTPException:
            self.update_log(f"HTTPException raised again for: \n{title}\n{link}\n{state}\n{sizes}")
            pass

    def send_alert_supreme(self, link, img, color=0xff0000):
        embed_var = discord.Embed(title="Supreme New Item", color=color, url=link)
        embed_var.set_image(url=img)
        embed_var.set_author(name="andr3i monitors", url="https://github.com/andr3i-f/")
        
        send_alerts(self.supreme_webhooks, embed_var)
    
    def send_alert_footlocker(self, link, img, sku, price, name="test", color=0xababab):
        embed_var = discord.Embed(title=name, color=color, url=link)
        embed_var.set_image(url=img)
        embed_var.set_author(name="andr3i monitors", url="https://github.com/andr3i-f/")

        send_alerts(self.footlocker_webhooks, embed_var)
    
    def send_alert_SNKRS(self, title, prod_color, price, launch_date, sku, image, prod_link, color=0xff0008):
        embed_var = discord.Embed(title=title, color=color, url=prod_link)
        embed_var.set_image(url=image)
        embed_var.set_author(name="andr3i monitors", url="https://github.com/andr3i-f/")
        
        embed_var.add_field(name="Product Color", value=prod_color, inline=True)
        embed_var.add_field(name="Price", value=price, inline=True)
        embed_var.add_field(name="Launch Date", value=launch_date, inline=True)
        embed_var.add_field(name="SKU", value=sku, inline=True)

        send_alerts(self.snkrs_webhooks, embed_var)

    def broadcast(self, title, desc, color=0x00ffff):
        embed_var = discord.Embed(title=title, description=desc, color=color)
        embed_var.set_author(name="andr3i monitors", url="https://github.com/andr3i-f/")
        self.shopify_alert.send(embed=embed_var)

    def update_log(self, msg="Test"):
        self.webhook_logs.send(msg)


def import_webhooks(monitor_name):
    current_webhooks = []

    with open("config/webhooks.json") as f:
        all = json.load(f)
    
    for dict in all[monitor_name]:
        for x in dict.values():
            current_webhooks.append(x)
    
    return current_webhooks

def send_alerts(webhook_list, embed_var):
    for webhook in webhook_list:
        alert = discord.SyncWebhook.from_url(webhook)
        alert.send(embed=embed_var)
