from utils import display_line


def get_top_fans(session, limit = 3):
  """
    Finds the top users who have listened the most to an artists' songs.
  """
  assert not session.is_user()

  cursor = session.get_cursor()
  cursor.execute("""
    SELECT u.uid, u.name, SUM(l.cnt) AS listen_time FROM users u, listen l, perform p, artists a, songs s
      WHERE a.aid = ? AND s.sid = p.sid AND p.aid = a.aid AND l.sid = s.sid AND u.uid = l.uid
      GROUP BY u.uid
      ORDER BY listen_time DESC
      LIMIT ?
  """, (session.get_id(), limit))

  rows = cursor.fetchall()

  # convert tuples to dicts
  top_fans = []
  for row in rows:
    user_id, user_name, listen_time = row
    top_fans.append({
      "id": user_id,
      "name": user_name,
      "listen_time": listen_time
    })

  return top_fans

def get_top_playlists(session, limit = 3):
  """
    Finds the top playlist that has the most songs of a specific artist
    Returns a list containing the playlist id, name, and song count
  """
  assert not session.is_user()

  cursor = session.get_cursor()
  cursor.execute("""
    SELECT pl.pid, pl.title, COUNT(s.sid) AS artist_song_count
      FROM playlists pl, plinclude pli, songs s, artists a, perform p
      WHERE a.aid = ? AND s.sid = p.sid AND p.aid = a.aid
          AND pl.pid = pli.pid AND pli.sid = s.sid
      GROUP BY pl.pid
      ORDER BY artist_song_count DESC
      LIMIT ?
  """, (session.get_id(), limit))
  rows = cursor.fetchall()

  # convert tuples to dicts
  top_playlists = []
  for row in rows:
    playlist_id, playlist_title, song_count = row
    top_playlists.append({
      "id": playlist_id,
      "title": playlist_title,
      "artist_song_count": song_count
    })

  return top_playlists

def display_top_artist_playlists(session, artist_data): 
  top_playlists = enumerate(get_top_playlists(session, artist_data["id"]), 1)

  display_line()
  for position, playlist in top_playlists:
    print(position, '\t', playlist)

def display_top_artist_fans(session, artist_data):
  top_fans = enumerate(get_top_fans(session, artist_data["id"]), 1)

  display_line()
  for position, fan in top_fans:
    print(position, '\t', fan)