from utils import check_blank, clear_screen, display_line, stop_program

def listen_to_song(session, sid):
  # Start session if no session was started
  if not session.has_started():
    session.start()

  cursor = session.get_cursor()
  connection = session.get_conn()

  # Check for existing song possibility
  cursor.execute("SELECT 1 FROM listen WHERE uid=? AND sno=? AND sid=?", (session.get_id(), session.get_sno(), sid))
  existing_song_listen_results = cursor.fetchone()
  
  if existing_song_listen_results == None:
    # insert
    pass
  else:
    # update
    pass
  connection.commit()

def get_song_information(session, sid):
  cursor = session.get_cursor()
  
  # First get the song information
  cursor.execute("SELECT s.sid, s.title, s.duration FROM songs s WHERE s.sid = ?", (sid, ))
  song_info_result = cursor.fetchone()

  # Get artists of the song
  cursor.execute("""
    SELECT a.name FROM artists a, perform p WHERE p.sid = ? AND p.aid = a.aid
  """, (sid, ))
  artists_rows = cursor.fetchall()
  artists = []
  for row in artists_rows:
    artists.append(row["name"])

  # Find all playlists the song exists in
  cursor.execute("""
    SELECT DISTINCT pl.title FROM playlists pl, plinclude pli WHERE pli.sid = ? AND pli.pid = pl.pid
  """, (sid, ))
  playlist_rows = cursor.fetchall()
  playlists = []
  for row in playlist_rows:
    playlists.append(row["title"])

  # Return results
  data = {
    "id": song_info_result[0],
    "title": song_info_result[1],
    "duration": song_info_result[2],
    "artists": artists,
    "playlists": playlists
  }

  return data



def add_song_to_playlist(connection, cursor, sid, plid, order):
  cursor.execute("""INSERT INTO plinclude VALUES (?, ?, ?);""", (plid, sid, order))
  connection.commit()


def get_unique_pid(cursor):
  pid = 0
  found = False
  # get current pids
  cursor.execute("SELECT pid FROM playlists;")
  results = cursor.fetchall()
  # increment sid until a non-existing pid is found
  while not found:
      if tuple([pid]) in results:
          pid += 1
      else:
          found = True
  return pid


def add_playlist(connection, cursor, uid, sid):
  name = input("Enter name of new playlist: ")
  pid = get_unique_pid(cursor)
  cursor.execute("INSERT INTO playlists VALUES (?, ?, ?);", (pid, name, uid))
  connection.commit()

def song_actions(session, sid):
  clear_screen()
  while True:
    print("Enter 1: Listen to the Song")
    print("Enter 2: View More Information About Song")
    print("Enter 3: Add song to a playlist")
    print("Enter 4: Quit")
    display_line()

    action = input("Which option would you like to choose? ")

    if check_blank(action):
      break

    if action == "1":
      clear_screen()
      listen_to_song(session, sid)
      return
    elif action == "2":
      clear_screen()
      data = get_song_information(session, sid)
      
      print(f"Song Information - {data['title']}")
      display_line()
      
      print("ID: ", data["id"])
      print("Duration: ", data["duration"])

      print("Artists: ", data["artists"].join(" "))
      print("Playlists: ")

      for playlist in data["playlists"]:
        print(playlist["name"])

      display_line()
    elif action == "3":
      # TODO: Add song to playlist 
      pass
    elif action == "4":
      stop_program(session.get_conn(), session.get_cursor())
  
