from song_search import song_search
from artist_search import artist_search
from artist_stats import *
from add_song import add_song
from getpass import getpass
from session import *
from utils import clear_screen

def first_screen(connection, cursor):
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
            quit()
        else:
            print("Please choose correct option.")

def sign_in(connection, cursor):
    clear_screen()

    while True:
        username = input("Enter your username: ").lower()
        password = getpass("Enter your password: ")
        cursor.execute("""SELECT aid as username, pwd
                          FROM artists
                          WHERE LOWER(aid) = ?
                          UNION ALL
                          SELECT uid as username, pwd
                          FROM users
                          WHERE LOWER(uid) = ?;
                       """, (username, username))
    
        user_check = cursor.fetchall()
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
            except:
                print("The username and password you entered do not match")
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
            except:
                cursor.execute("""SELECT aid as username, pwd
                                  FROM artists
                                  WHERE LOWER(aid) = ?
                               """, (username, ))
                user_check = cursor.fetchone()
                if password == user_check[1]:
                    print("Access granted")

                    session = Session(connection, cursor, aid=username)
                    artist_second_screen(session)
                else:
                    print("The username and password you entered do not match")

def sign_up(connection, cursor):
    while True:
        username = input("Enter your username: ")
        cursor.execute("""SELECT uid
                          FROM users
                          WHERE uid = ?;
                       """, (username, ))
        username_check = cursor.fetchone()
        try:
            if username == username_check[0]:
                print("This username has already been taken. Please enter different username")
                continue
        except:
            break
    
    name = input("Enter Your Name: ")
    while True:
        password = getpass("Enter your password: ")
        confirm_password = getpass("Confirm your password: ")
        if password == confirm_password:
            break
        print("")

    data = (username, name, password)
    cursor.execute("INSERT INTO users(uid, name, pwd) VALUES(?, ?, ?);", data)
    connection.commit()
    first_screen(connection, cursor)

def user_second_screen(session):
    clear_screen()

    while True:
        if not session.has_started():
            while True:
                clear_screen()
                print("Enter 1: Start session")
                print("Enter 2: Search for songs/playlists")
                print("Enter 3: Search for artists")


                print("Enter : Log out")
                print("Enter : Quit")
                option = input("Choose your option: ")
                if option == '1':
                    session.start()
                    break
                elif option == '2':
                    clear_screen()
                    song_search(session)
                elif option == '3':
                    artist_search(session)
                elif option == '':
                    session.end()
                    first_screen(connection, cursor)
                elif option == '':
                    session.end()
                    quit()
                else:
                    print("Please choose correct option.")
        else:
            while True:
                clear_screen()
                print("-----------------In Session-----------------")
                print("--------------------------------------------")
                
                print("Enter 1: Search for songs/playlists")
                print("Enter 2: Search for artists")


                print("Enter 3: End session")
                print("Enter : Log out")
                print("Enter : Quit")
                option = input("Choose your option: ")
                if option == '1':
                    clear_screen()
                    song_search(session)
                elif option == '2':
                    clear_screen()
                    artist_search(session)
                elif option == '3':
                    session.end()
                    break
                elif option == '':
                    clear_screen()
                elif option == '':
                    session.end()
                    quit()
                else:
                    print("Please choose correct option.")

def artist_second_screen(session):
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
        print("Your top fans")
        data = get_top_fans(session)
        display_top_artist_fans(session, data)
        print("Your top playlists")
        data = get_top_playlists(session)
        display_top_artist_playlists(session, data)
    # if the artist wants to logout
    elif option == "3":
        return
    # if the artist wants to exit the program
    elif option == "4":
        quit()
