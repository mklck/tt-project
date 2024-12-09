class RSAConn:
	BUFF_SIZE = 128
	def __init__(self, conn, crypto):
		self.conn = conn
		self.crypto = crypto
	def close(self):
		self.conn.close()
	def send(self, data):
		t = self.crypto.encrypt(data)
		self.conn.send(data)
	def recv(self):
		data = self.conn.recv(self.BUFF_SIZE)
		return self.crypto(decrypt)
