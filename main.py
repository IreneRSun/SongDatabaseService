from main_menu import *
import sqlite3

connection = sqlite3.connect("./data.db")
cursor = connection.cursor()
connection.commit()

first_screen(connection, cursor)