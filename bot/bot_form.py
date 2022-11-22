import discord
from discord import app_commands
import datetime

secret = "MTAyMTIyMDQ1Mzc1NjQ1Njk3MA.GX9KPz.cGUUchaSR1ldDQaGgUdQzFtACKQ3PtIz5Meefs"
guild_id = 1021219582247178260
membership_role = "1043673145074253875"

def main():
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    @tree.command(name="add_client", description="Adds you to the client database if you have the required role", guild=discord.Object(id=guild_id))
    async def add_client(interaction):
        has_role = interaction.user.get_role(int(membership_role))
        if has_role:
            discord_id = interaction.user.id
            discord_name = interaction.user
            membership = "Y"
            created = datetime.now()
        
        elif not has_role:
            await interaction.response.send_message("You do not have the 'Membership' role", ephemeral = True)
    
    @tree.command(name="shopify_webhook", description="Add your shopify webhook", guild=discord.Object(id=guild_id))
    async def shopify_webhook(interaction):
        await interaction.response.send_modal(webhook_form_shopify())

    @tree.command(name="supreme_webhook", description="Add your supreme webhook", guild=discord.Object(id=guild_id))
    async def shopify_webhook(interaction):
        await interaction.response.send_modal(webhook_form_supreme())

    @tree.command(name="footlocker_webhook", description="Add your footlocker webhook", guild=discord.Object(id=guild_id))
    async def shopify_webhook(interaction):
        await interaction.response.send_modal(webhook_form_footlocker())

    @tree.command(name="nike_webhook", description="Add your nike webhook", guild=discord.Object(id=guild_id))
    async def shopify_webhook(interaction):
        await interaction.response.send_modal(webhook_form_nike())

    @client.event
    async def on_ready():
        await tree.sync(guild=discord.Object(id=guild_id))
        print("ready!")
    

    client.run(secret)

class webhook_form_shopify(discord.ui.Modal, title="Shopify Webhook Input"):   # SHOPIFY WEBHOOK INPUT
    webhook = discord.ui.TextInput(label="WEBHOOK INPUT", style=discord.TextStyle.paragraph)
    

    async def on_submit(self, interaction: discord.Interaction):
        # When person presses submit, this is where I try to add their webhook
        await interaction.response.send_message(f"Submission entered", ephemeral=True)

class webhook_form_supreme(discord.ui.Modal, title="Supreme Webhook Input"):  # SUPREME WEBHOOK INPUT
    webhook = discord.ui.TextInput(label="WEBHOOK INPUT", style=discord.TextStyle.paragraph)
    

    async def on_submit(self, interaction: discord.Interaction):
        # When person presses submit, this is where I try to add their webhook
        await interaction.response.send_message(f"Submission entered", ephemeral=True)

class webhook_form_footlocker(discord.ui.Modal, title="Footlocker Webhook Input"):  # FOOTLOCKER WEBHOOK INPUT
    webhook = discord.ui.TextInput(label="WEBHOOK INPUT", style=discord.TextStyle.paragraph)
    

    async def on_submit(self, interaction: discord.Interaction):
        # When person presses submit, this is where I try to add their webhook
        await interaction.response.send_message(f"Submission entered", ephemeral=True)


class webhook_form_nike(discord.ui.Modal, title="Nike Webhook Input"):  # NIKE WEBHOOK INPUT
    webhook = discord.ui.TextInput(label="WEBHOOK INPUT", style=discord.TextStyle.paragraph)
    

    async def on_submit(self, interaction: discord.Interaction):
        # When person presses submit, this is where I try to add their webhook
        await interaction.response.send_message(f"Submission entered", ephemeral=True)

if __name__ == "__main__":
    main()