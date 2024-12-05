import battleship.battleship_pb2 as pb
from .types		import BoardPoint
from dataclasses	import dataclass

GameEnd	= 'game-end'
Update	= 'update'

class Register(str):
	pass

class InvalidProtocol(Exception):
	pass

class Protocol:

	def makeHit(self, bp : BoardPoint):
		h = pb.Hit()
		h.row = bp.y
		h.col = bp.x
		return h
	def makeBoardPoint(self, h : pb.Hit):
		return BoardPoint(
			x = h.col,
			y = h.row
		)

	def setToken(self, token):
		self.token = token

	def makeRegisterReq(self, name : str):
		t = pb.Request()
		t.token = 0
		t.type = pb.RqType.RQ_REGISTER
		t.name = name
		return t.SerializeToString()
		
	def makeHitReq(self, bp : BoardPoint):
		t = pb.Request()
		t.token = self.token
		t.type = pb.RqType.RQ_HIT;

		t.hit.CopyFrom(self.makeHit(bp))

		return t.SerializeToString()

	def makeUpdateReq(self):
		t = pb.Request()
		t.token = self.token
		t.type = pb.RqType.RQ_REGISTER
		return t.SerializeToString()


	def parseRequest(self, s : str):
		r = pb.Request()
		r.ParseFromString(s)

		if r.type == pb.RqType.RQ_REGISTER:
			return Register(r.name)
		elif r.type == pb.RqType.RQ_UPDATE:
			return Update
		elif r.type == pb.RqType.RQ_HIT:
			return self.makeBoardPoint(r.hit)
		else:
			raise InvalidProtocol()

	def parseResponse(self, s : str):
		r = pb.Response()
		r.ParseFromString(s)
		if r.type == pb.RsType.RS_HIT:
			return BoardPoint(
				x = r.hit.col,
				y = r.hit.row
			)
		elif r.type == pb.RsType.RS_LAST_HIT_UPDATE:
			return r.miss
		elif r.type == RS_GAME_END:
			return GameEnd
		elif r.type == RS_INVALID_VALUE:
			return None
		else:
			raise InvalidProtocol()
