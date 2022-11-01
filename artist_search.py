from song_search import handle_select
from utils import *



def find_artists(cursor, keywords):
  """
    Finds artists that match the query and returns the top artists that match the query.
  """

  possible_artists = {}
  possible_artist_freq = {}
  artists = []

  # for each keyword, how many times can an artist be found?
  for keyword in keywords:
    cursor.execute("""
      WITH valid_aids AS (
        SELECT a.aid FROM artists a, perform p, songs s WHERE a.aid = p.aid AND p.sid = s.sid AND ((LOWER(a.name) LIKE ?) OR (LOWER(s.title) LIKE ?)) 
      )
      
      SELECT a.aid, a.name, a.nationality FROM artists a WHERE a.aid IN valid_aids;
    """, ('%' + keyword.lower() + '%', '%' + keyword.lower() + '%'))
    results = cursor.fetchall()

    # for each artist found, increment their freq
    for row in results:
      artist_id, artist_name, nationality = row
      
      # ensure artist data can be looked up later
      if artist_id not in possible_artists:
        # retrieve amount of songs performed by this artist
        cursor.execute("""
          SELECT COUNT(*) FROM songs s, artists a, perform p WHERE s.sid = p.sid AND p.aid = a.aid AND a.aid=?
        """, (artist_id, ))
        songs_performed = cursor.fetchone()[0]

        possible_artists[artist_id] = {
          "id": artist_id,
          "name": artist_name,
          "nationality": nationality,
          "songs_performed": songs_performed
        }
        possible_artist_freq[artist_id] = 0
        artists.append(possible_artists[artist_id])

      # increase artist found freq
      possible_artist_freq[artist_id] += 1

  # order the artists by their freq
  ordered_artists = sorted(artists, key=lambda artist: possible_artist_freq[artist["id"]], reverse=True)
  return ordered_artists

def find_artist_songs(cursor, aid):
  """
    Given the artist id, find all songs belonging to that artist
  """
  cursor.execute("""
    SELECT s.sid, s.title, s.duration FROM songs s, perform p, artists a
      WHERE a.aid = ? AND s.sid = p.sid AND p.aid = a.aid
  """, (aid, ))
  rows = cursor.fetchall()

  songs = []
  for row in rows:
    song_id, song_title, song_duration = row
    songs.append({
      "id": song_id,
      "title": song_title,
      "duration": song_duration
    })

  return songs

def handle_select(data, session):
  songs = find_artist_songs(session.get_cursor(), data["id"])

  print(f"Artist - {data['name']}")
  display_line()

  handle_page_logic(songs, session, on_select=song_handle_select)

def song_handle_select(data, session):
  # TODO: song actions
  pass
    

# def show_artist_option(option_num, artist_data):
#     print(option_num, "\t", f"{artist_data['name']} - {artist_data['nationality']} - {artist_data['songs_performed']} songs performed")

def artist_search(session):
  print("Please enter the artist or song you want to find the artist of")
  print("To stop searching, enter a blank line")
  display_line()

  keywords = get_keywords()
  if isinstance(keywords, str):
    return

  artists = find_artists(session.get_cursor(), keywords)
  
  handle_page_logic(artists, session, on_select=handle_select)