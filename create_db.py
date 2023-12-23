import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="neetu324",
)
my_cursor=mydb.cursor()
# I have created a data base so we don't need this anymore so rather than deleting just comment out the below line so that is this file acciednelty gets run it don't create a new database
# my_cursor.execute("CREATE DATABASE our_users")
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)