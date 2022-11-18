import discord
secret = "MTAyMTIyMDQ1Mzc1NjQ1Njk3MA.GX9KPz.cGUUchaSR1ldDQaGgUdQzFtACKQ3PtIz5Meefs"
# inv https://discord.com/api/oauth2/authorize?client_id=1021220453756456970&permissions=1634504013888&scope=bot

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('!add_key '):
        key = (message.clean_content[8:])
        author = (message.author)
        await message.channel.send(message.clean_content[8:])

        


        with open("bot/test.txt", "a") as f:
            f.write(f"{author} : {key} \n")
            print("Writing key")


client.run(secret)