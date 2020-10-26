import mysql.connector

mydb=mysql.connector.connect(
    host="localhost"
    user="admin"
    password="KEThing1"
    )

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE mydatabase")