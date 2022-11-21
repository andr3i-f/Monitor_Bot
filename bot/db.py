import mysql.connector
from datetime import datetime


"""def main():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="testdatabase"
    )

    mycursor = db.cursor()
"""
    #query1 = "CREATE TABLE Clients (id int PRIMARY KEY AUTO_INCREMENT, user_id VARCHAR(50), name VARCHAR(50), webhook VARCHAR(150))"
    

tables = ['shopify', 'footlocker', 'supreme', 'nike']

class database:
    def __init__(self, host="localhost", user="root", passwd="root", database="A1Monitors"):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
    
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )

        self.mycursor = self.db.cursor()
    
    def commit(self):
        self.db.commit()

    def add_client(self, discord_id, discord_name, membership, created):
        # This will add in a client if they have the membership role
        query = "INSERT INTO Clients (DiscordID, DiscordName, Membership, Created) VALUES (%s, %s, %s, %s)"
        val = (discord_id, discord_name, membership, created)
        self.mycursor.execute(query, val)

        self.commit()
        
        pass
    
    def add_webhook_shopify(self, ID, webhook, created):
        # This will check, and if there is no user for the webhook then it will add it, if there is a user with this webhook it will change it
        query = "INSERT INTO Shopify (ID, webhook, Created) VALUES (%s, %s, %s)"
        val = (ID, webhook, created)
        self.mycursor.execute(query, val)

        self.commit()

        return True
    
    def add_webhook_supreme(self, ID, webhook, created):
        query = "INSERT INTO Supreme (ID, webhook, Created) VALUES (%s, %s, %s)"
        val = (ID, webhook, created)
        self.mycursor.execute(query, val)

        self.commit()
        
        return True      

    def add_webhook_footlocker(self, ID, webhook, created):
        query = "INSERT INTO Footlocker (ID, webhook, Created) VALUES (%s, %s, %s)"
        val = (ID, webhook, created)
        self.mycursor.execute(query, val)

        self.commit()

        return True 

    def add_webhook_nike(self, ID, webhook, created):
        query = "INSERT INTO Nike (ID, webhook, Created) VALUES (%s, %s, %s)"
        val = (ID, webhook, created)
        self.mycursor.execute(query, val)

        self.commit()

        return True 

    def update_webhook(self, ID, key, table_name):
        query =  f"UPDATE {table_name} SET webhook = '{key}' WHERE ID={ID}"
        self.mycursor.execute(query)

        self.commit()

        query = f"UPDATE {table_name} SET Created = '{datetime.now()}' WHERE ID={ID}"
        self.mycursor.execute(query)

        self.commit()

        return True
    
    def remove_webhook(self):
        # This will remove a webhook if the user does not want the webhook anymore
        pass

    def remove_user(self, id):
        # This will remove a user if the user does not have membership anymore
        query = f"DELETE FROM Clients WHERE ID = {id}"
        self.mycursor.execute(query)
        self.commit()

    def get_membership_role(self, discordID):
        # This will return true or false depending if the user has a current membership in client database
        query = f"SELECT Membership FROM Clients WHERE DiscordID={discordID}"
        self.mycursor.execute(query)

        try:
            member = self.mycursor.fetchone()[0]
        except TypeError:
            member = None

        if member == None:
            print('Member not found')
            return None
        elif member:
            return member
    
    def get_id_webhooks(self, discordID, table_name):
        # This will return a dictionary of the requested ID and webhook if there
        id = self.get_ID(discordID)

        if not id:
            return False
        elif id:
            query = f"SELECT webhook FROM {table_name} WHERE ID={id}"
            self.mycursor.execute(query)

            try:
                webhook = self.mycursor.fetchone()[0]
                return {str(id): webhook}
            except TypeError:
                return False




    def get_ID(self, discordID):
        # This will get the actual ID (not discord) from the user if they have membership
        query = f"SELECT ID FROM Clients WHERE DiscordID={discordID}"
        self.mycursor.execute(query)

        try:
            id = self.mycursor.fetchone()[0]
        except TypeError:
            id = False

        if not id:
            return False
        elif id:
            return id

    def add_user(self):
        # This is for testing purposes
        query = "INSERT INTO Clients (DiscordID, DiscordName, Membership, Created) VALUES (%s, %s, %s, %s)"
        val = ("12356", "Andrei", "Y", datetime.now())

        self.mycursor.execute(query, val)
        self.commit()

    def show_users(self):
        # This will show the current users
        query = "SELECT * FROM Clients"
        self.mycursor.execute(query)

        for x in self.mycursor:
            print(x)
    
    def show_table_contents(self, table):
        # This will show contents of a table
        query = f"SELECT * FROM {table}"
        self.mycursor.execute(query)

        for x in self.mycursor:
            print(x)
    
    def show_tables(self):
        # This will show current tables
        self.mycursor.execute("Show tables;")
        myresult = self.mycursor.fetchall()

        for x in myresult:
            print(x)

    def describe_table(self, table):
        # This will describe the table given
        self.mycursor.execute(f"DESCRIBE {table}")

        for x in self.mycursor:
            print(x)
    
    def create_tables(self):
        # Creates tables, only used once
        #self.mycursor.execute("CREATE TABLE Clients (DiscordID VARCHAR(100) NOT NULL, DiscordName VARCHAR(100) NOT NULL, Membership ENUM('Y', 'N') NOT NULL, Created datetime, ID int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
        #self.mycursor.execute("CREATE TABLE Supreme (ID int PRIMARY KEY, FOREIGN KEY(ID) REFERENCES Clients(ID), webhook VARCHAR(250), Created datetime)")
        pass
    
def main():
    db = database()
    #db.add_user()
    db.show_users()
    #db.remove_user(4)
    #db.show_users
    #print(db.get_ID('12356'))
    #db.describe_table('shopify')
    #db.show_table_contents('footlocker')
    #db.get_membership_role('121820049940938754')

if __name__ == "__main__":
    main()