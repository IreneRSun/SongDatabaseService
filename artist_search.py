def get_keywords(query):
  """
    Given a query, returns relevant keywords in lowercase
    No duplicates will be returned.
  """
  keywords = set()
  for keyword in query.split(" "):
    if not keyword.lower() in keywords:
      keywords.add(keyword.lower())
  
  return keywords


def find_artists(cursor, query, limit = 5):
  """
    Finds artists that match the query and returns the top artists that match the query.
  """
  keywords = get_keywords(query)
  
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

      cursor.execute("""
        SELECT COUNT(*) FROM songs s, artists a, perform p WHERE s.sid = p.sid AND p.aid = a.aid AND a.aid=?
      """, (artist_id, ))
      songs_performed = cursor.fetchone()[0]
      
      # ensure artist data can be looked up later
      if artist_id not in possible_artists:
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

  # return at MAX "limit" artists
  return ordered_artists[:limit]



def artist_search(cursor):
  pass