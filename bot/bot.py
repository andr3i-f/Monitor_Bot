import discord
import bot_form
from discord.ext import commands
from discord import app_commands
import interactions

from datetime import datetime
import db
import json
import sys
import mysql.connector

secret = "MTAyMTIyMDQ1Mzc1NjQ1Njk3MA.GX9KPz.cGUUchaSR1ldDQaGgUdQzFtACKQ3PtIz5Meefs"
# inv https://discord.com/api/oauth2/authorize?client_id=1021220453756456970&permissions=1634504013888&scope=bot


membership_role = "1043673145074253875"


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix='$', intents=intents)

    database = db.database()
    
    @client.command()
    async def test(ctx, arg):
        print(ctx.author.id)
        print(ctx.author.roles)
        #add_webhook_to_json(database, ctx.author.id, 'shopify')
        await ctx.send(arg)
    
    @client.command()
    async def check_role(ctx):
        has_role = ctx.author.get_role(int(membership_role))
        if has_role:
            await ctx.send("You have the membership role")
        elif not has_role:
            await ctx.send("You do not have the membership role")

    @client.command()
    async def add_client(ctx):
        has_role = ctx.author.get_role(int(membership_role))

        if has_role:
            discord_id = str(ctx.author.id)
            discord_name = str(ctx.author)
            membership = "Y"
            created = datetime.now()

            try:
                database.add_client(discord_id, discord_name, membership, created)
            except mysql.connector.IntegrityError:
                await ctx.send("You are already added into Client database")
        
        elif not has_role:
            await ctx.send("Cannot add, try $check_role")

    @client.command()
    async def add_shopify(ctx, arg):
        key = str(arg)
        discord_id = str(ctx.author.id)
        time = datetime.now()
        result = None

        ID = database.get_ID(discord_id)
        member = database.get_membership_role(discord_id)
        if ID == False:
            await ctx.send("Could not find in database, try $add_client")

        elif ID and member == 'Y':
            try:
                result = database.add_webhook_shopify(ID, key, time)
            except mysql.connector.IntegrityError:
                result = database.update_webhook(ID, key, 'shopify')
        
        if result:
            add_webhook_to_json(database, discord_id, 'shopify')
            await ctx.send("Added webhook into database")
        elif not result:
            await ctx.send("Could not add webhook into database")

    @client.command()    
    async def add_supreme(ctx, arg):
        key = str(arg)
        discord_id = str(ctx.author.id)
        time = datetime.now()
        result = None

        ID = database.get_ID(discord_id)
        member = database.get_membership_role(discord_id)
        if ID == False:
            await ctx.send("Could not find in database, try $add_client")
        
        elif ID and member == 'Y':
            try:
                result = database.add_webhook_supreme(ID, key, time)
            except mysql.connector.IntegrityError:
                result = database.update_webhook(ID, key, 'supreme')

        if result:
            add_webhook_to_json(database, discord_id, 'supreme')
            await ctx.send("Added webhook into database")
        elif not result:
            await ctx.send("Could not add webhook into database")

    @client.command()
    async def add_footlocker(ctx, arg):
        key = str(arg)
        discord_id = str(ctx.author.id)
        time = datetime.now()
        result = None

        ID = database.get_ID(discord_id)
        member = database.get_membership_role(discord_id)
        if ID == False:
            await ctx.send("Could not find in database, try $add_client")
        
        elif ID and member == 'Y':
            try: 
                result = database.add_webhook_footlocker(ID, key, time)
            except mysql.connector.IntegrityError:
                result = database.update_webhook(ID, key, 'footlocker')
            

        if result:
            add_webhook_to_json(database, discord_id, 'footlocker')
            await ctx.send("Added webhook into database")
        elif not result:
            await ctx.send("Could not add webhook into database")

    @client.command()
    async def add_nike(ctx, arg):
        key = str(arg)
        discord_id = str(ctx.author.id)
        time = datetime.now()
        result = None

        ID = database.get_ID(discord_id)
        member = database.get_membership_role(discord_id)
        if ID == False:
            await ctx.send("Could not find in database, try $add_client")

        elif ID and member == 'Y':
            try:
                result = database.add_webhook_nike(ID, key, time) 
            except mysql.connector.IntegrityError:
                result = database.update_webhook(ID, key, 'nike')
                


        if result:
            add_webhook_to_json(database, discord_id, 'nike')
            await ctx.send("Added webhook into database")
        elif not result:
            await ctx.send("Could not add webhook into database")

    client.run(secret)

def add_webhook_to_json(database, discordID, table_name):
    id_wh = database.get_id_webhooks(discordID, table_name)
    present_flag = False
    
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
        
            

if __name__ == "__main__":
    main()