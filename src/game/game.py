from .clientTCP	        import ClientTCP
from .gui		import Gui, GameQuit
from .circleCross	import CircleCross, FieldType
from .types		import Point
from .circleCross	import Field, BoardPoint
import time

class Game:
	def __init__(self):
		self.gui = Gui(Point(800,800))
		self.tcp = ClientTCP()
		
	def run(self):
                check = 0;
                while True:
                        if self.tcp.connectServer() == 1:
                                break;
                        self.tick(self.tcp.turn);
                        
                while self.tcp.sign == None:
                        self.tcp.clientRead();
                        self.tick(self.tcp.turn);

                    
                print("Gui ustawione");   
                self.gui.setSign(self.tcp.sign);
                
                while True:
                        
                        if self.tcp.turn == 0 or self.tcp.turn == -1:
                                bp = self.tcp.clientRead();
                                
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
                                
                        if self.tcp.turn == 1 and  self.gui.game.move_done == 1:
                                send_data = int.from_bytes(self.gui.game.last.asTuple());
                                self.tcp.clientSend(send_data.to_bytes(32));
                                self.gui.game.move_done = 0;
                               
                        self.tick(self.tcp.turn);


                        
	def tick(self,turn):
		try:
			self.gui.tick(turn)
		except GameQuit:
			print('quit game')
			exit()
