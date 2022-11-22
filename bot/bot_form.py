import discord
from discord import app_commands

secret = "MTAyMTIyMDQ1Mzc1NjQ1Njk3MA.GX9KPz.cGUUchaSR1ldDQaGgUdQzFtACKQ3PtIz5Meefs"
guild_id = 1021219582247178260

def main():
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    @tree.command(name="ping", description="Will pong", guild=discord.Object(id=guild_id))
    async def ping(interaction):
        await interaction.response.send_message("pong", ephemeral=True)

    
    @tree.command(name="shopify_webhook", description="Add your shopify webhook", guild=discord.Object(id=guild_id))
    async def shopify_webhook(interaction):
        await interaction.response.send_modal(webhook_form_shopify())

    @tree.command(name="supreme_webhook", description="Add your shopify webhook", guild=discord.Object(id=guild_id))
    async def shopify_webhook(interaction):
        await interaction.response.send_modal(webhook_form_supreme())

    @tree.command(name="footlocker_webhook", description="Add your shopify webhook", guild=discord.Object(id=guild_id))
    async def shopify_webhook(interaction):
        await interaction.response.send_modal(webhook_form_footlocker())

    @tree.command(name="nike_webhook", description="Add your shopify webhook", guild=discord.Object(id=guild_id))
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