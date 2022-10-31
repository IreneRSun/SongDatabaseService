def get_sno(connection, cursor, uid):
    """
      Retrieves the highest sno
    """

    cursor.execute("""SELECT MAX(sno)
					  FROM sessions
					  WHERE uid = ?;
       			   """, (uid, ))

    row = cursor.fetchone()
    if row[0] == None:
        return 0
    else:
        return row[0]

def start_session(connection, cursor, uid, sno):
	"""
	Starts a session for a user.
	"""

	cursor.execute("INSERT INTO sessions (uid, sno, start) VALUES (?, ?, CURRENT_DATE)", (uid, sno))
	connection.commit()

def end_session(connection, cursor, uid, sno):
	"""
	Stops any active session for a user.
	"""

	cursor.execute("UPDATE sessions SET end=CURRENT_DATE WHERE uid=? AND sno=?", (uid, sno))
	connection.commit()
