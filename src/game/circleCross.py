from dataclasses	import dataclass
from enum		import Enum

from .types		import Point

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
	def __init__(self):
		self.fields = list()
		self.setPlayer()

	def setPlayer(self):
		self.player = random.choice([FieldType.cross, FieldType.circle])

	def hit(self, bp : BoardPoint):
		self.checkIfEmpty(bp)
		field = Field(pos = bp, type=self.player)
		self.fields.append(field)
		self.togglePlayer()

	def togglePlayer(self):
		if self.player is FieldType.circle:
			self.player = FieldType.cross
		else:
			self.player = FieldType.circle

	def checkIfEmpty(self, bp : BoardPoint):
		for x in self.fields:
			if x.pos == bp:
				raise FieldNotEmpty()
