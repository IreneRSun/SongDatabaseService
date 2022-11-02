from main_menu import *
import sqlite3

database = input("Enter database name you want to use: ")
connection = sqlite3.connect(database)
cursor = connection.cursor()
connection.commit()

first_screen(connection, cursor)
