def display_line():
    """
    print a line of dashes
    :return: N/A
    """
    print("-" * 80)


def check_blank(inp):
    """
    checks whether the user entered a blank line
    :return: whether the user entered a blank line (bool)
    """
    return inp == "" or inp.isspace()


def get_title():
    """
    gets user input for the title of the song to add
    :return: a blank line if the user enters a blank line (str), otherwise returns the title of the song (str)
    """
    return input("Enter title of song: ")


def get_duration():
    """
    gets user input for the duration of the song to add
    :return: a blank line if the user enters a blank line (str), otherwise returns the duration of the song (int)
    """
    while True:
        # get user input
        duration = input("Enter duration of song: ")
        # if a blank line is entered
        if check_blank(duration):
            break
        # if an integer is entered
        elif duration.isdigit():
            duration = int(duration)
            break
        # handle invalid input
        else:
            print("Invalid input")
    return duration


def find_song(user_aid, title, duration, cursor):
    """
    queries for a song performed by the given artist, with the given title and duration from a database
    :param user_aid: the artist id to use in the query (str)
    :param title: the title of the song to use in the query (str)
    :param duration: the duration (int)
    :param cursor: the cursor used to search the database for songs that match the query
    :return: query result (tuple)
    """
    # query for song with the given title and duration for the given user_aid
    cursor.execute("""SELECT * FROM songs, perform
                    WHERE songs.sid = perform.sid
                    AND perform.aid = :aid
                    AND lower(songs.title) = :title
                    AND songs.duration = :duration;""",
                   {"aid": user_aid, "title": title.lower(), "duration": duration})

    # fetch query results
    return cursor.fetchone()


def get_aids(cursor, user_aid):
    """
    get other artists who also performed the song that is being added
    :param cursor: the cursor used to search the database for existing artists
    :param user_aid: the artist id of the user to ensure result only contains other artists (str)
    :return: a blank line if the user enters a blank line (str), otherwise returns the artist ids of other artists who
    performed the song (list of str)
    """
    while True:
        # get user input for other aids
        print("If there are no other artists who performed this song, enter None")
        aids = input("Otherwise enter the aids of the other artists of this song, seperating each with whitespace: ")
        aids = aids.lower()
        # check if user entered a blank line
        if check_blank(aids):
            break
        # check if there are no other people who have performed this song
        if aids == "none":
            aids = []
            break
        # check user input if there are other artists
        aids = aids.split()
        checked = 0
        for aid in aids:
            # search for aid in artists
            cursor.execute("SELECT * FROM artists WHERE aid = :aid AND aid != :uaid;",
                           {"aid": aid, "uaid": user_aid})
            result = cursor.fetchone()
            # if artist not found
            if result is None:
                print(f"aid not found: {aid}")
                checked = 0
                break
            # increment checked if artist is found
            else:
                checked += 1
        # break while loop if all aids exist
        if checked == len(aids):
            break
    return aids


def get_unique_sid(cursor):
    """
    generate a unique sid for the new song
    :param cursor: the cursor used to get the existing sids from the database
    :return: the unique sid (int)
    """
    sid = 0
    found = False
    # get current sids
    cursor.execute("SELECT sid FROM songs;")
    results = cursor.fetchall()
    # increment sid until a non-existing sid is found
    while not found:
        if tuple([sid]) in results:
            sid += 1
        else:
            found = True
    return sid


def insert_song(sid, title, duration, user_aid, aids, cursor, connection):
    """
    add a song to the database
    :param sid: the sid to use when adding the song into the database (int)
    :param title: the title of the song to add to the database (str)
    :param duration: the duration of the song to add to the database (int)
    :param user_aid: the artist adding the song (str)
    :param aids: the other artists who performed this song (list of str)
    :param cursor: the cursor used to get the existing sids from the database
    :param connection: the connection to the database
    :return: N/A
    """
    # add the new song to songs
    cursor.execute("INSERT INTO songs VALUES (:sid, :title, :duration);",
                   {"sid": sid, "title": title, "duration": duration})

    # add the new song to perform with the relevant artists
    # create list of the values to insert into perform
    insertions = [(user_aid, sid)]
    for aid in aids:
        insertions.append((aid, sid))
    # add the artists who performed the song into perform
    cursor.executemany("INSERT INTO perform VALUES (?, ?);", insertions)

    # commit changes
    connection.commit()


def add_song(connection, cursor, user_aid):
    """
    implements process to add song to database
    :param connection: connection to the database
    :param cursor: the cursor to use to query and manipulate the database
    :param user_aid: the aid of the artist that is logged in (str)
    :return: N/A
    """
    # print instructions
    print("When prompted, enter the relevant song details")
    print("To stop adding a song, enter a blank line")
    display_line()

    # get title of the song
    title = get_title()
    # stop song adding if user enters a blank line
    if check_blank(title):
        return

    # get duration of the song
    duration = get_duration()
    # stop song adding if user enters a blank line
    if isinstance(duration, str):
        return

    # check if artist already has song with same title and duration
    find = find_song(user_aid, title, duration, cursor)

    # if song with same title and duration already exists
    if find is not None:
        # warn the user and reject it
        print("Song with same title and duration already exists")
        print("Song not added")

    # if song with same title and duration does not already exist
    else:
        # get other artists who also performed this song
        aids = get_aids(cursor, user_aid)
        # stop song adding if user enters a blank line
        if isinstance(aids, str):
            return

        # generate unique sid for the song
        sid = get_unique_sid(cursor)

        # add song to database
        insert_song(sid, title, duration, user_aid, aids, cursor, connection)

        # indicate that the song was successfully added
        print("Song added successfully")