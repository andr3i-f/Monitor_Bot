import discord
from discord.ext import commands
from datetime import datetime
import db
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

            database.add_client(discord_id, discord_name, membership, created)
        
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
            result = database.add_webhook_supreme(ID, key, time)        
        
        if result:
            await ctx.send("Added webhook into database")
        elif not result:
            await ctx.send("Could not add webhook into database")
    
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
            result = database.add_webhook_supreme(ID, key, time)

        if result:
            await ctx.send("Added webhook into database")
        elif not result:
            await ctx.send("Could not add webhook into database")

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
            result = database.add_webhook_supreme(ID, key, time)

        if result:
            await ctx.send("Added webhook into database")
        elif not result:
            await ctx.send("Could not add webhook into database")

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
            result = database.add_webhook_supreme(ID, key, time) 

        if result:
            await ctx.send("Added webhook into database")
        elif not result:
            await ctx.send("Could not add webhook into database")             

    client.run(secret)

if __name__ == "__main__":
    main()