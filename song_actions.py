from utils import check_blank, clear_screen, display_line, stop_program, handle_page_logic

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
    cursor.execute("INSERT INTO listen (uid, sno, sid, cnt) VALUES (?, ?, ?, 1)", (session.get_id(), session.get_sno(), sid))
  else:
    cursor.execute("UPDATE listen SET cnt=cnt + 1 WHERE uid=? AND sno=? AND sid=?", (session.get_id(), session.get_sno(), sid))
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
    artists.append(row[0])

  # Find all playlists the song exists in
  cursor.execute("""
    SELECT DISTINCT pl.title FROM playlists pl, plinclude pli WHERE pli.sid = ? AND pli.pid = pl.pid
  """, (sid, ))
  playlist_rows = cursor.fetchall()
  playlists = []
  for row in playlist_rows:
    playlists.append(row[0])

  # Return results
  data = {
    "id": song_info_result[0],
    "title": song_info_result[1],
    "duration": song_info_result[2],
    "artists": artists,
    "playlists": playlists
  }

  return data



def add_song_to_playlist(session, sid, plid, order):
  session.get_cursor().execute("""INSERT INTO plinclude VALUES (?, ?, ?);""", (plid, sid, order))
  session.get_conn().commit()


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


def add_playlist(session):
  cursor = session.get_cursor()
  connection = session.get_conn()

  name = input("Enter name of new playlist: ")
  pid = get_unique_pid(session.get_cursor())

  cursor.execute("INSERT INTO playlists VALUES (?, ?, ?);", (pid, name, session.get_id()))
  connection.commit()

  return pid

def select_playlist(session):  
  # Get all playlists the user owns
  cursor = session.get_cursor()
  cursor.execute("""
    SELECT pid, title FROM playlists WHERE uid=?
  """, (session.get_id(), ))
  playlist_rows = cursor.fetchall()

  # Ask for playlist to be selected
  while True:
    # Display possible options
    print("Please select a playlist to add this song to")
    display_line()
    print("1) Create New Playlist")
    for placing, row in enumerate(playlist_rows, 2):
      _, title = row
      print(f"{placing}) {title}")

    # Get valid input
    try:
      selection = int(input("Please select an option: "))      
    except:
      clear_screen()
      print("Invalid input")
      continue
    if selection < 1 or selection > len(playlist_rows) + 1:
      clear_screen()
      print("Invalid input")
      continue

    if selection == 1:
      plid = add_playlist(session)
    else:
      plid = playlist_rows[selection - 2][0]
    
    return plid
      
def get_order():
  clear_screen()
  while True:
    try:
      order = int(input("What order should this song be placed at: "))
      return order
    except:
      clear_screen()
      print("Invalid input.")

def has_song(session, plid, sid):
  cursor = session.get_cursor()
  cursor.execute("SELECT 1 FROM plinclude WHERE pid=? AND sid=?", (plid, sid))
  has_song = cursor.fetchone() != None

  return has_song

def playlist_select_callback(data, session):
  pass

def song_actions(session, sid):
  data = get_song_information(session, sid)

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
      # listen to song
      clear_screen()
      listen_to_song(session, sid)
      print(f"You listened to {data['title']}!")
    elif action == "2":
      # view more information about a song
      clear_screen()
      
      print(f"Song Information - {data['title']}")
      display_line()
      
      print("ID: ", data["id"])
      print("Duration: ", data["duration"])

      print("Artists: ", " ".join(data["artists"]))
      print("Playlists:")

      for playlist in data["playlists"]:
        print(f"- {playlist}")

      display_line()
    elif action == "3":
      # add song to a playlist
      clear_screen()
      plid = select_playlist(session)
    
      if has_song(session, plid, sid):
        clear_screen()
        print("This playlist already has this song!")
      else:
        order = get_order()
        add_song_to_playlist(session, sid, plid, order)

        clear_screen()
        print("Added song!")
    elif action == "4":
      # quit
      stop_program(session.get_conn(), session.get_cursor())
  
