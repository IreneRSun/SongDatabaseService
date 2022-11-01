from song_actions import song_actions
from utils import *
import os


def get_matches(cursor, keywords):
    """
    get info on songs and playlists that contain the keywords
    :param cursor: cursor used to search for songs and playlists that contain the keywords
    :param keywords: keywords to search for (list of str)
    :return: info about songs and playlists that contain the keywords (list of tuples)
    """
    # create list for storing songs and playlists that contain the keywords
    match = []
    # search for songs and playlists containing the keywords
    for keyword in keywords:
        # search for songs containing the keyword
        cursor.execute("""SELECT "Song", sid, title, duration
                        FROM songs
                        WHERE lower(title) LIKE ?;""",
                       ("%" + keyword.lower() + "%",))
        # fetch results
        rows = cursor.fetchall()
        # add results to the list
        match = match + rows

        # search for playlists containing the keyword
        cursor.execute("""SELECT "Playlist", playlists.pid, playlists.title, COUNT(duration)
                        FROM playlists, plinclude, songs
                        WHERE lower(playlists.title) LIKE ?
                        AND playlists.pid = plinclude.pid
                        AND plinclude.sid = songs.sid
                        GROUP BY playlists.pid, playlists.title;""",
                       ("%" + keyword.lower() + "%",))
        # fetch results
        rows = cursor.fetchall()
        # add results to the list match
        match = match + rows
    return match


def remove_dupes(matches):
    """
    remove duplicates from a list while maintaining list order
    :param matches: list to remove duplicates from (list of tuples)
    :return: list with duplicates removed (list of tuples)
    """
    exist = set()  # for storing elements that already exist in the list
    new = []  # new list with duplicates removed
    # remove duplicates
    for result in matches:
        # if result has not already been added
        if result not in exist:
            # add result
            exist.add(result)
            new.append(result)
    return new


def show_playlist(session, pid):
    """
    display songs in playlist
    :param session: contains user and listening session data
    :param pid: the id of the playlist to display the songs of
    :param uid: the user id (str)
    :return: N/A
    """
    os.system("cls")
    display_line()
    print("Songs in this Playlist")
    # query for songs in the playlist
    cursor = session.get_cursor()

    cursor.execute("""SELECT songs.sid, songs.title, songs.duration
                    FROM songs, plinclude
                    WHERE plinclude.pid = :pid
                    AND songs.sid = plinclude.sid;""", {"pid": pid})
    # fetch results
    results = cursor.fetchall()
    # display results
    for num, row in enumerate(results, 1):
        print(num, "sid:", row[0], "title:", row[1], "duration:", row[2])
    # allow user to select a song
    while True:
        action = input("To select a song, enter its song number")
        # if a blank line was entered
        if check_blank(action):
            return
        # if the user wants to exit the program
        if action.lower() == "quit":
            if session.has_started():
                session.end()
            quit()
        # check input
        if action.isdigit():
            choice = int(action[1])
            # make sure choice is within bounds
            if choice > len(results) or choice < 1:
                print("Please select an existing song number")
            else:
                # get data to pass on
                data = ["Song"]
                data = data + results[choice - 1]
                handle_select(data, session)
        # if input is invalid
        else:
            print("Invalid input")


def handle_select(data, session):
    """
    handle the user selecting a song/playlist from the results
    :param data: specific song/playlist selected
    :param session: contains user and listening data
    :return: N/A
    """
    # get the type (song or playlist) of the result selected
    result_type = data[0]
    # handle song selection
    if result_type == "Song":
        # get sid of the song
        sid = data[1]
        # handle song actions
        song_actions(session, sid)
    # handle playlist selection
    elif result_type == "Playlist":
        # get pid of playlist
        pid = data[1]
        # show songs in playlist
        show_playlist(session, pid)


def song_search(session):
    """
    implements process to search for songs/playlists that contain entered keywords
    :param session: contains user and listening session data
    :return: N/A
    """
    # print instructions for searching
    print("When prompted, enter the specified details")
    print("To stop searching, enter a blank line")
    display_line()

    # get keywords from user
    keywords = get_keywords()

    # check if user wants to go back or exit the program
    if isinstance(keywords, str):
        # if user entered quit
        if keywords.lower() == "quit":
            if session.has_started():
                session.end()
                
            quit()
        # if user inputted a blank line
        else:
            return

    # get rows of songs/playlists that contain the keywords (contains duplicates)
    matches = get_matches(session.get_cursor(), keywords)

    # sort the rows according to the number of matching keywords
    sorted(matches, key=lambda x: matches.count(x), reverse=True)

    # remove duplicates rows
    matches = remove_dupes(matches)

    handle_page_logic(matches, session, on_select=handle_select)
