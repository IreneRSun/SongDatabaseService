def get_next_sno(cursor, uid):
    """
      Retrieves the next available sno
    """

    cursor.execute("""SELECT MAX(sno)
					  FROM sessions
					  WHERE uid = ?;
       			   """, (uid, ))

    row = cursor.fetchone()
    if row[0] == None:
        return 0
    else:
        return row[0] + 1

class Session:
	def __init__(self, connection, cursor, uid=None, aid=None):
		# Ensure only one id is specified
		assert (uid == None or aid == None) and (uid != aid) 

		self.connection = connection
		self.cursor = cursor

		self.id = uid if uid != None else aid
		self.id_is_user = uid != None

		self.sno = None
		self.has_session = False

	def has_started(self):
		return self.has_session

	def is_user(self):
		return self.id_is_user

	def get_id(self):
		return self.id

	def get_sno(self):
		return self.sno

	def get_cursor(self):
		return self.cursor

	def start(self):
		assert not self.has_started()
		assert self.is_user()

		self.sno = get_next_sno(self.get_cursor(), self.id)
		self.has_session = True

		self.cursor.execute("INSERT INTO sessions (uid, sno, start) VALUES (?, ?, CURRENT_DATE)", (self.get_id(), self.get_sno()))
		self.connection.commit()

	def end(self):
		assert self.has_started()

		self.cursor.execute("UPDATE sessions SET end=CURRENT_DATE WHERE uid=? AND sno=?", (self.get_id(), self.get_sno()))
		connection.commit()

		self.sno = None
		self.has_session = False