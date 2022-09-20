import discord
from dotenv import load_dotenv
import os


class DiscordNotify:
    """Manages the messages that are being sent to the discord"""
    def __init__(self):
        load_dotenv()
        self.WEB_HOOK_ALERT = os.getenv('WEB_HOOK_ALERT')
        self.WEB_HOOK_LOGS = os.getenv('WEB_HOOK_LOGS')

        self.webhook_alert = discord.SyncWebhook.from_url(self.WEB_HOOK_ALERT)
        self.webhook_logs = discord.SyncWebhook.from_url(self.WEB_HOOK_LOGS)

    def send_alert(self, msg="Test"):
        self.webhook_alert.send(msg)

    def update_log(self, msg="Test"):
        self.webhook_logs.send(msg)

