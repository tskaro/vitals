import sqlite3


connection = sqlite3.connect("Health_Data.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, "
               "password TEXT)")

connection.commit()

connection.close()