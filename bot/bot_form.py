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
        await interaction.response.send_message("pong")
    
    @tree.command(name="add_webhook", description="Add webhook", guild=discord.Object(id=guild_id))
    async def add_webhook(interaction):
        await interaction.response.send
    
    @client.event
    async def on_ready():
        await tree.sync(guild=discord.Object(id=guild_id))
        print("ready!")
    

    client.run(secret)


if __name__ == "__main__":
    main()