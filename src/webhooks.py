import discord
import os
import json


class DiscordNotify:
    """Manages the messages that are being sent to the discord"""
    def __init__(self):
        with open("config/webhooks.json") as f:
            webhooks = json.load(f)

        self.WEB_HOOK_ALERT = webhooks['alert_webhook']
        self.WEB_HOOK_LOGS = webhooks['logs_webhook']

        self.webhook_alert = discord.SyncWebhook.from_url(self.WEB_HOOK_ALERT)
        self.webhook_logs = discord.SyncWebhook.from_url(self.WEB_HOOK_LOGS)

    def send_alert(self, title, link, desc, img, color=0xf705cb):
        desc = desc
        embed_var = discord.Embed(title=title, description=desc, color=color, url=link)
        embed_var.set_image(url=img)
        embed_var.set_author(name="andr3i monitors", url="https://github.com/andr3i-f/")
        self.webhook_alert.send(embed=embed_var)

    def broadcast(self, title, desc, color=0x00ffff):
        embed_var = discord.Embed(title=title, description=desc, color=color)
        embed_var.set_author(name="andr3i monitors", url="https://github.com/andr3i-f/")
        self.webhook_alert.send(embed=embed_var)

    def update_log(self, msg="Test"):
        self.webhook_logs.send(msg)
