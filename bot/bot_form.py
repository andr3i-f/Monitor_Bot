import discord
from discord import app_commands, member
from discord.ext import tasks, commands
from datetime import datetime
import db
import mysql.connector
import json
import time

secret = "MTAyMTIyMDQ1Mzc1NjQ1Njk3MA.GX9KPz.cGUUchaSR1ldDQaGgUdQzFtACKQ3PtIz5Meefs"
guild_id = 1021219582247178260
membership_role = "1043673145074253875"

def main():
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)
    database = db.database()
    
    @tasks.loop(seconds=5)
    async def myloop():
        database_loop = db.database()
        guild = await client.fetch_guild(guild_id)
        discord_id_list = database_loop.get_all_discord_ids()

        for member in discord_id_list:
            for id in member:
                try:
                    user = await guild.fetch_member(id)
                    if user.get_role(int(membership_role)):
                        print("has role")
                        pass

                    elif not user.get_role(int(membership_role)):
                        print("no has role")  # Remove user from client database, and remove all their webhooks, and update webhook file
                        db_id = database.get_ID(id)
                        database.remove_user_webhooks(db_id)
                        database.remove_user_clients(id)
                        
                except AttributeError:  # User is not in discord anymore
                        print("not in discord")
                        db_id = database.get_ID(id)
                        database.remove_user_webhooks(db_id)
                        database.remove_user_clients(id)
                
        # Update json file
        update_webhook_to_json(database_loop)
        del database_loop

    @tree.command(name="add_client", description="Adds you to the client database if you have the required role", guild=discord.Object(id=guild_id))
    async def add_client(interaction):
        has_role = interaction.user.get_role(int(membership_role))
        if has_role:
            discord_id = interaction.user.id
            discord_name = interaction.user
            membership = "Y"
            created = datetime.now()

            id = database.get_ID(discord_id)
            if not id:
                database.add_client(discord_id, str(discord_name), membership, created)
                await interaction.response.send_message("You have been successfully added into the client database", ephemeral = True)
            elif id:
                await interaction.response.send_message("You are already in the client database", ephemeral = True)
        
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
        myloop.start()
        await tree.sync(guild=discord.Object(id=guild_id))
        print("ready!")
    

    client.run(secret)

class webhook_form_shopify(discord.ui.Modal, title="Shopify Webhook Input"):   # SHOPIFY WEBHOOK INPUT
    webhook = discord.ui.TextInput(label="WEBHOOK INPUT", style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        # When person presses submit, this is where I try to add their webhook
        database = db.database()

        webhook_value = str(self.children[0])
        discord_id = interaction.user.id
        created = datetime.now()
        result = None

        ID = database.get_ID(discord_id)
        member = database.get_membership_role(discord_id)

        if ID == False:
            await interaction.response.send_message("Could not find user in database, try /add_client", ephemeral=True)
        
        elif ID and member == 'Y':
            try:
                result = database.add_webhook_shopify(ID, webhook_value, created)
            except mysql.connector.IntegrityError:
                result = database.update_webhook(ID, webhook_value, 'shopify')
        
        if result:
            add_webhook_to_json(database, discord_id, 'shopify')
            await interaction.response.send_message("Added webhook into database", ephemeral=True)
        elif not result:
            await interaction.response.send_message("Could not add webhook into database", ephemeral=True)

class webhook_form_supreme(discord.ui.Modal, title="Supreme Webhook Input"):  # SUPREME WEBHOOK INPUT
    webhook = discord.ui.TextInput(label="WEBHOOK INPUT", style=discord.TextStyle.paragraph)
    

    async def on_submit(self, interaction: discord.Interaction):
        # When person presses submit, this is where I try to add their webhook
        database = db.database()

        webhook_value = str(self.children[0])
        discord_id = interaction.user.id
        created = datetime.now()
        result = None

        ID = database.get_ID(discord_id)
        member = database.get_membership_role(discord_id)

        if ID == False:
            await interaction.response.send_message("Could not find user in database, try /add_client", ephemeral=True)
        
        elif ID and member == 'Y':
            try:
                result = database.add_webhook_supreme(ID, webhook_value, created)
            except mysql.connector.IntegrityError:
                result = database.update_webhook(ID, webhook_value, 'supreme')
        
        if result:
            add_webhook_to_json(database, discord_id, 'supreme')
            await interaction.response.send_message("Added webhook into database", ephemeral=True)
        elif not result:
            await interaction.response.send_message("Could not add webhook into database", ephemeral=True)

class webhook_form_footlocker(discord.ui.Modal, title="Footlocker Webhook Input"):  # FOOTLOCKER WEBHOOK INPUT
    webhook = discord.ui.TextInput(label="WEBHOOK INPUT", style=discord.TextStyle.paragraph)
    

    async def on_submit(self, interaction: discord.Interaction):
        # When person presses submit, this is where I try to add their webhook
        database = db.database()

        webhook_value = str(self.children[0])
        discord_id = interaction.user.id
        created = datetime.now()
        result = None

        ID = database.get_ID(discord_id)
        member = database.get_membership_role(discord_id)

        if ID == False:
            await interaction.response.send_message("Could not find user in database, try /add_client", ephemeral=True)
        
        elif ID and member == 'Y':
            try:
                result = database.add_webhook_footlocker(ID, webhook_value, created)
            except mysql.connector.IntegrityError:
                result = database.update_webhook(ID, webhook_value, 'footlocker')
        
        if result:
            add_webhook_to_json(database, discord_id, 'footlocker')
            await interaction.response.send_message("Added webhook into database", ephemeral=True)
        elif not result:
            await interaction.response.send_message("Could not add webhook into database", ephemeral=True)

class webhook_form_nike(discord.ui.Modal, title="Nike Webhook Input"):  # NIKE WEBHOOK INPUT
    webhook = discord.ui.TextInput(label="WEBHOOK INPUT", style=discord.TextStyle.paragraph)
    

    async def on_submit(self, interaction: discord.Interaction):
        # When person presses submit, this is where I try to add their webhook
        database = db.database()

        webhook_value = str(self.children[0])
        discord_id = interaction.user.id
        created = datetime.now()
        result = None

        ID = database.get_ID(discord_id)
        member = database.get_membership_role(discord_id)

        if ID == False:
            await interaction.response.send_message("Could not find user in database, try /add_client", ephemeral=True)
        
        elif ID and member == 'Y':
            try:
                result = database.add_webhook_nike(ID, webhook_value, created)
            except mysql.connector.IntegrityError:
                result = database.update_webhook(ID, webhook_value, 'nike')
        
        if result:
            add_webhook_to_json(database, discord_id, 'nike')
            await interaction.response.send_message("Added webhook into database", ephemeral=True)
        elif not result:
            await interaction.response.send_message("Could not add webhook into database", ephemeral=True)

def add_webhook_to_json(database, discordID, table_name):
    id_wh = database.get_id_webhooks(discordID, table_name)
    present_flag = False
    print(id_wh)
    with open("config/webhooks.json", "r") as f:
        x = json.load(f)

        for key, val in x.items():
            if key == table_name:
                if not val:  # List of webhooks is empty
                    print('Empty list')
                    val.append(id_wh)
                elif val:  # List of webhooks is not empty
                    for wh in val:
                        print(id_wh.keys(), wh.keys())
                        if id_wh.keys() == wh.keys():
                            print('Changing webhook')
                            val.remove(wh)
                            val.append(id_wh)
                            present_flag = True

                    if not present_flag:
                        print('Appending webhook')
                        val.append(id_wh)  # If list is not empty, but webhook isn't present

    with open("config/webhooks.json", "w") as f:
        json.dump(x, f, indent=4)
        
def update_webhook_to_json(database):
    print("first step updating")
    ids_webhooks = database.get_all_ids_webhooks()
    print(ids_webhooks)
    json_tables = ['shopify', 'footlocker', 'supreme', 'nike']

    with open('config/webhooks.json', 'r') as f:
        x = json.load(f)

    for count, table in enumerate(ids_webhooks):

        x[json_tables[count]] = []

        for webhook_details in table:
            id_wh = {}
            id = webhook_details[0]
            webhook = webhook_details[1]
            id_wh[id] = webhook

            x[json_tables[count]].append(id_wh)
    
    print(x)

    with open('config/webhooks.json', 'w') as f:
        json.dump(x, f, indent=4)






if __name__ == "__main__":
    main()