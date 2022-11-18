import mysql.connector


def main():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="testdatabase"
    )

    mycursor = db.cursor()
    


if __name__ == "__main__":
    main()