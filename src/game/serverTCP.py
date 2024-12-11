import socket
import game.crypto as crypto
import keyExchange as keyEx
import select

from .RSAConn	import RSAConn


class ServerTCP:
	BUFFER_SIZE = 20000
	def __init__(self):
		self.crypto = crypto.cryptographic(32)
		self.keyEx = keyEx(self.crypto);

	def bindServer(self, TCP_IP = '127.0.0.1', TCP_PORT = 5005):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # allow for polling
		    
		self.s.bind((TCP_IP, TCP_PORT))
		self.s.listen(30)

	def newConnection(self):
		ready, _, _ = select.select([self.s], [], [])
		if len(ready) == 0:
			return None
		conn, _ = ready[0].accept()
		self.keyEx.initConnection(conn);
		return RSAConn(crypto=self.crypto, conn=conn)
