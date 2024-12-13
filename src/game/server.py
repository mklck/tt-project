from .serverTCP         import ServerTCP
from .gui		import Gui, GameQuit
from .circleCross	import CircleCross, FieldType
from .types		import Point
from .circleCross	import Field, BoardPoint
import time

class Server:
	def __init__(self):
                self.gui = Gui(Point(800,800))
                self.s = ServerTCP()
                self.s.bindServer()
	def run(self):

                check = 0;
                
                while True:
                        if self.s.runServer() == 1:
                                break;
                        self.tick(self.s.turn);
                        
                self.gui.setSign(self.s.sign);
                
                while True:
                        
                        if self.s.turn == 0:
                                bp = self.s.serverRead();
                                
                                if bp != None:
                                        bp = int.from_bytes(bp);
                                        x, y = tuple( bp.to_bytes(2) )
                                        bp = BoardPoint(x, y)
                                        if self.gui.game.player == FieldType.cross:
                                                field = Field(pos = bp, type=FieldType.circle)
                                        else:
                                                field = Field(pos = bp, type=FieldType.cross)
                                        self.gui.game.fields.append(field)
                                        check = 1;
                                
                        if self.s.turn == 1 and  self.gui.game.move_done == 1:
                                send_data = int.from_bytes(self.gui.game.last.asTuple());
                                self.s.serverSend(send_data.to_bytes(32));
                                #print("Dlugosc danych: ", len(send_data.encode()))
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
