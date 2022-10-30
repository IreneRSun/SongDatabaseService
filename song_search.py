from utils import *

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

def show_playlist(cursor, pid):
    """
    display songs in playlist
    :param cursor: cursor used to get the songs in the playlist
    :param pid: the id of the playlist to display the songs of
    :return: N/A
    """
    display_line()
    print("Songs in this Playlist")
    # query for songs in the playlist
    cursor.execute("""SELECT songs.sid, songs.title, songs.duration
                    FROM songs, plinclude
                    WHERE plinclude.pid = :pid
                    AND songs.sid = plinclude.sid;""", {"pid": pid})
    # fetch results
    results = cursor.fetchall()
    # display results
    for row in results:
        print(row)


def handle_select(action, results, cursor):
    """
    handle the user selecting a song/playlist from the results
    :param action: user input indicating which action to take (list of str)
    :param results: the ordered list of songs and playlists that contain a keyword (list of tuples)
    :param cursor: the cursor used to get data from the database
    :return: N/A
    """
    result_num = action[1]
    # if the result_num is a number
    if result_num.isdigit():
        result_num = int(result_num)
        # if result_num is not in range
        if result_num > len(results) or result_num < 1:
            print("Invalid input")
        # if result_num is in range
        else:
            # get the type (song or playlist) of the result selected
            result_type = results[result_num - 1][0]
            print(result_type)
            # handle song selection
            if result_type == "Song":
            # --------- implement song actions ---------
                pass
            # handle playlist selection
            elif result_type == "Playlist":
                # get pid of playlist
                pid = results[result_num - 1][1]
                # show songs in playlist
                show_playlist(cursor, pid)
    # if the result_num is not a number
    else:
        print("Invalid input")


def song_search(connection, cursor, uid=None, aid=None):
    """
    implements process to search for songs/playlists that contain entered keywords
    :param connection: connection to the database
    :param cursor: the cursor to use to query and manipulate the database
    :param uid: the user id of the user, if user is a normal user
    :param aid: the artist id of the artist, if user is an artist
    :return: N/A
    """
    # print instructions for searching
    print("When prompted, enter the specified details")
    print("To stop searching, enter a blank line")
    display_line()

    # get keywords from user
    keywords = get_keywords()
    # if user inputted a blank line
    if isinstance(keywords, str):
        return

    # get rows of songs/playlists that contain the keywords (contains duplicates)
    matches = get_matches(cursor, keywords)

    # sort the rows according to the number of matching keywords
    sorted(matches, key=lambda x: matches.count(x), reverse=True)

    # remove duplicates rows
    matches = remove_dupes(matches)

    handle_page_logic(matches, cursor, on_select=handle_select)
