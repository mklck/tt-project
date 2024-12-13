from dataclasses	import dataclass
from itertools		import product
from enum		import Enum
from .types		import Point
from typing		import List, Optional

import random

class FieldNotEmpty(Exception):
	pass

class BoardPoint(Point):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		err = ValueError(f'Invalid BoardPoint: x = {self.x}, y = {self.y}')
		if self.x < 0 or self.x > 2:
			raise err
		elif self.y < 0 or self.y > 2:
			raise err

class FieldType(Enum):
	empty	= 0
	cross	= 1
	circle	= 2

@dataclass
class Field:
	type	: FieldType
	pos	: BoardPoint

class CircleCross:
	def __init__(self, sign):
            self.fields = list();
            self.last = None;
            self.move_done = 0;
            if sign == 'cross_':
                self.player = FieldType.cross;
            if sign == 'circle':
                self.player = FieldType.circle;
                
	def setPlayer(self):
		self.player = random.choice([FieldType.cross, FieldType.circle])

	def hit(self, bp : BoardPoint, turn):
                if turn == 1:
                        self.checkIfEmpty(bp)
                        field = Field(pos = bp, type=self.player)
                        self.fields.append(field)
                        self.last = bp;
                        self.move_done = 1;
                else:
                        pass

	def togglePlayer(self):
		if self.player is FieldType.circle:
			self.player = FieldType.cross
		else:
			self.player = FieldType.circle

	def checkIfEmpty(self, bp : BoardPoint):
		for x in self.fields:
			if x.pos == bp:
				raise FieldNotEmpty()

	def whoWins(self) -> FieldType:
		t = CircleCrossChecker(self.fields)
		return t.check()

@dataclass
class CircleCrossChecker:
	fields	: List[Field]
	def check(self) -> Optional[FieldType]:
		if t := self.checkDiagonal():
			return t
		if t := self.checkOrtholinear():
			return t
		return None
	def checkOrtholinear(self):
		for x in self.getOrtholinear():
			if t := self.winnable(x):
				return t
		return None
	def winnable(self, l : List[Field]) -> Optional[FieldType]:
		if len(l) != 3:
			return None
		tp = l[0].type
		for f in l:
			if f.type != tp:
				return None
		return tp
	def checkDiagonal(self):
		d0 = [
			BoardPoint(0, 0),
			BoardPoint(1, 1),
			BoardPoint(2, 2),
		]
		d1 = [
			BoardPoint(0, 2),
			BoardPoint(1, 1),
			BoardPoint(2, 0),
		]

		t0 = self.getFieldsWithPosition(d0)
		t1 = self.getFieldsWithPosition(d1)
		print(t0, t1)
		for x in (t0, t1):
			if t := self.winnable(x):
				return t
		return None
	def getFieldsWithPosition(self, pos : List[BoardPoint]):
		pred = lambda f: f.pos in pos
		t = filter(pred, self.fields)
		return list(t)
	def getOrtholinear(self):
		r = range(0, 3)
		for row in r:
			t = filter(lambda f: f.pos.y == row, self.fields)
			yield list(t)
		
		for col in r:
			t = filter(lambda f: f.pos.x == col, self.fields)
			yield list(t)
