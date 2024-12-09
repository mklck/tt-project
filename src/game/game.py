from .client_tcp	import ClientTCP
from .gui		import Gui, GameQuit
from .circleCross	import CircleCross, FieldType
from .types		import Point

class Game:
	def __init__(self):
		self.gui = Gui(Point(800,800))
		self.tcp = ClientTCP()
		self.tcp.connect_serwer()
	def run(self):
		while True:
			self.tick()
	def tick(self):
		try:
			self.gui.tick()
		except GameQuit:
			print('quit game')
			exit()
