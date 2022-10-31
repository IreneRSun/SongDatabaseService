from song_search import song_search
from artist_search import artist_search
from artist_stats import *
from add_song import add_song
from getpass import getpass
from start_end import *
import os

def first_screen(connection, cursor):
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
    os.system('clear')

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
                        user_second_screen(connection, cursor, username, False)
                    else:
                        artist_second_screen(connection, cursor, False)
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
                    user_second_screen(connection, cursor, username, False)
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
                    artist_second_screen(connection, cursor, False)
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
    password = input("Enter your password: ")
    data = (username, name, password)
    cursor.execute("INSERT INTO users(uid, name, pwd) VALUES(?, ?, ?);", data)
    connection.commit()
    first_screen(connection, cursor)

def user_second_screen(connection, cursor, uid, session):
    while True:
        os.system("clear")
        if session == False:
            while True:
                print("Enter 1: Start session")
                print("Enter 2: Search for songs/playlists")
                print("Enter 3: Search for artists")


                print("Enter : Log out")
                print("Enter : Quit")
                option = input("Choose your option: ")
                if option == '1':
                    sno = get_sno(connection, cursor, uid) + 1
                    start_session(connection, cursor, uid, sno)
                    session = True
                    break
                elif option == '2':
                    # if user play the song, run session_start(connection, cursor), Ill add it later
                    song_search(connection, cursor, session)
                elif option == '3':
                    artist_search(cursor)
                elif option == '':
                    first_screen(connection, cursor)
                elif option == '':
                    quit()
                else:
                    print("Please choose correct option.")
        else:
            while True:
                print("-----------------In Session-----------------")
                print("--------------------------------------------")
                
                print("Enter 1: Search for songs/playlists")
                print("Enter 2: Search for artists")


                print("Enter 3: End session")
                print("Enter : Log out")
                print("Enter : Quit")
                option = input("Choose your option: ")
                if option == '1':
                    pass
                elif option == '2':
                    os.system('clear')
                    song_search(connection, cursor, session)
                elif option == '3':
                    sno = get_sno(connection, cursor, uid)
                    end_session(connection, cursor, uid, sno)
                    session = False
                    break
                elif option == '':
                    os.system('clear')
                    artist_search(cursor)
                elif option == '':
                    
                    quit()
                else:
                    print("Please choose correct option.")

def artist_second_screen(connection, cursor, session, aid):
    # print instructions
    print("Enter 1: Add a Song")
    print("Enter 2: Find Top Fans and Playlists")
    print("Enter 3: Logout")
    print("Enter 4: Quit")

    # prompt user to enter input
    option = input("Choose your option: ")

    # if the artist wants to add a song
    if option == "1":
        add_song(connection, cursor, aid)
    # if the artist wants to see top fans and playlists
    elif option == "2":
        print("Your top fans")
        data = get_top_fans(cursor, aid)
        display_top_artist_fans(cursor, data)
        print("Your top playlists")
        data = get_top_playlists(cursor, aid)
        display_top_artist_playlists(cursor, data)
    # if the artist wants to logout
    elif option == "3":
        return
    # if the artist wants to exit the program
    elif option == "4":
        quit()
