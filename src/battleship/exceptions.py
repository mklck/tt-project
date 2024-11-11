
class InvOrientationException(Exception):
	def __init__(self, type):
		super().__init__()
		self.type = type
	def __str__(self):
		return f'Invalid orientation {self.type}, expected "v" or "h"'

class ShipIsColliding(Exception):
	def __init__(self, ship : 'Ship', collisions : list['Ship']):
		self.ship = ship
		self.collisions = collisions

class InvalidShipSize(Exception):
	pass

class TooMuchShipsOfSize(Exception):
	pass

class PositionHitBefore(Exception):
	def __init__(self, p):
		super().__init__()
		self.p = p
	def __str__(self):
		return f"Position {self.p.toAlnum()} hit before"

class ShipInvalidPosition(Exception):
	def __init__(self, position, orientation):
		super().__init__()
		self.position = position
		self.orientation = orientation
	def __str__(self):
		return f'Invalid ship position {self.position}'
		' for orientation {self.orientation}'
