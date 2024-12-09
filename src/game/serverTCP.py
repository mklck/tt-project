import socket
import game.crypto as crypto
import select

from enum	import Enum
from .RSAConn	import RSAConn

class Color(Enum):
    PUBLIC_KEY_EXCHANGE = 1
    PUBLIC_KEY_ACK = 2
    COMMUNICATION = 3

Color = Enum(
	'Color',
	[
		('PUBLIC_KEY_EXCHANGE_SERVER', 1),
		('CLIENT_KEY_ACK', 2),
		('PUBLIC_KEY_EXCHANGE_CLIENT', 3),
		('SERVER_KEY_ACK', 4),
		('COMMUNICATION', 5),
		('END_CONN', 6)
	]
)

class ServerTCP:
	BUFFER_SIZE = 20000
	def __init__(self):
		self.crypto = crypto.cryptographic(32)

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
		self.initConnection(conn)
		return RSAConn(crypto=self.crypto, conn=conn)

	def initConnection(self, conn):
		conn_state = Color.PUBLIC_KEY_EXCHANGE_SERVER

		while 1:
			match conn_state:
				case Color.PUBLIC_KEY_EXCHANGE_SERVER:

					print("Sending public key [integer]: {} and modulus: {}".format(
							self.crypto.RSA.key.exponent, 
							self.crypto.RSA.key.modulus
						)
					)
					conn.send(
						"PUBLIC_KEY".encode()
						+ (str(self.crypto.RSA.key.exponent)).encode()
						+ (" ").encode()
						+ (str(self.crypto.RSA.key.modulus)).encode()
					)
					conn_state = Color.CLIENT_KEY_ACK;
                             
				case Color.CLIENT_KEY_ACK:
					print("Waiting for publick key ACK from client")
					data = conn.recv(self.BUFFER_SIZE);
					print(data.decode());
					if data.decode()[0:7] == "KEY_ACK":
						conn_state = Color.PUBLIC_KEY_EXCHANGE_CLIENT;

				case Color.PUBLIC_KEY_EXCHANGE_CLIENT:
					data = conn.recv(self.BUFFER_SIZE);
					if data.decode()[0:10] == "PUBLIC_KEY":
						public_pair = data.decode()[10:].split();
						print("PUBLICE KEY GOT:", int(public_pair[0]) )
						self.crypto.RSA.key.exponent_sym = int(public_pair[0]);
						self.crypto.RSA.key.modulus_sym = int(public_pair[1]);
						conn.send("KEY_ACK".encode());
						return conn
