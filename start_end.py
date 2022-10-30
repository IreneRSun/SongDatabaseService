def get_next_sno(cursor):
  """
    Retrieves the next sno to use for the session
  """

  cursor.execute("""
    SELECT (MAX(sno) OR 0) + 1 FROM sessions
  """)

  row = cursor.findone()

  return row[0]

def start_session(cursor, uid):
  """
    Starts a session for a user.
    If a user has an existing session, that session will be ended.
  """
  
  # End any existing session they have
  end_session(cursor, uid)

  sno = get_next_sno()

  cursor.execute("""
    INSERT INTO sessions (uid, sno, start) VALUES (?, ?, NOW())
  """, (uid, sno))

def end_session(cursor, uid):
  """
    Stops any active session for a user.
  """
  
  cursor.execute("""
    UPDATE sessions SET end=NOW() WHERE uid=? AND end=NULL
  """, (uid, ))