def first_screen(connection, cursor):
    print("Enter 1: Sign In")
    print("Enter 2: Sign Up")
    print("Enter 3: Exit")

    while True:
        option = input("Choose your option: ")
        if option == '1':
            sign_in(cursor)
        elif option == '2':
            sign_up(connection, cursor)
        elif option == '3':
            quit()
        else:
            print("Please choose correct option.")

def sign_in(cursor):
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    cursor.execute("""SELECT aid as username, pwd
                      FROM artists
                      WHERE aid = '""" + username + """'
                      UNION
                      SELECT uid as username, pwd
                      FROM users
                      WHERE uid = '""" + username + """';
                   """)

    user_check = cursor.fetchone()
    try:
        if password == user_check[1]:
            print("Access granted")
        else:
            print("The username and password you entered do not match")
    except:
        print("The username and password you entered do not match")

def sign_up(connection, cursor):
    while True:
        username = input("Enter your username: ")
        cursor.execute("""SELECT uid
                          FROM users
                          WHERE uid = '""" + username + """';
                       """)
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


