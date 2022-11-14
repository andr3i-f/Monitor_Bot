import discord
import json


class DiscordNotify:
    """Manages the messages that are being sent to the discord"""
    def __init__(self):
        with open("config/webhooks.json") as f:
            webhooks = json.load(f)

        self.SHOPIFY_HOOK_ALERT = webhooks['shopify_webhook']
        self.SUPREME_HOOK_ALERT = webhooks['supreme_webhook']
        self.FOOTLOCKER_HOOK_ALERT = webhooks['footlocker_webhook']
        self.WEB_HOOK_LOGS = webhooks['logs_webhook']

        self.shopify_alert = discord.SyncWebhook.from_url(self.SHOPIFY_HOOK_ALERT)
        self.supreme_alert = discord.SyncWebhook.from_url(self.SUPREME_HOOK_ALERT)
        self.footlocker_alert = discord.SyncWebhook.from_url(self.FOOTLOCKER_HOOK_ALERT)
        self.webhook_logs = discord.SyncWebhook.from_url(self.WEB_HOOK_LOGS)

    def send_alert(self, title, link, state, sizes, img, color=0xf705cb):
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
            embed_var.add_field(name="Sizes", value="\n".join([size for size in sizes]))

        try:
            self.shopify_alert.send(embed=embed_var)
        except discord.errors.HTTPException:
            self.update_log(f"HTTPException raised again for: \n{title}\n{link}\n{state}\n{sizes}")
            pass

    def send_alert_supreme(self, link, img, color=0xff0000):
        embed_var = discord.Embed(title="Supreme New Item", color=color, url=link)
        embed_var.set_image(url=img)
        embed_var.set_author(name="andr3i monitors", url="https://github.com/andr3i-f/")
        
        self.supreme_alert.send(embed=embed_var) 
    
    def send_alert_footlocker(self, link, img, sku, price, name="test", color=0xababab):
        embed_var = discord.Embed(title=name, color=color, url=link)
        embed_var.set_image(url=img)
        embed_var.set_author(name="andr3i monitors", url="https://github.com/andr3i-f/")

        self.footlocker_alert.send(embed=embed_var)

    def broadcast(self, title, desc, color=0x00ffff):
        embed_var = discord.Embed(title=title, description=desc, color=color)
        embed_var.set_author(name="andr3i monitors", url="https://github.com/andr3i-f/")
        self.shopify_alert.send(embed=embed_var)

    def update_log(self, msg="Test"):
        self.webhook_logs.send(msg)
