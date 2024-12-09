from .serverTCP import ServerTCP

class Server:
	def __init__(self):
		self.s = ServerTCP()
		self.s.bindServer()
		self.connections = list()
	def run(self):
		if c := self.s.newConnection():
			self.connections.append(c)
		

def server():
	Server().run()
