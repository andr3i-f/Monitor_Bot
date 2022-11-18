import discord
import mysql.connector
import db
secret = "MTAyMTIyMDQ1Mzc1NjQ1Njk3MA.GX9KPz.cGUUchaSR1ldDQaGgUdQzFtACKQ3PtIz5Meefs"
# inv https://discord.com/api/oauth2/authorize?client_id=1021220453756456970&permissions=1634504013888&scope=bot



def main():
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    database = db.database()

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
            key = str(message.clean_content[9:])
            author = str(message.author.id)
            name = str(message.author)

            #print(key)
            #print(author)
            #print(name)

            t = database.add_webhook(author, name, key)
            database.commit()
            #print(t)

            database.show_users()
            await message.channel.send(message.clean_content[8:])

    client.run(secret)

if __name__ == "__main__":
    main()