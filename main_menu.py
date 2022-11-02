from song_search import song_search
from artist_search import artist_search
from artist_stats import *
from add_song import add_song
from getpass import getpass
from session import *
from utils import *

def first_screen(connection, cursor):
    """
        Sign In/Sign Up user
    """
    
    clear_screen()
    print("Enter 1: Sign In")
    print("Enter 2: Sign Up")
    print("Enter 3: Exit")

    while True:
        option = input("Choose your option: ")
        if option == '1':
            sign_in(connection, cursor)
        elif option == '2':
            sign_up(connection, cursor)
        elif option == '3':
            stop_program(connection, cursor)
        else:
            print("Please choose correct option.")

def sign_in(connection, cursor):
    """
        User sign in
    """
    
    clear_screen()
    print("-----------------Sign in-----------------")
    while True:
        username = input("Enter your username: ").lower()
        password = getpass("Enter your password: ")
        # Check user sign in credentials
        cursor.execute("""SELECT aid as username, pwd
                          FROM artists
                          WHERE LOWER(aid) = ?
                          UNION ALL
                          SELECT uid as username, pwd
                          FROM users
                          WHERE LOWER(uid) = ?;
                       """, (username, username))
    
        user_check = cursor.fetchall()
        # If account have both user artist, ask which want they want to use to sign in
        if len(user_check) > 1:
            print("Do you want to login as a user or as an artist")
            print("Enter 1 if you are a user")
            print("Enter 2 if you are a artist")
            
            while True:
                option = input("Choose your option: ")
                if option == '1':
                    type_of_user = "user"
                    break
                elif option == '2':
                    type_of_user = "artist"
                    break
                else:
                    print("Please choose correct option.")

            try:
                if password == user_check[1][1]:
                    print("Access granted")
                    if type_of_user == "user":
                        session = Session(connection, cursor, uid=username)
                        user_second_screen(session)
                    else:
                        session = Session(connection, cursor, aid=username)
                        artist_second_screen(session)
                else:
                    print("The username and password you entered do not match")
            except Exception:
                print("The username and password you entered do not match")
        # Sign in as user or artits base on sign in credentials
        else:
            try:
                cursor.execute("""SELECT uid as username, pwd
                                  FROM users
                                  WHERE LOWER(uid) = ?
                               """, (username, ))
                user_check = cursor.fetchone()
                if password == user_check[1]:
                    print("Access granted")

                    session = Session(connection, cursor, uid=username)
                    user_second_screen(session)
                else:
                    print("The username and password you entered do not match")
            except Exception as err:
                print(err)
                cursor.execute("""SELECT aid as username, pwd
                                  FROM artists
                                  WHERE LOWER(aid) = ?
                               """, (username, ))
                user_check = cursor.fetchone()
                if (user_check != None) and (password == user_check[1]):
                    print("Access granted")

                    session = Session(connection, cursor, aid=username)
                    artist_second_screen(session)
                else:
                    print("The username and password you entered do not match")

def sign_up(connection, cursor):
    """
        Create account for user
    """
    clear_screen()
    while True:
        print("-----------------Sign Up-----------------")
        username = input("Enter your username: ")
        cursor.execute("""SELECT uid
                          FROM users
                          WHERE uid = ?;
                       """, (username, ))
        username_check = cursor.fetchone()
        # Check if username already exist
        try:
            if username == username_check[0]:
                print("This username has already been taken. Please enter different username")
                continue
        except:
            break
    
    name = input("Enter Your Name: ")
    # Check if password and confirm password match
    while True:
        password = getpass("Enter your password: ")
        confirm_password = getpass("Confirm your password: ")
        if password == confirm_password:
            break
        print("Password and confirm password not match")

    # Insert new user into database
    data = (username, name, password)
    cursor.execute("INSERT INTO users(uid, name, pwd) VALUES(?, ?, ?);", data)
    connection.commit()
    first_screen(connection, cursor)

def user_second_screen(session):
    clear_screen()

    while True:
        if not session.has_started():
            clear_screen()
            print("Enter 1: Start session")
            print("Enter 2: Search for songs/playlists")
            print("Enter 3: Search for artists")


            print("Enter 4: Log out")
            print("Enter 5: Quit")
            option = input("Choose your option: ")
            if option == '1':
                session.start()
            elif option == '2':
                clear_screen()
                song_search(session)
            elif option == '3':
                artist_search(session)
            elif option == '4':
                first_screen(session.get_conn(), session.get_cursor())
            elif option == '5':
                if session.has_started():
                    session.end()
                stop_program(session.get_conn(), session.get_cursor())
            else:
                print("Please choose correct option.")
        else:
            clear_screen()
            print("-----------------In Session-----------------")
            print("--------------------------------------------")
            print("Enter 1: Search for songs/playlists")
            print("Enter 2: Search for artists")
            print("Enter 3: End session")
            print("Enter 4: Log out")
            print("Enter 5: Quit")
            option = input("Choose your option: ")
            if option == '1':
                clear_screen()
                song_search(session)
            elif option == '2':
                clear_screen()
                artist_search(session)
            elif option == '3':
                session.end()
            elif option == '4':
                session.end()
                first_screen(session.get_conn(), session.get_cursor())
            elif option == '5':
                session.end()
                stop_program(session.get_conn(), session.get_cursor())
            else:
                print("Please choose correct option.")

def artist_second_screen(session):
    while True:
        # print instructions
        print("Enter 1: Add a Song")
        print("Enter 2: Find Top Fans and Playlists")
        print("Enter 3: Logout")
        print("Enter 4: Quit")

        # prompt user to enter input
        option = input("Choose your option: ")

        # if the artist wants to add a song
        if option == "1":
            add_song(session)
        # if the artist wants to see top fans and playlists
        elif option == "2":
            clear_screen()
            display_top_artist_fans(session)
            display_line()
            display_top_artist_playlists(session)
            display_line()
        # if the artist wants to logout
        elif option == "3":
            return
        # if the artist wants to exit the program
        elif option == "4":
            stop_program(session.get_conn(), session.get_cursor())
