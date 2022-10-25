from query import *

def first_screen(connection, cursor):
    print("Enter 1: Sign In")
    print("Enter 2: Sign Up")
    print("Enter 3: Exit")
    option = input("Choose your option: ")

    if option == '1':
        sign_in()
    elif option == '2':
        sign_up(connection, cursor)
    elif option == '3':
        quit()
    else:
        print("Please choose correct option.")

def sign_in():
    return

def sign_up(connection, cursor):
    while True:
        print("Enter 1 if you are user")
        print("Enter 2 if you are artist")
        type_of_user = input("Choose your option: ")
        if type_of_user == 1:
            break
        elif type_of_user == 2:
            break
        else:
            print("Please choose correct option.")

    
    while True:
        username = (input("Enter your username: "),)
        cursor.execute("""SELECT aid
                          FROM artists
                          WHERE aid = ?;
                       """, username)
        username_check = cursor.fetchone()
        try:
            if username[0] == username_check[0]:
                print("This username has already been taken. Please enter different username")
                continue
        except:
            break
    
    
    nationality = input("Enter your nationality: ")
    name = input("Enter Your Name: ")
    password = input("Enter your password: ")
    
    connection.commit()
    return
def sign_out():
    first_screen()

