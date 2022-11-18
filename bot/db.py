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
    
class database:
    def __init__(self, host="localhost", user="root", passwd="root", database="testdatabase"):
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
    
    def add_webhook(self, input_user_id, input_name, input_webhook):
        # This will check, and if there is no user for the webhook then it will add it, if there is a user with this webhook it will change it
        query = "INSERT INTO Clients (user_id, name, webhook) VALUES (%s, %s, %s)"
        val = (input_user_id, input_name, input_webhook)
        self.mycursor.execute(query, val)
        return True
    
    def remove_webhook(self, ):
        # This will remove a webhook if the user does not want the webhook anymore
        pass

    def remove_user(self,):
        # This will remove a user if the user does not have membership anymore
        pass

    def show_users(self):
        # This will show the current users
        query = "SELECT * FROM Clients"
        self.mycursor.execute(query)

        for x in self.mycursor:
            print(x)