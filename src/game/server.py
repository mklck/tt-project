from .serverTCP         import ServerTCP
from .gui		import Gui, GameQuit
from .circleCross	import CircleCross, FieldType
from .types		import Point

class Server:
	def __init__(self):
                self.gui = Gui(Point(800,800))
                self.s = ServerTCP()
                self.s.bindServer()
	def run(self):
                while True:
                        if self.s.runServer() == 1:
                                break;
                        self.tick(self.s.turn);
                        
                self.gui.setSign(self.s.sign);
                while True:
                        
                        
                        if self.s.turn == 0:
                                self.s.serverRead();
                                
                        if self.s.turn == 1 and  self.gui.game.move_done == 1:
                                send_data = 'Cos do wyslania'
                                self.s.serverSend(send_data.encode());
                                self.gui.game.move_done = 0;
                        
                        self.tick(self.s.turn);
                        
	def tick(self,turn):
		try:
			self.gui.tick(turn)
		except GameQuit:
			print('quit game')
			exit()
			
def server():
	Server().run()
