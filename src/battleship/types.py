from dataclasses	import dataclass, field
from typing		import Iterable, Tuple, Literal, cast

from .exceptions	import *

type Orientation = Literal['vertical', 'horizontal']
type Range = Tuple[int, int]

def saturate(min, max, num):
	if num < min:
		return min
	elif num > max:
		return max
	else:
		return num

class ShipSize(int):
	def __new__(cls, size):
		if not (1 <= size <= 4):
			raise InvalidShipSize(size)
		return super().__new__(cls, size)

@dataclass(frozen=True, eq=True)
class Point:
	x : int
	y : int

class BoardPoint(Point):
	""" Extends class Point by alphanumerical representation, and
	keeping position in rect (1, 1), (10, 10).
	"""
	COLUMNS = "abcdefghij"
	
	def __init__(self, x, y):
		super().__init__(x=x, y=y)
		r = range(1, 11)
		valid = self.x in r and self.y in r
		if not valid:
			raise ValueError(f'Point {self} not in rect (1, 1), (10, 10)')
			
	@classmethod
	def fromAlnum(cls, col : str, row : int):
		idx = cls.COLUMNS.index(col) + 1
		return cls(idx, row)
		
	@classmethod
	def newSaturated(cls, x, y):
		x = saturate(min=1, max=10, num=x)
		y = saturate(min=1, max=10, num=y)
		return cls(x=x, y=y)

	def toAlnum(self):
		return self.COLUMNS[self.x - 1], self.y


@dataclass(init=False)
class Rect:
	origin	: BoardPoint
	end	: BoardPoint
	area	: int

	def __init__(self, origin : BoardPoint, end : BoardPoint):
		self.origin = BoardPoint(min(origin.x, end.x), min(origin.y, end.y))
		self.end = BoardPoint(max(origin.x, end.x), max(origin.y, end.y))
		self.area = (self.end.x - self.origin.x + 1) * (self.end.y - self.origin.y + 1)
	
	def __contains__(self, p : BoardPoint):
		a = (self.origin.x <= p.x <= self.end.x)
		b = (self.origin.y <= p.y <= self.end.y)
		return a and b

	def overlap(self, other):
		rx0 = self.origin.x, self.end.x
		rx1 = other.origin.x, other.end.x
		
		ry0 = self.origin.y, self.end.y
		ry1 = other.origin.y, other.end.y

		return self.rangeOverlap(rx0, rx1) and self.rangeOverlap(ry0, ry1)
	def extends(self, other):
		return other.origin in self and other.end in self

	@staticmethod
	def rangeOverlap(a : Range, b : Range) -> bool:
		def _overlap(s0, e0, s1, e1):
			cond0 = (s0 <= s1 <= e0)
			cond1 = (s0 <= s1 <= e0)
			return cond0 or cond1
		return _overlap(*a, *b) or _overlap(*b, *a)


@dataclass(init=False)
class Ship:
	area	: Rect
	border	: Rect

	def __init__(self, size : ShipSize, origin : BoardPoint, orientation : Orientation):
		end = self._getShipEnd(size, origin, orientation)
		self.area = Rect(origin, end)
		self.border = self._getBorder()

	def _getShipEnd(self, size : ShipSize, origin : BoardPoint, o : Orientation):
		try:
			if o == 'vertical':
				return BoardPoint(origin.x, origin.y + size - 1)
			elif o == 'horizontal':
				return BoardPoint(origin.x + size - 1, origin.y)
			raise Exception(f'Invalid orientation {o}')
		except ValueError:
			raise ShipInvalidPosition(origin, o)
	
	def _getBorder(self):
		origin = BoardPoint.newSaturated(
			self.area.origin.x - 1,
			self.area.origin.y - 1
		)
		end = BoardPoint.newSaturated(
			self.area.end.x + 1,
			self.area.end.y + 1
		)
		return Rect(origin=origin, end=end)
	
	def collide(self, other) -> bool:
		return self.border.overlap(other.area)

	def belong(self, p : BoardPoint) -> bool:
		return p in self.area

	def getSize(self) -> ShipSize:
		return ShipSize(self.area.area)


@dataclass
class Board:	
	""" Stores ships and hits.
	For correct creation of board see BoardConstructor.
	"""
	ships : list[Ship]
	hits  : set[BoardPoint] = field(default_factory=set)
	def hit(self, p : BoardPoint):
		if p in self.hits:
			raise PositionHitBefore(p)
		self.hits.add(p)


@dataclass
class BoardConstructor:
	""" Implement board creation logic.
	For adding ships to board see: addShip(), addShipVer(), addShipHor().
	After adding all ships, use getBoard().
	"""
	ships : list = field(default_factory=list)
	SHIPS_COUNT_MAX = {
		1: 4,
		2: 3,
		3: 2,
		4: 1
	}
	
	def addShip(self, size : ShipSize, pos : BoardPoint, orientation : Orientation):
		""" Add ship to board, if placed correctly on board.
		If there are too much ships of some size, raises TooMuchShipsOfSize.
		In case when ship is colliding with another ships, ShipIsColliding is raised.
		"""
		s = Ship(size, pos, orientation)
		c = self._getShipsCountBySize(size)
		if c >= self.SHIPS_COUNT_MAX[size]:
			raise TooMuchShipsOfSize(size)
		colliding = list(self._getColliding(s))
		if len(colliding) > 0:
			raise ShipIsColliding(s, colliding)
		self.ships.append(s)

	def addShipVer(self, size : ShipSize, pos : BoardPoint):
		self.addShip(size=size, pos=pos, orientation='vertical')

	def addShipHor(self, size : ShipSize, pos : BoardPoint):
		self.addShip(size=size, pos=pos, orientation='horizontal')

	def _getColliding(self, s : Ship) -> Iterable[Ship]:
		pred = lambda ship: s.collide(ship)
		return filter(pred, self.ships)

	def _getShipsCountBySize(self, size : ShipSize) -> int:
		pred = lambda ship: ship.getSize() == size
		it = filter(pred, self.ships)
		return len(list(it))

	def isReady(self):
		for size, amount in self.SHIPS_COUNT_MAX.items():
			size = cast(ShipSize, size)
			if self._getShipsCountBySize(size) != amount:
				return False
		return True

	def getBoard(self) -> Board:
		if not self.isReady():
			raise Exception('Board is not yet ready')
		return Board(self.ships)
